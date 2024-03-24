from pathlib import Path

import odsparsator.odsparsator as parser

DATA = Path(__file__).parent / "data"
FILE_BLUE = DATA / "col_cell_blue.ods"


def test_blue_content_base_minimal():
    body = parser.ods_to_python(FILE_BLUE, export_minimal=True)["body"]
    # no celle values
    # -> display empty result
    expected = [{"name": "Sheet1", "table": []}]
    assert body == expected


def test_blue_content_base_color():
    body = parser.ods_to_python(FILE_BLUE, colors=True)["body"]
    # no "keep" parameter:
    # -> empty cells are removed
    # -> empty result, no cell color to show
    expected = [{"name": "Sheet1", "table": [], "width": []}]
    assert body == expected


def test_blue_content_base_keep():
    body = parser.ods_to_python(FILE_BLUE, keep_styled=True)["body"]
    # keep_styled
    # -> do not erase colored empty cells
    # -> see yellow cell of style ce2
    expected = [
        {
            "name": "Sheet1",
            "table": [
                {"row": [None, None, None], "style": "ro1"},
                {"row": [None, {"style": "ce2", "value": None}, None], "style": "ro1"},
                {"row": [None, None, None], "style": "ro1"},
            ],
            "width": ["2.258cm", "2.258cm", "2.258cm"],
        }
    ]
    assert body == expected


def test_blue_content_keep_minimal():
    body = parser.ods_to_python(
        FILE_BLUE,
        keep_styled=True,
        export_minimal=True,
    )["body"]
    # keep_styled, export minimal
    # -> do not erase colored empty cells
    # -> but without style, does only show structure
    expected = [
        {
            "name": "Sheet1",
            "table": [[None, None, None], [None, None, None], [None, None, None]],
        }
    ]
    assert body == expected


def test_blue_content_keep_colors():
    body = parser.ods_to_python(
        FILE_BLUE,
        keep_styled=True,
        colors=True,
    )["body"]
    # keep_styled, show colors
    # -> do not erase colored empty cells
    # -> display "bgcolor" key
    expected = [
        {
            "name": "Sheet1",
            "table": [
                {
                    "row": [
                        {"bgcolor": "#2a6099", "value": None},
                        {"bgcolor": "#2a6099", "value": None},
                        {"bgcolor": "#2a6099", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#2a6099", "value": None},
                        {"bgcolor": "#ffff00", "style": "ce2", "value": None},
                        {"bgcolor": "#2a6099", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#2a6099", "value": None},
                        {"bgcolor": "#2a6099", "value": None},
                        {"bgcolor": "#2a6099", "value": None},
                    ],
                    "style": "ro1",
                },
            ],
            "width": ["2.258cm", "2.258cm", "2.258cm"],
        }
    ]

    assert body == expected


def test_blue_content_keep_colors_minimal():
    body = parser.ods_to_python(
        FILE_BLUE,
        keep_styled=True,
        colors=True,
        export_minimal=True,
    )["body"]
    # keep_styled, show colors, export minimal
    # -> do not erase colored empty cells
    # -> display only "bgcolor" and "value" keys
    expected = [
        {
            "name": "Sheet1",
            "table": [
                [
                    {"bgcolor": "#2a6099", "value": None},
                    {"bgcolor": "#2a6099", "value": None},
                    {"bgcolor": "#2a6099", "value": None},
                ],
                [
                    {"bgcolor": "#2a6099", "value": None},
                    {"bgcolor": "#ffff00", "value": None},
                    {"bgcolor": "#2a6099", "value": None},
                ],
                [
                    {"bgcolor": "#2a6099", "value": None},
                    {"bgcolor": "#2a6099", "value": None},
                    {"bgcolor": "#2a6099", "value": None},
                ],
            ],
        }
    ]

    assert body == expected
