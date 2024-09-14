import json
from pathlib import Path

import odsparsator.odsparsator as parser

DATA = Path(__file__).parent / "data"
FILE_HIDDEN_ODS = DATA / "minimal_hidden.ods"
FILE_RESULT_HIDDEN = DATA / "minimal_hidden.json"
FILE_RESULT_NO_HIDDEN = DATA / "minimal_no_hidden.json"


def canonical(dict_item):
    if "styles" in dict_item:
        tmp = sorted([(s["definition"], s.get("name")) for s in dict_item["styles"]])
        dict_item["styles"] = tmp
    return json.dumps(dict_item, sort_keys=True, indent=4, ensure_ascii=False)


def test_no_hidden_content():
    content = parser.ods_to_python(FILE_HIDDEN_ODS)
    expected = json.loads(FILE_RESULT_NO_HIDDEN.read_text(encoding="utf8"))
    assert canonical(content) == canonical(expected)


def test_hidden_content():
    content = parser.ods_to_python(FILE_HIDDEN_ODS, see_hidden=True)
    expected = json.loads(FILE_RESULT_HIDDEN.read_text(encoding="utf8"))
    assert canonical(content) == canonical(expected)
