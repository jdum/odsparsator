from pathlib import Path

import odsparsator.odsparsator as parser

DATA = Path(__file__).parent / "data"
FILE_MINIMAL = DATA / "minimal.ods"
CACHE = {}


def body():
    if "body" not in CACHE:
        CACHE["body"] = parser.ods_to_python(FILE_MINIMAL)["body"]
    return CACHE["body"]


def body_min():
    if "body_min" not in CACHE:
        CACHE["body_min"] = parser.ods_to_python(FILE_MINIMAL, export_minimal=True)[
            "body"
        ]
    return CACHE["body_min"]


def test_nb_tables():
    assert len(body()) == 2


def test_nb_tables_min():
    assert len(body_min()) == 2


def test_t0_name():
    table = body()[0]
    assert table["name"] == "Tab 1"


def test_t0m_name():
    t = body_min()[0]
    assert t["name"] == "Tab 1"


def test_t1_name():
    t = body()[1]
    assert t["name"] == "Tab 2"


def test_t1m_name():
    t = body_min()[1]
    assert t["name"] == "Tab 2"


def test_t0_rows():
    t = body()[0]
    rows = t["table"]
    assert len(rows) == 4


def test_t0m_rows():
    t = body_min()[0]
    rows = t["table"]
    assert len(rows) == 4


def test_t1_rows():
    t = body()[1]
    rows = t["table"]
    assert len(rows) == 4


def test_t1m_rows():
    t = body_min()[1]
    rows = t["table"]
    assert len(rows) == 4


######################################
# t0 row 0
######################################
def test_t0_r0_dict():
    t = body()[0]
    row = t["table"][0]
    assert isinstance(row, dict)


def test_t0_r0_krow():
    t = body()[0]
    row = t["table"][0]
    assert isinstance(row["row"], list)


def test_t0m_r0_list():
    t = body_min()[0]
    row = t["table"][0]
    assert isinstance(row, list)


def test_t0_r0_len():
    t = body()[0]
    row = t["table"][0]
    assert len(row["row"]) == 10


def test_t0m_r0_len():
    t = body_min()[0]
    row = t["table"][0]
    assert len(row) == 10


def test_t0_r0_row_values_type():
    t = body()[0]
    row = t["table"][0]
    for i in range(10):
        assert isinstance(row["row"][i], dict)


def test_t0m_r0_row_values_type():
    t = body_min()[0]
    row = t["table"][0]
    for i in range(10):
        assert isinstance(row[i], str)


def test_t0_r0_cell_dict():
    t = body()[0]
    row = t["table"][0]
    for i in range(10):
        assert isinstance(row["row"][i]["value"], str)


def test_t0_r0_cell_dict_st():
    t = body()[0]
    row = t["table"][0]
    for i in range(10):
        assert isinstance(row["row"][i]["style"], str)


def test_t0_r0_cell_values():
    t = body()[0]
    row = t["table"][0]
    values = [row["row"][i]["value"] for i in range(10)]
    assert values == ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]


def test_t0_r0_cell_styles():
    t = body()[0]
    row = t["table"][0]
    styles = [row["row"][i]["style"] for i in range(10)]
    assert styles == ["left"] * 10


def test_t0m_r0_row_values():
    t = body_min()[0]
    row = t["table"][0]
    assert row == ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]


def test_t0_r0_row_style():
    t = body()[0]
    row = t["table"][0]
    assert row["style"] == "default_table_row"


######################################
# t0 row 1
######################################
def test_t0_r1_dict():
    t = body()[0]
    row = t["table"][1]
    assert isinstance(row, dict)


def test_t0_r1_krow():
    t = body()[0]
    row = t["table"][1]
    assert isinstance(row["row"], list)


def test_t0m_r1_list():
    t = body_min()[0]
    row = t["table"][1]
    assert isinstance(row, list)


def test_t0_r1_len():
    t = body()[0]
    row = t["table"][1]
    assert len(row["row"]) == 10


def test_t0m_r1_len():
    t = body_min()[0]
    row = t["table"][1]
    assert len(row) == 10


def test_t0_r1_row_values_type():
    t = body()[0]
    row = t["table"][1]
    for i in range(10):
        assert isinstance(row["row"][i], dict)


def test_t0m_r1_row_values_type():
    t = body_min()[0]
    row = t["table"][1]
    for i in range(10):
        assert isinstance(row[i], int)


