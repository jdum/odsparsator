# Copyright 2021-2024 Jérôme Dumonteil
# Licence: MIT
# Authors: jerome.dumonteil@gmail.com
"""Generate a json file from an OpenDocument Format .ods file.

When used as a script, odsparsator parses a .ods file and generates a json
file using the odfdo library.

When used as a library, odsparsator parses a .ods file and returns a python
structure.

The resulting data follow the format of the reverse odsgenerator.py script.
"""

from functools import cache
import json
from decimal import Decimal
from pathlib import Path

from odfdo import Document, Element
from odfdo.cell import Cell
from odfdo.document import Table
from odfdo.frame import Any
from odfdo.row import Row

__version__ = "1.9.0"


BODY = "body"
TABLE = "table"
ROW = "row"
VALUE = "value"
FORMULA = "formula"
BGCOLOR = "bgcolor"
COLSPAN = "colspanned"
ROWSPAN = "rowspanned"
NAME = "name"
DEFINITION = "definition"
WIDTH = "width"
SPAN = "span"
STYLE = "style"
STYLES = "styles"
DEFAULT_BGCOLOR = "#ffffff"

NBCOLSPAN = "table:number-columns-spanned"
NBROWSPAN = "table:number-rows-spanned"


class ODSParsator:
    def __init__(
        self,
        export_minimal=False,
        use_decimal=False,
        all_styles=False,
        colors=False,
    ):
        """Class in charge of parsing the .ods document..

        Use ODSParsator via the front-end function ods_to_json() to save the
        content as json file.

        Args:
            Boolean options
        """
        self.doc = None
        self.body = []
        self.styles = []
        self.col_widths = {}
        self.export_full = not export_minimal
        self.use_decimal = use_decimal
        self.all_styles = all_styles
        self.colors = colors
        self._default_bgcolor = ""
        self._current_table = None
        self._current_table_column_cache = {}

    def collect_col_widths(self):
        """Collect all columns widths from styles."""
        self.col_widths = {}
        if not self.export_full:
            return
        for style in self.doc.get_styles(family="table-column"):
            try:
                width = style.get_properties("table-column")["style:column-width"]
                self.col_widths[style.name] = width
            except (KeyError, TypeError):
                pass

    def collect_all_styles(self):
        """Store all automatic styles of the document.

        Styles are a list of dict: Name and definition of styles.
        """
        self.styles = []
        for style in self.doc.get_styles(automatic=True):
            name = style.name
            if name:
                style.set_attribute("style:name", None)
                self.styles.append(
                    {
                        NAME: name,
                        DEFINITION: style.serialize(pretty=True),
                    }
                )

    def collect_used_styles(self):  # noqa: C901
        """Store used automatic styles of the document.

        Styles are a list of dict: Name and definition of styles.
        """

        styles_elements = {}
        used_styles = set()

        def store_style_name(name):
            if not name:
                return
            if name not in used_styles and name in styles_elements:
                style = styles_elements[name]
                used_styles.add(name)
                # add style dependacies
                for key, value in style.attributes.items():
                    if key.endswith("style-name"):
                        store_style_name(value)

        def keep_style(item):
            if isinstance(item, dict):
                store_style_name(item.get(STYLE))

        self.collect_all_styles()
        for style in self.styles:
            name = style.get(NAME)
            definition = style.get(DEFINITION)
            style = Element.from_tag(definition)
            styles_elements[name] = style
        for table in self.body:
            keep_style(table)
            for row in table[TABLE]:
                if isinstance(row, dict):
                    keep_style(row)
                    cells = row[ROW]
                else:
                    cells = row
                for cell in cells:
                    keep_style(cell)
        self.styles = []
        for name in used_styles:
            style = styles_elements[name]
            if style.name:
                style.set_attribute("style:name", None)
            self.styles.append(
                {
                    NAME: name,
                    DEFINITION: style.serialize(pretty=True),
                }
            )

    def parse_document(self, document_path):
        """Parse the input .ods file..

        The result is available in self.content or self.content_json.

        Args:
            path (ODF path): Input .ods file.
        """
        self.load_document(document_path)
        self.parse()

    def load_document(self, document_path):
        """Load the ODF file and checks its type."""
        self.doc = Document(document_path)
        if not self.is_spreadsheet():
            raise ValueError("Input file must be a .ods file.")

    def parse(self):
        """Parse the .ods content."""
        self.collect_col_widths()
        self.collect_tables()
        if self.export_full:
            if self.all_styles:
                self.collect_all_styles()
            else:
                self.collect_used_styles()

    def collect_tables(self):
        """Retrieve all tables of the input document."""
        self.body = []
        aggressive = not self.colors
        for table in self.doc.body.get_tables():
            self._current_table_column_cache = {}
            self._current_table = table  # for default bgcolor
            table.rstrip(aggressive=aggressive)
            self.parse_table(table)

    def parse_table(self, table):
        """Parse one table content.

        Args:
            table (odfdo.Table): Table object.
        """
        record = {NAME: table.name}
        record[TABLE] = [self.parse_row(row) for row in table.traverse()]
        if self.export_full:
            record[WIDTH] = self.columns_width(table)
        self.body.append(record)

    def columns_width(self, table):
        """Retrieve the table columsn widths.

        Args:
            table (odfdo.Table): Table object.

        Returns:
            list: List of widths.
        """
        # parse "table-column" styles, keep only the width component
        widths = []
        for col in table.get_columns():
            style_name = col.style
            width = self.col_widths.get(style_name)
            if not width:
                break
            widths.append(width)
        return widths

    @staticmethod
    def json_convert(cell):  # pylint: disable=too-many-return-statements
        """Convert the value of the cell in a basic python type.

        Args:
            cell (odfdo.Cell): The ODF cell.

        Returns:
            any: Cell value.
        """
        value_type = cell.get_attribute("office:value-type")
        if value_type == "boolean":
            return cell.get_attribute("office:boolean-value")
        if value_type in {"float", "percentage", "currency"}:
            value = Decimal(cell.get_attribute("office:value"))
            if int(value) == value:
                return int(value)
            return float(value)
        if value_type == "date":
            return cell.get_attribute("office:date-value")
        if value_type == "time":
            return cell.get_attribute("office:time-value")
        if value_type == "string":
            value = cell.get_attribute("office:string-value")
            if value is not None:
                return value
            value = []
            for para in cell.get_elements("text:p"):
                value.append(para.text_recursive)
            return "\n".join(value)
        return None

    def parse_row(self, row):
        """Parse the row content.

        Args:
            row (odfdo.Row): Row object.

        Returns:
            list or dict: Python content of the row.
        """
        style = row.style
        if self.colors:
            cells = [self.parse_cell_color(row, cell) for cell in row.traverse()]
        else:
            cells = [self.parse_cell(cell) for cell in row.traverse()]
        if style and self.export_full:
            return {ROW: cells, STYLE: style}
        return cells

    def parse_cell(self, cell):
        """Parse the cell content.

        Args:
            cell (odfdo.Cell): Cell object.

        Returns:
            value or dict: Python content of the cell.
        """
        if self.use_decimal:
            value = cell.get_value()
        else:
            value = self.json_convert(cell)
        spanned = self.spanned(cell)
        if self.export_full:
            style = cell.style
            formula = cell.formula
        else:
            style = None
            formula = None
        if not spanned and not style and not formula and not self.colors:
            return value
        record = {VALUE: value}
        if style:
            record[STYLE] = style
        if spanned:
            record.update(spanned)
        if formula:
            record[FORMULA] = formula
        return record

    def parse_cell_color(self, row: Row, cell: Cell) -> dict[str, Any]:
        """Parse the cell content, including cell background color.

        Args:
            row (odfdo.Row): Row object.
            cell (odfdo.Cell): Cell object.

        Returns:
            dict: Python content of the cell.
        """
        record = self.parse_cell(cell)
        record[BGCOLOR] = self.cell_bgcolor(row, cell)
        return record

    @cache
    def _style_cell_properties(self, family: str, style: str) -> dict[str, Any]:
        return self.doc.get_style_properties(family, style, "table-cell") or {}

    def _column_bgcolor(self, column_nb: int) -> str:
        if column_nb in self._current_table_column_cache:
            return self._current_table_column_cache[column_nb]
        column = self._current_table.get_column(column_nb)
        if style := column.get_default_cell_style():
            props = self._style_cell_properties("table-cell", style)
            color = props.get("fo:background-color", DEFAULT_BGCOLOR)
        else:
            color = DEFAULT_BGCOLOR
        self._current_table_column_cache[column_nb] = color
        return color

    def cell_bgcolor(self, row: Row, cell: Cell) -> str:
        if cell.style:
            props = self._style_cell_properties("table-cell", cell.style)
            return props.get("fo:background-color", DEFAULT_BGCOLOR)
        if row.style:
            props = self._style_cell_properties("table-row", row.style)
            if props:
                return props.get("fo:background-color", DEFAULT_BGCOLOR)
        return self._column_bgcolor(cell.x)

    def get_cell_style_properties(
        self, table: str | int, coord: tuple | list | str
    ) -> dict[str, str]:  # type: ignore
        """Return the style properties of a table cell of a .ods document,
        from the cell style or from the row style."""

        def _get_table(table: int | str) -> Table | None:
            table_pos = 0
            table_name = None
            if isinstance(table, int):
                table_pos = table
            elif isinstance(table, str):
                table_name = table_name
            else:
                raise TypeError(f"Table parameter must be int or str: {table!r}")
            return self.body.get_table(
                position=table_pos, name=table_name  # type: ignore
            )

        if not (sheet := _get_table(table)):
            return {}
        cell = sheet.get_cell(coord, clone=False)
        if cell.style:
            return (
                self.get_style_properties("table-cell", cell.style, "table-cell") or {}
            )
        try:
            row = sheet.get_row(cell.y, clone=False, create=False)  # type: ignore
            if row.style:  # noqa: SIM102
                if props := self.get_style_properties(
                    "table-row", row.style, "table-cell"
                ):
                    return props
            column = sheet.get_column(cell.x)  # type: ignore
            if style := column.get_default_cell_style():
                return (
                    self.get_style_properties("table-cell", style, "table-cell") or {}
                )
        except ValueError:
            return {}

    def get_cell_background_color(
        self,
        table: str | int,
        coord: tuple | list | str,
        default: str = "#ffffff",
    ) -> str:
        """Return the background color of a table cell of a .ods document,
        from the cell style, or from the row or column.

        If color is not defined, return default value."""
        found = self.get_cell_style_properties(table, coord).get("fo:background-color")
        return found or default

    @staticmethod
    def spanned(cell):
        """Detect and retrieve the spanned columns and rows of the cell.

        Args:
            cell (odfdo.Cell): Cell object.

        Returns:
            dict or None: Spanned parameters.
        """
        if (
            cell.get_attribute(NBCOLSPAN) is None
            and cell.get_attribute(NBROWSPAN) is None
        ):
            return None
        try:
            cols = int(cell.get_attribute(NBCOLSPAN))
            rows = int(cell.get_attribute(NBROWSPAN))
        except (TypeError, ValueError):
            return None
        if cols > 1 or rows > 1:
            return {COLSPAN: cols, ROWSPAN: rows}
        return None

    def is_spreadsheet(self):
        """Check the ODF document is a spreadsheet"""
        return bool(self.doc.get_type() == "spreadsheet")

    @property
    def content(self):
        """Python dict of the content."""
        if self.export_full:
            return {BODY: self.body, STYLES: self.styles}
        return {BODY: self.body}

    @property
    def json_content(self):
        """JSON string of the content."""
        return json.dumps(self.content, ensure_ascii=False, indent=4, sort_keys=True)


