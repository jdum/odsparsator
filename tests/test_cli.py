import json
import re
import shlex
import subprocess
from pathlib import Path

from odsparsator.cli import check_odfdo_version

RE_VERS = re.compile(r' *version *= *"(\S+)"$')
DATA = Path(__file__).parent / "data"
FILE_MINIMAL = DATA / "minimal.ods"


def read_proj_version():
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject) as content:
        for line in content:
            if group := RE_VERS.match(line):
                return group[1]
    raise ValueError


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out.strip(), err.strip(), proc.returncode


def test_odfdo_version():
    assert check_odfdo_version()


def test_no_param():
    command = ["odsparsator"]
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b""
    assert err.startswith(b"usage: odsparsator [-h] [--version]")


def test_version():
    command = ["odsparsator", "--version"]
    out, err, exitcode = capture(command)
    assert exitcode == 0
    expected = f"odsparsator {read_proj_version()}".encode()
    assert out == expected
    assert err == b""


def test_help():
    command = ["odsparsator", "--help"]
    out, err, exitcode = capture(command)
    assert exitcode == 0
    assert err == b""
    assert b"Generate a json file from an OpenDocument Format" in out
    assert b"The resulting data follow the format of" in out


def test_generate(tmp_path):
    dest = tmp_path / "minimal.json"
    dest.unlink(missing_ok=True)
    command = ["odsparsator", "-m", str(FILE_MINIMAL), str(dest)]
    out, err, exitcode = capture(command)
    assert exitcode == 0
    assert err == b""
    assert out == b""
    assert dest.is_file()
    content = json.loads(dest.read_text(encoding="utf8"))
    assert "body" in content
    assert len(content["body"]) == 2


def test_generate_keep(tmp_path):
    dest = tmp_path / "minimal.json"
    dest.unlink(missing_ok=True)
    command = shlex.split(f"odsparsator -m -k {FILE_MINIMAL} {dest}")
    out, err, exitcode = capture(command)
    assert exitcode == 0
    assert err == b""
    assert out == b""
    assert dest.is_file()
    content = json.loads(dest.read_text(encoding="utf8"))
    assert "body" in content
    assert len(content["body"]) == 2


def test_generate_keep_color(tmp_path):
    dest = tmp_path / "minimal.json"
    dest.unlink(missing_ok=True)
    command = shlex.split(f"odsparsator -m -k -c {FILE_MINIMAL} {dest}")
    out, err, exitcode = capture(command)
    assert exitcode == 0
    assert err == b""
    assert out == b""
    assert dest.is_file()
    content = json.loads(dest.read_text(encoding="utf8"))
    assert "body" in content
    assert len(content["body"]) == 2