def test_t0_r1_cell_dict():
    t = body()[0]
    row = t["table"][1]
    for i in range(10):
        assert isinstance(row["row"][i]["value"], int)


def test_t0_r1_cell_dict_st():
    t = body()[0]
    row = t["table"][1]
    for i in range(10):
        assert isinstance(row["row"][i]["style"], str)


def test_t0_r1_cell_values():
    t = body()[0]
    row = t["table"][1]
    values = [row["row"][i]["value"] for i in range(10)]
    assert values == [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]


def test_t0_r1_cell_styles():
    t = body()[0]
    row = t["table"][1]
    styles = [row["row"][i]["style"] for i in range(10)]
    assert styles == ["right"] * 10


def test_t0m_r1_row_values():
    t = body_min()[0]
    row = t["table"][1]
    assert row == [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]


def test_t0_r1_row_style():
    t = body()[0]
    row = t["table"][1]
    assert row["style"] == "default_table_row"


######################################
# t0 row 2
######################################
def test_t0_r2_dict():
    t = body()[0]
    row = t["table"][2]
    assert isinstance(row, dict)


def test_t0_r2_krow():
    t = body()[0]
    row = t["table"][2]
    assert isinstance(row["row"], list)


def test_t0m_r2_list():
    t = body_min()[0]
    row = t["table"][2]
    assert isinstance(row, list)


def test_t0_r2_len():
    t = body()[0]
    row = t["table"][2]
    assert len(row["row"]) == 10


def test_t0m_r2_len():
    t = body_min()[0]
    row = t["table"][2]
    assert len(row) == 10


def test_t0_r2_row_values_type():
    t = body()[0]
    row = t["table"][2]
    for i in range(10):
        assert isinstance(row["row"][i], dict)


def test_t0m_r2_row_values_type():
    t = body_min()[0]
    row = t["table"][2]
    for i in range(10):
        assert isinstance(row[i], int)


def test_t0_r2_cell_dict():
    t = body()[0]
    row = t["table"][2]
    for i in range(10):
        assert isinstance(row["row"][i]["value"], int)


def test_t0_r2_cell_dict_st():
    t = body()[0]
    row = t["table"][2]
    for i in range(10):
        assert isinstance(row["row"][i]["style"], str)


def test_t0_r2_cell_values():
    t = body()[0]
    row = t["table"][2]
    values = [row["row"][i]["value"] for i in range(10)]
    assert values == [1, 11, 21, 31, 41, 51, 61, 71, 81, 91]


def test_t0_r2_cell_styles():
    t = body()[0]
    row = t["table"][2]
    styles = [row["row"][i]["style"] for i in range(10)]
    assert styles == ["right"] * 10


def test_t0m_r2_row_values():
    t = body_min()[0]
    row = t["table"][2]
    assert row == [1, 11, 21, 31, 41, 51, 61, 71, 81, 91]


def test_t0_r2_row_style():
    t = body()[0]
    row = t["table"][2]
    assert row["style"] == "default_table_row"


######################################
# t1 row 0
######################################
def test_t1_r0_dict():
    t = body()[1]
    row = t["table"][0]
    assert isinstance(row, dict)


def test_t1_r0_krow():
    t = body()[1]
    row = t["table"][0]
    assert isinstance(row["row"], list)


def test_t1m_r0_list():
    t = body_min()[1]
    row = t["table"][0]
    assert isinstance(row, list)


def test_t1_r0_len():
    t = body()[1]
    row = t["table"][0]
    assert len(row["row"]) == 10


def test_t1m_r0_len():
    t = body_min()[1]
    row = t["table"][0]
    assert len(row) == 10


def test_t1_r0_row_values_type():
    t = body()[1]
    row = t["table"][0]
    for i in range(10):
        assert isinstance(row["row"][i], dict)


def test_t1m_r0_row_values_type():
    t = body_min()[1]
    row = t["table"][0]
    for i in range(10):
        assert isinstance(row[i], str)


def test_t1_r0_cell_dict():
    t = body()[1]
    row = t["table"][0]
    for i in range(10):
        assert isinstance(row["row"][i]["value"], str)


def test_t1_r0_cell_dict_st():
    t = body()[1]
    row = t["table"][0]
    for i in range(10):
        assert isinstance(row["row"][i]["style"], str)


def test_t1_r0_cell_values():
    t = body()[1]
    row = t["table"][0]
    values = [row["row"][i]["value"] for i in range(10)]
    assert values == ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]


