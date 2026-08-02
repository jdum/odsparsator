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
    if "default_styles" in dict_item:
        tmp = sorted([s["definition"] for s in dict_item["default_styles"]])
        dict_item["default_styles"] = tmp
    if "common_styles" in dict_item:
        tmp = sorted(
            [(s["definition"], s.get("name")) for s in dict_item["common_styles"]]
        )
        dict_item["common_styles"] = tmp
    return json.dumps(dict_item, sort_keys=True, indent=4, ensure_ascii=False)


def test_json_content():
    content = parser.ods_to_python(FILE_STYLES)
    expected = json.loads(FILE_RESULT.read_text(encoding="utf8"))
    assert canonical(content) == canonical(expected)


def test_json_content_min():
    content = parser.ods_to_python(FILE_STYLES, export_minimal=True)
    expected = json.loads(FILE_RESULT_M.read_text(encoding="utf8"))
    assert canonical(content) == canonical(expected)


def test_default_styles():
    content = parser.ods_to_python(FILE_STYLES)
    assert "default_styles" in content
    assert isinstance(content["default_styles"], list)
    assert len(content["default_styles"]) > 0
    assert "definition" in content["default_styles"][0]
    assert "<style:default-style" in content["default_styles"][0]["definition"]


def test_common_styles():
    content = parser.ods_to_python(FILE_STYLES)
    assert "common_styles" in content
    assert isinstance(content["common_styles"], list)
    assert len(content["common_styles"]) > 0
    assert "name" in content["common_styles"][0]
    assert "definition" in content["common_styles"][0]
