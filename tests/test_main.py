import pytest

import odsparsator.odsparsator as parser


def test_no_args_odsparsator():
    with pytest.raises(TypeError):
        parser.ods_to_json()


def test_one_args_odsparsator():
    with pytest.raises(TypeError):
        parser.ods_to_json()("some file")


def test_bad_args_odsparsator():
    with pytest.raises(TypeError):
        parser.ods_to_json()("some file", "output", "badarg")
