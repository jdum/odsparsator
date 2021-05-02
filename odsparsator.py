#!/usr/bin/env python
# Copyright 2021 Jérôme Dumonteil
# Licence: MIT
# Authors: jerome.dumonteil@gmail.com
"""xxx
"""

import sys
import argparse
from decimal import Decimal
import json
import odfdo
from odfdo import Document, Table, Row, Cell, Element

__version__ = "0.5"


BODY = "body"
TABLE = "table"
ROW = "row"
VALUE = "value"
COLSPAN = "colspanned"
ROWSPAN = "rowspanned"
TEXT = "text"
NAME = "name"
DEFINITION = "definition"
WIDTH = "width"
SPAN = "span"
STYLE = "style"
STYLES = "styles"
DEFAULTS = "defaults"

NBCOLSPAN = "table:number-columns-spanned"
NBROWSPAN = "table:number-rows-spanned"


def check_odfdo_version():
    """Utility to verify we have the minimal version of the odfdo library."""
    if tuple(int(x) for x in odfdo.__version__.split(".")) > (3, 3, 0):
        return True
    print("Error: I need odfdo version >= 3.3.0")
    return False


class ODSParser:
    def __init__(self, path):
        self.doc = Document(path)
        self.content = None
        if not self.is_spreadsheet():
            return
        self.col_widths = self.collect_col_widths()
        self.parse()

    def collect_col_widths(self):
        widths = {}
        for style in self.doc.get_styles(family="table-column"):
            try:
                widths[style.name] = style.get_properties("table-column")[
                    "style:column-width"
                ]
            except (KeyError, TypeError):
                pass
        return widths

    def parse(self):
        self.content = {"body": []}
        for t in self.doc.body.get_tables():
            t.rstrip(aggressive=True)
            self.content["body"].append(self.parse_table(t))

    def parse_table(self, table):
        record = {"name": table.name}
        record["table"] = [self.parse_row(row) for row in table.traverse()]
        record["width"] = self.parse_columns_width(table)
        return record

    def parse_columns_width(self, table):
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
        return [self.parse_cell(c) for c in row.traverse()]

    def parse_cell(self, cell):
        value = self.json_convert(cell)
        spanned = self.spanned(cell)
        if not spanned:
            return value
        spanned["value"] = value
        return spanned

    def spanned(self, cell):
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
        return bool(self.doc.get_type() == "spreadsheet")

    def export(self):
        return json.dumps(self.content, ensure_ascii=False, indent=4)

    def print(self):
        print(self.export())

    def save(self, path):
        with open(path, "w", encoding="UTF-8") as f:
            f.write(self.export())


def main():
    if not check_odfdo_version():
        sys.exit(1)
    ods = sys.argv[1]
    p = ODSParser(ods)
    p.save("a.json")


if __name__ == "__main__":
    main()
