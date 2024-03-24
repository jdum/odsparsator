from pathlib import Path

import odsparsator.odsparsator as parser

DATA = Path(__file__).parent / "data"
FILE_COLS = DATA / "col_cell.ods"


def test_content_base_minimal():
    body = parser.ods_to_python(FILE_COLS, export_minimal=True)["body"]
    # minimal only: only not empty values are displayeds
    expected = [
        {
            "name": "Sheet1",
            "table": [
                [],
                ["r"],
                ["s"],
                [],
                [],
                [],
                [],
                ["a", "b", "c", "d"],
                [],
                ["e", "f"],
                [],
                [],
                [],
                [None, None, None, None, None, "x"],
            ],
        }
    ]

    assert body == expected


def test_content_base_color():
    body = parser.ods_to_python(FILE_COLS, colors=True)["body"]
    # no "keep" parameter:
    # -> empty cells are removed
    # -> empty result, no cell color to show for empty cells
    # -> but tag "bgcolors" displayed for rows and valued cells"
    expected = [
        {
            "name": "Sheet1",
            "table": [
                {"row": [], "style": "ro1"},
                {
                    "row": [{"bgcolor": "#ffffff", "style": "ce1", "value": "r"}],
                    "style": "ro1",
                },
                {
                    "row": [{"bgcolor": "#ffffff", "style": "ce2", "value": "s"}],
                    "style": "ro1",
                },
                {"row": [], "style": "ro1"},
                {"row": [], "style": "ro1"},
                {"row": [], "style": "ro1"},
                {"row": [], "style": "ro1"},
                {
                    "row": [
                        {"bgcolor": "#b4c7dc", "style": "ce4", "value": "a"},
                        {"bgcolor": "#b4c7dc", "style": "ce4", "value": "b"},
                        {"bgcolor": "#ffff6d", "style": "ce11", "value": "c"},
                        {"bgcolor": "#ff3838", "style": "ce10", "value": "d"},
                    ],
                    "style": "ro1",
                },
                {"row": [], "style": "ro1"},
                {
                    "row": [
                        {"bgcolor": "#ed4c05", "style": "ce5", "value": "e"},
                        {"bgcolor": "#ed4c05", "style": "ce5", "value": "f"},
                    ],
                    "style": "ro1",
                },
                {"row": [], "style": "ro1"},
                {"row": [], "style": "ro1"},
                {"row": [], "style": "ro1"},
                {
                    "row": [
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#fff5ce", "style": "ce13", "value": "x"},
                    ],
                    "style": "ro1",
                },
            ],
            "width": ["2.258cm", "2.258cm", "2.258cm", "2.258cm", "2.258cm", "2.258cm"],
        }
    ]
    assert body == expected


