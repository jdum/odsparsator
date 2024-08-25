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
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from odfdo import Document, Element
from odfdo.cell import Cell
from odfdo.document import Table
from odfdo.row import Row

__version__ = "1.11.0"


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
        export_minimal: bool = False,
        use_decimal: bool = False,
        all_styles: bool = False,
        colors: bool = False,
        keep_styled: bool = False,
    ) -> None:
        """Class in charge of parsing the .ods document..

        Use ODSParsator via the front-end function ods_to_json() to save the
        content as json file.

        Args:
            Boolean options
        """
        self.doc: Document | None = None
        self.body: Element = []
        self.styles: list = []
        self.col_widths: dict = {}
        self.export_full: bool = not export_minimal
        self.use_decimal: bool = use_decimal
        self.all_styles: bool = all_styles
        self.colors: bool = colors
        self.keep_styled: bool = keep_styled
        self._current_table: Table | None = None
        self._doc_style_cache: dict[tuple[str, str], dict[str, Any]] = {}
        self._current_table_column_cache: dict[int, str] = {}

    def collect_col_widths(self) -> None:
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

    def collect_all_styles(self) -> None:
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

    def collect_used_styles(self) -> None:  # noqa: C901
        """Store used automatic styles of the document.

        Styles are a list of dict: Name and definition of styles.
        """

        styles_elements = {}
        used_styles = set()

        def store_style_name(name: str | None) -> None:
            if not name:
                return
            if name not in used_styles and name in styles_elements:
                style = styles_elements[name]
                used_styles.add(name)
                # add style dependacies
                for key, value in style.attributes.items():
                    if key.endswith("style-name"):
                        store_style_name(value)

        def keep_style(item: Any) -> None:
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

    def parse_document(self, document_path: Path | str) -> None:
        """Parse the input .ods file..

        The result is available in self.content or self.content_json.

        Args:
            path (ODF path): Input .ods file.
        """
        self.load_document(document_path)
        self.parse()

    def load_document(self, document_path: Path | str) -> None:
        """Load the ODF file and checks its type."""
        self.doc = Document(document_path)
        if not self.is_spreadsheet():
            raise ValueError("Input file must be a .ods file.")

    def parse(self) -> None:
        """Parse the .ods content."""
        self.collect_col_widths()
        self.collect_tables()
        if self.export_full:
            if self.all_styles:
                self.collect_all_styles()
            else:
                self.collect_used_styles()

    def collect_tables(self) -> None:
        """Retrieve all tables of the input document."""
        self.body = []
        for table in self.doc.body.get_tables():
            self.initialize_table(table)
            self.parse_table(table)

    def initialize_table(self, table: Table) -> None:
        """Shrink table keeping empty calls or strongly strip
        the table.

        Args:
            table (odfdo.Table): Table object.
        """
        self._current_table_column_cache = {}
        self._current_table = table  # for default bgcolor
        if self.keep_styled:
            table.optimize_width()
        else:
            table.rstrip(aggressive=True)

    def parse_table(self, table: Table) -> None:
        """Parse one table content.

        Args:
            table (odfdo.Table): Table object.
        """
        record = {NAME: table.name}
        record[TABLE] = [self.parse_row(row) for row in table.traverse()]
        if self.export_full:
            record[WIDTH] = self.columns_width(table)
        self.body.append(record)

    def columns_width(self, table: Table) -> list[str]:
        """Retrieve the table columsn widths.

        Args:
            table (odfdo.Table): Table object.

        Returns:
            list: List of widths.
        """
        # parse "table-column" styles, keep only the width component
        widths: list[str] = []
        for col in table.get_columns():
            style_name = col.style
            width = self.col_widths.get(style_name)
            if not width:
                break
            widths.append(width)
        return widths

    @staticmethod
    def json_convert(cell: Cell) -> Any:  # pylint: disable=too-many-return-statements
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

    def parse_row(self, row: Row) -> list | dict:
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

    def parse_cell(self, cell: Cell) -> Any:
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

    def _style_cell_properties(self, family_style: tuple[str, str]) -> dict[str, Any]:
        if props := self._doc_style_cache.get(family_style):
            return props
        props = (
            self.doc.get_style_properties(
                family_style[0], family_style[1], "table-cell"
            )
            or {}
        )
        self._doc_style_cache[family_style] = props
        return props

    def _column_bgcolor(self, column_nb: int) -> str:
        if color := self._current_table_column_cache.get(column_nb):
            return color
        column = self._current_table.get_column(column_nb)
        if style := column.get_default_cell_style():
            props = self._style_cell_properties(("table-cell", style))
            color = props.get("fo:background-color", DEFAULT_BGCOLOR)
        else:
            color = DEFAULT_BGCOLOR
        self._current_table_column_cache[column_nb] = color
        return color

    def cell_bgcolor(self, row: Row, cell: Cell) -> str:
        if cell.style:
            props = self._style_cell_properties(("table-cell", cell.style))
            return props.get("fo:background-color", DEFAULT_BGCOLOR)
        if row.style:
            props = self._style_cell_properties(("table-row", row.style))
            if props:
                return props.get("fo:background-color", DEFAULT_BGCOLOR)
        return self._column_bgcolor(cell.x)

    @staticmethod
    def spanned(cell: Cell) -> dict | None:
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

    def is_spreadsheet(self) -> bool:
        """Check the ODF document is a spreadsheet"""
        return bool(self.doc.get_type() == "spreadsheet")

    @property
    def content(self) -> dict[str, Any]:
        """Python dict of the content."""
        if self.export_full:
            return {BODY: self.body, STYLES: self.styles}
        return {BODY: self.body}

    @property
    def json_content(self) -> str:
        """JSON string of the content."""
        return json.dumps(self.content, ensure_ascii=False, indent=4, sort_keys=True)


