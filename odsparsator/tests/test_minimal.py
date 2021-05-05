#!/usr/bin/env python

from unittest import TestCase, main

import os
import json
import odsparsator.odsparsator as p


class TestFileMinimal(TestCase):
    def setUp(self):
        fname = "test_minimal"
        self.output = fname + ".json"
        self.output_min = fname + "_min.json"
        if os.path.isfile(self.output):
            os.remove(self.output)
        if os.path.isfile(self.output_min):
            os.remove(self.output_min)
        p.ods_to_json(fname + ".ods", self.output)
        p.ods_to_json(fname + ".ods", self.output_min, True)
        with open(self.output, "r", encoding="utf-8") as r:
            self.content = json.load(r)
        with open(self.output_min, "r", encoding="utf-8") as r:
            self.content_min = json.load(r)
        self.body = self.content["body"]
        self.body_min = self.content_min["body"]

    def tearDown(self):
        try:
            os.remove(self.output)
        except IOError:
            pass
        try:
            os.remove(self.output_min)
        except IOError:
            pass

    def test_nb_tables(self):
        self.assertEqual(len(self.body), 2)

    def test_nb_tables_min(self):
        self.assertEqual(len(self.body_min), 2)

    def test_t0_name(self):
        t = self.body[0]
        self.assertEqual(t["name"], "Tab 1")

    def test_t0m_name(self):
        t = self.body_min[0]
        self.assertEqual(t["name"], "Tab 1")

    def test_t1_name(self):
        t = self.body[1]
        self.assertEqual(t["name"], "Tab 2")

    def test_t1m_name(self):
        t = self.body_min[1]
        self.assertEqual(t["name"], "Tab 2")

    def test_t0_rows(self):
        t = self.body[0]
        rows = t["table"]
        self.assertEqual(len(rows), 4)

    def test_t0m_rows(self):
        t = self.body_min[0]
        rows = t["table"]
        self.assertEqual(len(rows), 4)

    def test_t1_rows(self):
        t = self.body[1]
        rows = t["table"]
        self.assertEqual(len(rows), 4)

    def test_t1m_rows(self):
        t = self.body_min[1]
        rows = t["table"]
        self.assertEqual(len(rows), 4)

    ######################################
    # t0 row 0
    ######################################
    def test_t0_r0_dict(self):
        t = self.body[0]
        row = t["table"][0]
        self.assertIsInstance(row, dict)

    def test_t0_r0_krow(self):
        t = self.body[0]
        row = t["table"][0]
        self.assertIsInstance(row["row"], list)

    def test_t0m_r0_list(self):
        t = self.body_min[0]
        row = t["table"][0]
        self.assertIsInstance(row, list)

    def test_t0_r0_len(self):
        t = self.body[0]
        row = t["table"][0]
        self.assertEqual(len(row["row"]), 10)

    def test_t0m_r0_len(self):
        t = self.body_min[0]
        row = t["table"][0]
        self.assertEqual(len(row), 10)

    def test_t0_r0_row_values_type(self):
        t = self.body[0]
        row = t["table"][0]
        for i in range(10):
            self.assertIsInstance(row["row"][i], dict)

    def test_t0m_r0_row_values_type(self):
        t = self.body_min[0]
        row = t["table"][0]
        for i in range(10):
            self.assertIsInstance(row[i], str)

    def test_t0_r0_cell_dict(self):
        t = self.body[0]
        row = t["table"][0]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["value"], str)

    def test_t0_r0_cell_dict_st(self):
        t = self.body[0]
        row = t["table"][0]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["style"], str)

    def test_t0_r0_cell_values(self):
        t = self.body[0]
        row = t["table"][0]
        values = [row["row"][i]["value"] for i in range(10)]
        self.assertEqual(values, ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])

    def test_t0_r0_cell_styles(self):
        t = self.body[0]
        row = t["table"][0]
        styles = [row["row"][i]["style"] for i in range(10)]
        self.assertEqual(styles, ["left"] * 10)

    def test_t0m_r0_row_values(self):
        t = self.body_min[0]
        row = t["table"][0]
        self.assertEqual(row, ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])

    def test_t0_r0_row_style(self):
        t = self.body[0]
        row = t["table"][0]
        self.assertEqual(row["style"], "default_table_row")

    ######################################
    # t0 row 1
    ######################################
    def test_t0_r1_dict(self):
        t = self.body[0]
        row = t["table"][1]
        self.assertIsInstance(row, dict)

    def test_t0_r1_krow(self):
        t = self.body[0]
        row = t["table"][1]
        self.assertIsInstance(row["row"], list)

    def test_t0m_r1_list(self):
        t = self.body_min[0]
        row = t["table"][1]
        self.assertIsInstance(row, list)

    def test_t0_r1_len(self):
        t = self.body[0]
        row = t["table"][1]
        self.assertEqual(len(row["row"]), 10)

    def test_t0m_r1_len(self):
        t = self.body_min[0]
        row = t["table"][1]
        self.assertEqual(len(row), 10)

    def test_t0_r1_row_values_type(self):
        t = self.body[0]
        row = t["table"][1]
        for i in range(10):
            self.assertIsInstance(row["row"][i], dict)

    def test_t0m_r1_row_values_type(self):
        t = self.body_min[0]
        row = t["table"][1]
        for i in range(10):
            self.assertIsInstance(row[i], int)

    def test_t0_r1_cell_dict(self):
        t = self.body[0]
        row = t["table"][1]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["value"], int)

    def test_t0_r1_cell_dict_st(self):
        t = self.body[0]
        row = t["table"][1]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["style"], str)

    def test_t0_r1_cell_values(self):
        t = self.body[0]
        row = t["table"][1]
        values = [row["row"][i]["value"] for i in range(10)]
        self.assertEqual(values, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90])

    def test_t0_r1_cell_styles(self):
        t = self.body[0]
        row = t["table"][1]
        styles = [row["row"][i]["style"] for i in range(10)]
        self.assertEqual(styles, ["right"] * 10)

    def test_t0m_r1_row_values(self):
        t = self.body_min[0]
        row = t["table"][1]
        self.assertEqual(row, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90])

    def test_t0_r1_row_style(self):
        t = self.body[0]
        row = t["table"][1]
        self.assertEqual(row["style"], "default_table_row")

    ######################################
    # t0 row 2
    ######################################
    def test_t0_r2_dict(self):
        t = self.body[0]
        row = t["table"][2]
        self.assertIsInstance(row, dict)

    def test_t0_r2_krow(self):
        t = self.body[0]
        row = t["table"][2]
        self.assertIsInstance(row["row"], list)

    def test_t0m_r2_list(self):
        t = self.body_min[0]
        row = t["table"][2]
        self.assertIsInstance(row, list)

    def test_t0_r2_len(self):
        t = self.body[0]
        row = t["table"][2]
        self.assertEqual(len(row["row"]), 10)

    def test_t0m_r2_len(self):
        t = self.body_min[0]
        row = t["table"][2]
        self.assertEqual(len(row), 10)

    def test_t0_r2_row_values_type(self):
        t = self.body[0]
        row = t["table"][2]
        for i in range(10):
            self.assertIsInstance(row["row"][i], dict)

    def test_t0m_r2_row_values_type(self):
        t = self.body_min[0]
        row = t["table"][2]
        for i in range(10):
            self.assertIsInstance(row[i], int)

    def test_t0_r2_cell_dict(self):
        t = self.body[0]
        row = t["table"][2]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["value"], int)

    def test_t0_r2_cell_dict_st(self):
        t = self.body[0]
        row = t["table"][2]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["style"], str)

    def test_t0_r2_cell_values(self):
        t = self.body[0]
        row = t["table"][2]
        values = [row["row"][i]["value"] for i in range(10)]
        self.assertEqual(values, [1, 11, 21, 31, 41, 51, 61, 71, 81, 91])

    def test_t0_r2_cell_styles(self):
        t = self.body[0]
        row = t["table"][2]
        styles = [row["row"][i]["style"] for i in range(10)]
        self.assertEqual(styles, ["right"] * 10)

    def test_t0m_r2_row_values(self):
        t = self.body_min[0]
        row = t["table"][2]
        self.assertEqual(row, [1, 11, 21, 31, 41, 51, 61, 71, 81, 91])

    def test_t0_r2_row_style(self):
        t = self.body[0]
        row = t["table"][2]
        self.assertEqual(row["style"], "default_table_row")

    ######################################
    # t1 row 0
    ######################################
    def test_t1_r0_dict(self):
        t = self.body[1]
        row = t["table"][0]
        self.assertIsInstance(row, dict)

    def test_t1_r0_krow(self):
        t = self.body[1]
        row = t["table"][0]
        self.assertIsInstance(row["row"], list)

    def test_t1m_r0_list(self):
        t = self.body_min[1]
        row = t["table"][0]
        self.assertIsInstance(row, list)

    def test_t1_r0_len(self):
        t = self.body[1]
        row = t["table"][0]
        self.assertEqual(len(row["row"]), 10)

    def test_t1m_r0_len(self):
        t = self.body_min[1]
        row = t["table"][0]
        self.assertEqual(len(row), 10)

    def test_t1_r0_row_values_type(self):
        t = self.body[1]
        row = t["table"][0]
        for i in range(10):
            self.assertIsInstance(row["row"][i], dict)

    def test_t1m_r0_row_values_type(self):
        t = self.body_min[1]
        row = t["table"][0]
        for i in range(10):
            self.assertIsInstance(row[i], str)

    def test_t1_r0_cell_dict(self):
        t = self.body[1]
        row = t["table"][0]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["value"], str)

    def test_t1_r0_cell_dict_st(self):
        t = self.body[1]
        row = t["table"][0]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["style"], str)

    def test_t1_r0_cell_values(self):
        t = self.body[1]
        row = t["table"][0]
        values = [row["row"][i]["value"] for i in range(10)]
        self.assertEqual(values, ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])

    def test_t1_r0_cell_styles(self):
        t = self.body[1]
        row = t["table"][0]
        styles = [row["row"][i]["style"] for i in range(10)]
        self.assertEqual(styles, ["left"] * 10)

    def test_t1m_r0_row_values(self):
        t = self.body_min[1]
        row = t["table"][0]
        self.assertEqual(row, ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])

    def test_t1_r0_row_style(self):
        t = self.body[1]
        row = t["table"][0]
        self.assertEqual(row["style"], "default_table_row")

    ######################################
    # t1 row 1
    ######################################
    def test_t1_r1_dict(self):
        t = self.body[1]
        row = t["table"][1]
        self.assertIsInstance(row, dict)

    def test_t1_r1_krow(self):
        t = self.body[1]
        row = t["table"][1]
        self.assertIsInstance(row["row"], list)

    def test_t1m_r1_list(self):
        t = self.body_min[1]
        row = t["table"][1]
        self.assertIsInstance(row, list)

    def test_t1_r1_len(self):
        t = self.body[1]
        row = t["table"][1]
        self.assertEqual(len(row["row"]), 10)

    def test_t1m_r1_len(self):
        t = self.body_min[1]
        row = t["table"][1]
        self.assertEqual(len(row), 10)

    def test_t1_r1_row_values_type(self):
        t = self.body[1]
        row = t["table"][1]
        for i in range(10):
            self.assertIsInstance(row["row"][i], dict)

    def test_t1m_r1_row_values_type(self):
        t = self.body_min[1]
        row = t["table"][1]
        for i in range(10):
            self.assertIsInstance(row[i], int)

    def test_t1_r1_cell_dict(self):
        t = self.body[1]
        row = t["table"][1]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["value"], int)

    def test_t1_r1_cell_dict_st(self):
        t = self.body[1]
        row = t["table"][1]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["style"], str)

    def test_t1_r1_cell_values(self):
        t = self.body[1]
        row = t["table"][1]
        values = [row["row"][i]["value"] for i in range(10)]
        self.assertEqual(values, [100, 110, 120, 130, 140, 150, 160, 170, 180, 190])

    def test_t1_r1_cell_styles(self):
        t = self.body[1]
        row = t["table"][1]
        styles = [row["row"][i]["style"] for i in range(10)]
        self.assertEqual(styles, ["right"] * 10)

    def test_t1m_r1_row_values(self):
        t = self.body_min[1]
        row = t["table"][1]
        self.assertEqual(row, [100, 110, 120, 130, 140, 150, 160, 170, 180, 190])

    def test_t1_r1_row_style(self):
        t = self.body[1]
        row = t["table"][1]
        self.assertEqual(row["style"], "default_table_row")

    ######################################
    # t1 row 2
    ######################################
    def test_t1_r2_dict(self):
        t = self.body[1]
        row = t["table"][2]
        self.assertIsInstance(row, dict)

    def test_t1_r2_krow(self):
        t = self.body[1]
        row = t["table"][2]
        self.assertIsInstance(row["row"], list)

    def test_t1m_r2_list(self):
        t = self.body_min[1]
        row = t["table"][2]
        self.assertIsInstance(row, list)

    def test_t1_r2_len(self):
        t = self.body[1]
        row = t["table"][2]
        self.assertEqual(len(row["row"]), 10)

    def test_t1m_r2_len(self):
        t = self.body_min[1]
        row = t["table"][2]
        self.assertEqual(len(row), 10)

    def test_t1_r2_row_values_type(self):
        t = self.body[1]
        row = t["table"][2]
        for i in range(10):
            self.assertIsInstance(row["row"][i], dict)

    def test_t1m_r2_row_values_type(self):
        t = self.body_min[1]
        row = t["table"][2]
        for i in range(10):
            self.assertIsInstance(row[i], int)

    def test_t1_r2_cell_dict(self):
        t = self.body[1]
        row = t["table"][2]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["value"], int)

    def test_t1_r2_cell_dict_st(self):
        t = self.body[1]
        row = t["table"][2]
        for i in range(10):
            self.assertIsInstance(row["row"][i]["style"], str)

    def test_t1_r2_cell_values(self):
        t = self.body[1]
        row = t["table"][2]
        values = [row["row"][i]["value"] for i in range(10)]
        self.assertEqual(values, [101, 111, 121, 131, 141, 151, 161, 171, 181, 191])

    def test_t1_r2_cell_styles(self):
        t = self.body[1]
        row = t["table"][2]
        styles = [row["row"][i]["style"] for i in range(10)]
        self.assertEqual(styles, ["right"] * 10)

    def test_t1m_r2_row_values(self):
        t = self.body_min[1]
        row = t["table"][2]
        self.assertEqual(row, [101, 111, 121, 131, 141, 151, 161, 171, 181, 191])

    def test_t1_r2_row_style(self):
        t = self.body[1]
        row = t["table"][2]
        self.assertEqual(row["style"], "default_table_row")


if __name__ == "__main__":
    main()