def test_t1_r0_cell_styles():
    t = body()[1]
    row = t["table"][0]
    styles = [row["row"][i]["style"] for i in range(10)]
    assert styles == ["left"] * 10


def test_t1m_r0_row_values():
    t = body_min()[1]
    row = t["table"][0]
    assert row == ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]


def test_t1_r0_row_style():
    t = body()[1]
    row = t["table"][0]
    assert row["style"] == "default_table_row"


######################################
# t1 row 1
######################################
def test_t1_r1_dict():
    t = body()[1]
    row = t["table"][1]
    assert isinstance(row, dict)


def test_t1_r1_krow():
    t = body()[1]
    row = t["table"][1]
    assert isinstance(row["row"], list)


def test_t1m_r1_list():
    t = body_min()[1]
    row = t["table"][1]
    assert isinstance(row, list)


def test_t1_r1_len():
    t = body()[1]
    row = t["table"][1]
    assert len(row["row"]) == 10


def test_t1m_r1_len():
    t = body_min()[1]
    row = t["table"][1]
    assert len(row) == 10


def test_t1_r1_row_values_type():
    t = body()[1]
    row = t["table"][1]
    for i in range(10):
        assert isinstance(row["row"][i], dict)


def test_t1m_r1_row_values_type():
    t = body_min()[1]
    row = t["table"][1]
    for i in range(10):
        assert isinstance(row[i], int)


def test_t1_r1_cell_dict():
    t = body()[1]
    row = t["table"][1]
    for i in range(10):
        assert isinstance(row["row"][i]["value"], int)


def test_t1_r1_cell_dict_st():
    t = body()[1]
    row = t["table"][1]
    for i in range(10):
        assert isinstance(row["row"][i]["style"], str)


def test_t1_r1_cell_values():
    t = body()[1]
    row = t["table"][1]
    values = [row["row"][i]["value"] for i in range(10)]
    assert values == [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]


def test_t1_r1_cell_styles():
    t = body()[1]
    row = t["table"][1]
    styles = [row["row"][i]["style"] for i in range(10)]
    assert styles == ["right"] * 10


def test_t1m_r1_row_values():
    t = body_min()[1]
    row = t["table"][1]
    assert row == [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]


def test_t1_r1_row_style():
    t = body()[1]
    row = t["table"][1]
    assert row["style"] == "default_table_row"


######################################
# t1 row 2
######################################
def test_t1_r2_dict():
    t = body()[1]
    row = t["table"][2]
    assert isinstance(row, dict)


def test_t1_r2_krow():
    t = body()[1]
    row = t["table"][2]
    assert isinstance(row["row"], list)


def test_t1m_r2_list():
    t = body_min()[1]
    row = t["table"][2]
    assert isinstance(row, list)


def test_t1_r2_len():
    t = body()[1]
    row = t["table"][2]
    assert len(row["row"]) == 10


def test_t1m_r2_len():
    t = body_min()[1]
    row = t["table"][2]
    assert len(row) == 10


def test_t1_r2_row_values_type():
    t = body()[1]
    row = t["table"][2]
    for i in range(10):
        assert isinstance(row["row"][i], dict)


def test_t1m_r2_row_values_type():
    t = body_min()[1]
    row = t["table"][2]
    for i in range(10):
        assert isinstance(row[i], int)


def test_t1_r2_cell_dict():
    t = body()[1]
    row = t["table"][2]
    for i in range(10):
        assert isinstance(row["row"][i]["value"], int)


def test_t1_r2_cell_dict_st():
    t = body()[1]
    row = t["table"][2]
    for i in range(10):
        assert isinstance(row["row"][i]["style"], str)


def test_t1_r2_cell_values():
    t = body()[1]
    row = t["table"][2]
    values = [row["row"][i]["value"] for i in range(10)]
    assert values == [101, 111, 121, 131, 141, 151, 161, 171, 181, 191]


def test_t1_r2_cell_styles():
    t = body()[1]
    row = t["table"][2]
    styles = [row["row"][i]["style"] for i in range(10)]
    assert styles == ["right"] * 10


def test_t1m_r2_row_values():
    t = body_min()[1]
    row = t["table"][2]
    assert row == [101, 111, 121, 131, 141, 151, 161, 171, 181, 191]


def test_t1_r2_row_style():
    t = body()[1]
    row = t["table"][2]
    assert row["style"] == "default_table_row"
