import json
from pathlib import Path

import odsparsator.odsparsator as parser

DATA = Path(__file__).parent / "data"
FILE_BLUE = DATA / "col_cell_blue.ods"
FILE_RESULT = DATA / "result_col_cell_blue_kcm.json"


def canonical(dict_item):
    if "styles" in dict_item:
        tmp = sorted([(s["definition"], s.get("name")) for s in dict_item["styles"]])
        dict_item["styles"] = tmp
    return json.dumps(dict_item, sort_keys=True, indent=4, ensure_ascii=False)


def test_blue_content_keep_colors_minimal_json():
    content = parser.ods_to_python(
        FILE_BLUE,
        keep_styled=True,
        colors=True,
        export_minimal=True,
    )
    expected = json.loads(FILE_RESULT.read_text(encoding="utf8"))

    assert content == expected