def ods_to_json(
    input_path: Path | str,
    output_path: Path | str,
    export_minimal: bool = False,
    all_styles: bool = False,
    colors: bool = False,
    keep_styled: bool = False,
) -> None:
    """Parse the input file and save the result in a json file.

    The input file must be a .ods ODF file

    Args:
        input_path (str or Path): Path of the .ods file
        output_path (str or Path or BytesIO): Path of the json output file.
        export_minimal (bool): Export only values, no styles or formula or col width.
        all_styles (bool): Collect all styles from the input.
        colors (bool): Collect background color of cells.
        keep_styled (bool): Keep styled cells with empty value.
    """
    parser = ODSParsator(
        export_minimal=export_minimal,
        use_decimal=False,
        all_styles=all_styles,
        colors=colors,
        keep_styled=keep_styled,
    )
    parser.parse_document(input_path)
    Path(output_path).write_text(parser.json_content, encoding="utf8")


def ods_to_python(
    input_path: Path | str,
    export_minimal: bool = False,
    use_decimal: bool = False,
    all_styles: bool = False,
    colors: bool = False,
    keep_styled: bool = False,
) -> dict[str, Any] | list[Any]:
    """Parse the input file and return the content as python structure.

    The input file must be a .ods ODF file

    Args:
        input_path (str or Path): Path of the .ods file
        export_minimal (bool): Export only values, no styles or formula or col width.
        use_decimal (bool): Use Decimal(), DateTime() for the cell values.
        all_styles (bool): Collect all styles from the input.
        colors (bool): Collect background color of cells.
        keep_styled (bool): Keep styled cells with empty value.

    Returns:
        dict or list: content as python structure
    """
    parser = ODSParsator(
        export_minimal=export_minimal,
        use_decimal=use_decimal,
        all_styles=all_styles,
        colors=colors,
        keep_styled=keep_styled,
    )
    parser.parse_document(input_path)
    return parser.content