def test_content_base_keep():
    body = parser.ods_to_python(FILE_COLS, keep_styled=True)["body"]
    # keep_styled
    # -> do not erase colored empty cells
    # -> but do not explicitely show "bgcolor" tag
    expected = [
        {
            "name": "Sheet1",
            "table": [
                {
                    "row": [
                        None,
                        None,
                        {"style": "ce9", "value": None},
                        None,
                        None,
                        None,
                        None,
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"style": "ce1", "value": "r"},
                        {"style": "ce8", "value": None},
                        {"style": "ce10", "value": None},
                        {"style": "ce10", "value": None},
                        {"style": "ce10", "value": None},
                        None,
                        None,
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"style": "ce2", "value": "s"},
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    ],
                    "style": "ro1",
                },
                {"row": [None, None, None, None, None, None, None], "style": "ro1"},
                {"row": [None, None, None, None, None, None, None], "style": "ro1"},
                {
                    "row": [
                        {"style": "ce3", "value": None},
                        {"style": "ce3", "value": None},
                        {"style": "ce3", "value": None},
                        {"style": "ce3", "value": None},
                        {"style": "ce3", "value": None},
                        None,
                        {"style": "ce3", "value": None},
                    ],
                    "style": "ro1",
                },
                {"row": [None, None, None, None, None, None, None], "style": "ro1"},
                {
                    "row": [
                        {"style": "ce4", "value": "a"},
                        {"style": "ce4", "value": "b"},
                        {"style": "ce11", "value": "c"},
                        {"style": "ce10", "value": "d"},
                        {"style": "ce4", "value": None},
                        None,
                        {"style": "ce4", "value": None},
                    ],
                    "style": "ro1",
                },
                {"row": [None, None, None, None, None, None, None], "style": "ro1"},
                {
                    "row": [
                        {"style": "ce5", "value": "e"},
                        {"style": "ce5", "value": "f"},
                        {"style": "ce5", "value": None},
                        {"style": "ce5", "value": None},
                        {"style": "ce5", "value": None},
                        None,
                        {"style": "ce5", "value": None},
                    ],
                    "style": "ro1",
                },
                {"row": [None, None, None, None, None, None, None], "style": "ro1"},
                {
                    "row": [
                        {"style": "ce6", "value": None},
                        {"style": "ce6", "value": None},
                        {"style": "ce6", "value": None},
                        {"style": "ce6", "value": None},
                        {"style": "ce6", "value": None},
                        None,
                        {"style": "ce6", "value": None},
                    ],
                    "style": "ro1",
                },
                {"row": [None, None, None, None, None, None, None], "style": "ro1"},
                {
                    "row": [
                        None,
                        None,
                        None,
                        None,
                        None,
                        {"style": "ce13", "value": "x"},
                        None,
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"style": "ce7", "value": None},
                        {"style": "ce7", "value": None},
                        {"style": "ce7", "value": None},
                        {"style": "ce7", "value": None},
                        {"style": "ce7", "value": None},
                        {"style": "ce14", "value": None},
                        {"style": "ce7", "value": None},
                    ],
                    "style": "ro1",
                },
                {"row": [None, None, None, None, None, None, None], "style": "ro1"},
            ],
            "width": [
                "2.258cm",
                "2.258cm",
                "2.258cm",
                "2.258cm",
                "2.258cm",
                "2.258cm",
                "2.258cm",
            ],
        }
    ]

    assert body == expected


