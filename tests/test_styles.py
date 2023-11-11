import json
from pathlib import Path

import odsparsator.odsparsator as parser

DATA = Path(__file__).parent / "data"
FILE_STYLES = DATA / "styles.ods"
FILE_RESULT = DATA / "result_styles.json"
FILE_RESULT_M = DATA / "result_styles_m.json"


def canonical(dict_item):
    if "styles" in dict_item:
        tmp = sorted([(s["definition"], s.get("name")) for s in dict_item["styles"]])
        dict_item["styles"] = tmp
    return json.dumps(dict_item, sort_keys=True, indent=4, ensure_ascii=False)


def test_json_content():
    content = parser.ods_to_python(FILE_STYLES)
    expected = json.loads(FILE_RESULT.read_text(encoding="utf8"))
    assert canonical(content) == canonical(expected)


def test_json_content_min():
    content = parser.ods_to_python(FILE_STYLES, export_minimal=True)
    expected = json.loads(FILE_RESULT_M.read_text(encoding="utf8"))
    assert canonical(content) == canonical(expected)
