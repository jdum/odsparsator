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

import json
from decimal import Decimal
from pathlib import Path

from odfdo import Document, Element

__version__ = "1.9.0"


BODY = "body"
TABLE = "table"
ROW = "row"
VALUE = "value"
FORMULA = "formula"
COLSPAN = "colspanned"
ROWSPAN = "rowspanned"
NAME = "name"
DEFINITION = "definition"
WIDTH = "width"
SPAN = "span"
STYLE = "style"
STYLES = "styles"

NBCOLSPAN = "table:number-columns-spanned"
NBROWSPAN = "table:number-rows-spanned"


class ODSParsator:
    def __init__(
        self,
        export_minimal=False,
        use_decimal=False,
        all_styles=False,
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
        for table in self.doc.body.get_tables():
            table.rstrip(aggressive=True)
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
        if not spanned and not style and not formula:
            return value
        record = {VALUE: value}
        if style:
            record[STYLE] = style
        if spanned:
            record.update(spanned)
        if formula:
            record[FORMULA] = formula
        return record

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
):
    """Parse the input file and save the result in a json file.

    The input file must be a .ods ODF file

    Args:
        input_path (str or Path): Path of the .ods file
        output_path (str or Path or BytesIO): Path of the json output file.
        export_minimal (bool): Export only values, no styles or formula or col width.
        all_styles (bool): Collect all styles from the input.
    """
    parser = ODSParsator(
        export_minimal=export_minimal,
        use_decimal=False,
        all_styles=all_styles,
    )
    parser.parse_document(input_path)
    Path(output_path).write_text(parser.json_content, encoding="utf8")


def ods_to_python(
    input_path,
    export_minimal=False,
    use_decimal=False,
    all_styles=False,
):
    """Parse the input file and return the content as python structure.

    The input file must be a .ods ODF file

    Args:
        input_path (str or Path): Path of the .ods file
        export_minimal (bool): Export only values, no styles or formula or col width.
        use_decimal (bool): Use Decimal(), DateTime() for the cell values.
        all_styles (bool): Collect all styles from the input.

    Returns:
        dict or list: content as python structure
    """
    parser = ODSParsator(
        export_minimal=export_minimal,
        use_decimal=use_decimal,
        all_styles=all_styles,
    )
    parser.parse_document(input_path)
    return parser.content
