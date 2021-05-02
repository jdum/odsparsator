#!/usr/bin/env python
# Copyright 2021 Jérôme Dumonteil
# Licence: MIT
# Authors: jerome.dumonteil@gmail.com
"""Generate a json file from an OpenDocument Format .ods file.

When used as a script, odsparsator parses an .ods file and generates a json
file using the odfdo library.

When used as a library, odsparsator parses an .ods file and returns a python
structure.

The resulting data follow the format of the reverse odsgenerator.py script.
"""

import sys
import argparse
from decimal import Decimal
import json

import odfdo
from odfdo import Document

__version__ = "1.1.0"


BODY = "body"
TABLE = "table"
ROW = "row"
VALUE = "value"
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
    def __init__(self, path):
        """Core class of odsparsator.

        The class parses the input .ods content. The result is available in
        self.content. Use ODSParsator via the front-end function ods_to_json()
        to save the content as json file.

        Args:
            path (ODF path): Input .ods file.
        """
        self.doc = Document(path)
        self.content = None
        if not self.is_spreadsheet():
            raise ValueError("Input file must be an .ods file.")
        self.col_widths = self.collect_col_widths()
        self.parse()

    def collect_col_widths(self):
        """Collect all columns widths from styles.

        Returns:
            dict: Style name -> width string.
        """
        widths = {}
        for style in self.doc.get_styles(family="table-column"):
            try:
                widths[style.name] = style.get_properties("table-column")[
                    "style:column-width"
                ]
            except (KeyError, TypeError):
                pass
        return widths

    def all_styles(self):
        """Store all automatic styles of the document.

        Returns:
            dict: Style name -> style XML string.
        """
        styles = []
        for s in self.doc.get_styles(automatic=True):
            name = s.name
            if name:
                s.set_attribute("style:name", None)
                styles.append({NAME: name, DEFINITION: s.serialize(pretty=True)})
        return styles

    def parse(self):
        """Parse the .ods content and store it in self.content."""
        self.content = {BODY: []}
        for t in self.doc.body.get_tables():
            t.rstrip(aggressive=True)
            self.content[BODY].append(self.parse_table(t))
        self.content[STYLES] = self.all_styles()

    def parse_table(self, table):
        """Parse the table content.

        Args:
            table (odfdo.Table): Table object.

        Returns:
            dict: Python content of the table.
        """
        record = {NAME: table.name}
        record[TABLE] = [self.parse_row(row) for row in table.traverse()]
        record[WIDTH] = self.columns_width(table)
        return record

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
            w = self.col_widths.get(style_name)
            if not w:
                break
            widths.append(w)
        return widths

    @staticmethod
    def json_convert(cell):
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
        cells = [self.parse_cell(c) for c in row.traverse()]
        if style:
            return {ROW: cells, STYLE: style}
        return cells

    def parse_cell(self, cell):
        """Parse the cell content.

        Args:
            cell (odfdo.Cell): Cell object.

        Returns:
            value or dict: Python content of the cell.
        """

        value = self.json_convert(cell)
        spanned = self.spanned(cell)
        style = cell.style
        if not spanned and not style:
            return value
        record = {VALUE: value}
        if style:
            record[STYLE] = style
        if spanned:
            record.update(spanned)
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

    def json_content(self):
        """JSON string of the content."""
        return json.dumps(self.content, ensure_ascii=False, indent=4)


def ods_to_json(input_path, output_path):
    """Parse the input file and save the result in a json file.

    The input file must be a .ods ODF file

    Args:
        input_path (str or Path): Path of the .ods file
        output_path (str or Path or BytesIO): Path of the json output file.
    """
    content = ODSParsator(input_path).content
    json_content = json.dumps(content, ensure_ascii=False, indent=4)
    with open(output_path, "w", encoding="UTF-8") as f:
        f.write(json_content)


def ods_to_python(input_path):
    """Parse the input file and return the content as python structure.

    The input file must be a .ods ODF file

    Args:
        input_path (str or Path): Path of the .ods file

    Returns:
        dict or list: content of the .ods file
    """
    return ODSParsator(input_path).content


def check_odfdo_version():
    """Utility to verify we have the minimal version of the odfdo library."""
    if tuple(int(x) for x in odfdo.__version__.split(".")) > (3, 3, 0):
        return True
    print("Error: I need odfdo version >= 3.3.0")
    return False


def main():
    """Read parameters from STDIN and apply the required command.

    Usage:
       odsparsator [-h] [--version] [options] input_file output_file

    Arguments:
        input_file: Input file, a .ods file.

        output_file: Output file, json file generated from input.
    """
    if not check_odfdo_version():
        sys.exit(1)
    parser = argparse.ArgumentParser(
        description="Generate a json file from an OpenDocument Format .ods file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument(
        "input_file", help="input file containing data in json or yaml format"
    )
    parser.add_argument(
        "output_file", help="output file, .ods file generated from input"
    )
    args = parser.parse_args()
    ods_to_json(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
