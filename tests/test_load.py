import json
from pathlib import Path

import odsparsator.odsparsator as parser

DATA = Path(__file__).parent / "data"
FILE_FORMULA = DATA / "formula.ods"
FILE_JSON = DATA / "json.ods"
FILE_MINIMAL = DATA / "minimal.ods"
FILE_USE_CASE = DATA / "use_case.ods"
FILE_RESULT = DATA / "result_formula.json"
FILE_RESULT_M = DATA / "result_formula_m.json"
FILES = (FILE_FORMULA, FILE_JSON, FILE_MINIMAL, FILE_USE_CASE)


def test_run(tmp_path):
    for file in FILES:
        output = tmp_path / (file.stem + "1.json")
        parser.ods_to_json(file, output)
        assert output.is_file()


def test_run_min(tmp_path):
    for file in FILES:
        output = tmp_path / (file.stem + "2.json")
        parser.ods_to_json(file, output, True)
        assert output.is_file()


def test_run_min_styles(tmp_path):
    for file in FILES:
        output = tmp_path / (file.stem + "3.json")
        parser.ods_to_json(file, output, True)
        assert output.is_file()


def test_run_styles(tmp_path):
    for file in FILES:
        output = tmp_path / (file.stem + "4.json")
        parser.ods_to_json(file, output, False, True)
        assert output.is_file()


def test_load_json(tmp_path):
    for file in FILES:
        output = tmp_path / (file.stem + "5.json")
        parser.ods_to_json(file, output)
        with open(output, encoding="utf8") as rfile:
            content = json.load(rfile)
        assert isinstance(content, dict)
        assert isinstance(content["body"], list)