def ods_to_json(
    input_path,
    output_path,
    export_minimal=False,
    all_styles=False,
    colors=False,
):
    """Parse the input file and save the result in a json file.

    The input file must be a .ods ODF file

    Args:
        input_path (str or Path): Path of the .ods file
        output_path (str or Path or BytesIO): Path of the json output file.
        export_minimal (bool): Export only values, no styles or formula or col width.
        all_styles (bool): Collect all styles from the input.
        colors (bool): Collect background color of cells.
    """
    parser = ODSParsator(
        export_minimal=export_minimal,
        use_decimal=False,
        all_styles=all_styles,
        colors=colors,
    )
    parser.parse_document(input_path)
    Path(output_path).write_text(parser.json_content, encoding="utf8")


def ods_to_python(
    input_path,
    export_minimal=False,
    use_decimal=False,
    all_styles=False,
    colors=False,
):
    """Parse the input file and return the content as python structure.

    The input file must be a .ods ODF file

    Args:
        input_path (str or Path): Path of the .ods file
        export_minimal (bool): Export only values, no styles or formula or col width.
        use_decimal (bool): Use Decimal(), DateTime() for the cell values.
        all_styles (bool): Collect all styles from the input.
        colors (bool): Collect background color of cells.

    Returns:
        dict or list: content as python structure
    """
    parser = ODSParsator(
        export_minimal=export_minimal,
        use_decimal=use_decimal,
        all_styles=all_styles,
        colors=colors,
    )
    parser.parse_document(input_path)
    return parser.content