def test_content_keep_minimal():
    body = parser.ods_to_python(
        FILE_COLS,
        keep_styled=True,
        export_minimal=True,
    )["body"]
    # keep_styled, export minimal
    # -> do not erase colored empty cells
    # -> but without style, does only show structure
    expected = [
        {
            "name": "Sheet1",
            "table": [
                [None, None, None, None, None, None, None],
                ["r", None, None, None, None, None, None],
                ["s", None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                ["a", "b", "c", "d", None, None, None],
                [None, None, None, None, None, None, None],
                ["e", "f", None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, "x", None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
            ],
        }
    ]

    assert body == expected


def test_content_keep_colors():
    body = parser.ods_to_python(
        FILE_COLS,
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
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffff00", "style": "ce9", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "style": "ce1", "value": "r"},
                        {"bgcolor": "#55308d", "style": "ce8", "value": None},
                        {"bgcolor": "#ff3838", "style": "ce10", "value": None},
                        {"bgcolor": "#ff3838", "style": "ce10", "value": None},
                        {"bgcolor": "#ff3838", "style": "ce10", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "style": "ce2", "value": "s"},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#3465a4", "style": "ce3", "value": None},
                        {"bgcolor": "#3465a4", "style": "ce3", "value": None},
                        {"bgcolor": "#3465a4", "style": "ce3", "value": None},
                        {"bgcolor": "#3465a4", "style": "ce3", "value": None},
                        {"bgcolor": "#3465a4", "style": "ce3", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#3465a4", "style": "ce3", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#b4c7dc", "style": "ce4", "value": "a"},
                        {"bgcolor": "#b4c7dc", "style": "ce4", "value": "b"},
                        {"bgcolor": "#ffff6d", "style": "ce11", "value": "c"},
                        {"bgcolor": "#ff3838", "style": "ce10", "value": "d"},
                        {"bgcolor": "#b4c7dc", "style": "ce4", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#b4c7dc", "style": "ce4", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ed4c05", "style": "ce5", "value": "e"},
                        {"bgcolor": "#ed4c05", "style": "ce5", "value": "f"},
                        {"bgcolor": "#ed4c05", "style": "ce5", "value": None},
                        {"bgcolor": "#ed4c05", "style": "ce5", "value": None},
                        {"bgcolor": "#ed4c05", "style": "ce5", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ed4c05", "style": "ce5", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#168253", "style": "ce6", "value": None},
                        {"bgcolor": "#168253", "style": "ce6", "value": None},
                        {"bgcolor": "#168253", "style": "ce6", "value": None},
                        {"bgcolor": "#168253", "style": "ce6", "value": None},
                        {"bgcolor": "#168253", "style": "ce6", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#168253", "style": "ce6", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#fff5ce", "style": "ce13", "value": "x"},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#55215b", "style": "ce7", "value": None},
                        {"bgcolor": "#55215b", "style": "ce7", "value": None},
                        {"bgcolor": "#55215b", "style": "ce7", "value": None},
                        {"bgcolor": "#55215b", "style": "ce7", "value": None},
                        {"bgcolor": "#55215b", "style": "ce7", "value": None},
                        {"bgcolor": "#55215b", "style": "ce14", "value": None},
                        {"bgcolor": "#55215b", "style": "ce7", "value": None},
                    ],
                    "style": "ro1",
                },
                {
                    "row": [
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                        {"bgcolor": "#e6e905", "value": None},
                        {"bgcolor": "#ffffff", "value": None},
                    ],
                    "style": "ro1",
                },
            ],
            "width": [
                "2.258cm",
                "2.258cm",
                "2.258cm",
                "2.258cm",
                "2.258cm",
                "2.258cm",
                "2.258cm",
            ],
        }
    ]

    assert body == expected


def test_content_keep_colors_minimal():
    body = parser.ods_to_python(
        FILE_COLS,
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
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffff00", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": "r"},
                    {"bgcolor": "#55308d", "value": None},
                    {"bgcolor": "#ff3838", "value": None},
                    {"bgcolor": "#ff3838", "value": None},
                    {"bgcolor": "#ff3838", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": "s"},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#3465a4", "value": None},
                    {"bgcolor": "#3465a4", "value": None},
                    {"bgcolor": "#3465a4", "value": None},
                    {"bgcolor": "#3465a4", "value": None},
                    {"bgcolor": "#3465a4", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#3465a4", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#b4c7dc", "value": "a"},
                    {"bgcolor": "#b4c7dc", "value": "b"},
                    {"bgcolor": "#ffff6d", "value": "c"},
                    {"bgcolor": "#ff3838", "value": "d"},
                    {"bgcolor": "#b4c7dc", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#b4c7dc", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#ed4c05", "value": "e"},
                    {"bgcolor": "#ed4c05", "value": "f"},
                    {"bgcolor": "#ed4c05", "value": None},
                    {"bgcolor": "#ed4c05", "value": None},
                    {"bgcolor": "#ed4c05", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ed4c05", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#168253", "value": None},
                    {"bgcolor": "#168253", "value": None},
                    {"bgcolor": "#168253", "value": None},
                    {"bgcolor": "#168253", "value": None},
                    {"bgcolor": "#168253", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#168253", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#fff5ce", "value": "x"},
                    {"bgcolor": "#ffffff", "value": None},
                ],
                [
                    {"bgcolor": "#55215b", "value": None},
                    {"bgcolor": "#55215b", "value": None},
                    {"bgcolor": "#55215b", "value": None},
                    {"bgcolor": "#55215b", "value": None},
                    {"bgcolor": "#55215b", "value": None},
                    {"bgcolor": "#55215b", "value": None},
                    {"bgcolor": "#55215b", "value": None},
                ],
                [
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                    {"bgcolor": "#e6e905", "value": None},
                    {"bgcolor": "#ffffff", "value": None},
                ],
            ],
        }
    ]

    assert body == expected
