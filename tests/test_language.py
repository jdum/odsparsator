import json
import subprocess
from pathlib import Path

from odfdo import Document

import odsparsator.odsparsator as parser

DATA = Path(__file__).parent / "data"
FILE_MINIMAL = DATA / "minimal.ods"


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out.strip(), err.strip(), proc.returncode


def test_language_default():
    p = parser.ODSParsator()
    p.parse_document(FILE_MINIMAL)
    assert p.language == "fr-FR"
    assert p.content["language"] == "fr-FR"


def test_language_custom(tmp_path):
    doc_path = tmp_path / "custom_lang.ods"
    doc = Document("spreadsheet")
    doc.language = "en-US"
    doc.save(doc_path)

    p = parser.ODSParsator()
    p.parse_document(doc_path)
    assert p.language == "en-US"
    assert p.content["language"] == "en-US"


def test_language_ods_to_python(tmp_path):
    doc_path = tmp_path / "custom_lang.ods"
    doc = Document("spreadsheet")
    doc.language = "de-DE"
    doc.save(doc_path)

    content = parser.ods_to_python(doc_path)
    assert content["language"] == "de-DE"


def test_language_ods_to_json(tmp_path):
    doc_path = tmp_path / "custom_lang.ods"
    json_path = tmp_path / "output.json"
    doc = Document("spreadsheet")
    doc.language = "es-ES"
    doc.save(doc_path)

    parser.ods_to_json(doc_path, json_path)
    data = json.loads(json_path.read_text(encoding="utf8"))
    assert data["language"] == "es-ES"


def test_language_minimal_no_lang():
    content = parser.ods_to_python(FILE_MINIMAL, export_minimal=True)
    assert "language" not in content
    assert "body" in content


def test_cli_language(tmp_path):
    doc_path = tmp_path / "doc_en.ods"
    json_path = tmp_path / "doc_en.json"
    doc = Document("spreadsheet")
    doc.language = "en-GB"
    doc.save(doc_path)

    command = ["odsparsator", str(doc_path), str(json_path)]
    _out, err, exitcode = capture(command)
    assert exitcode == 0
    assert err == b""
    data = json.loads(json_path.read_text(encoding="utf8"))
    assert data["language"] == "en-GB"


def test_language_none():
    p = parser.ODSParsator()
    p.parse_document(FILE_MINIMAL)
    p.language = None
    assert "language" not in p.content
