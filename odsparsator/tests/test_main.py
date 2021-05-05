#!/usr/bin/env python

from unittest import TestCase, main

import os
import json
import odsparsator.odsparsator as p


class TestMain(TestCase):
    def test_no_args_odsparsator(self):
        with self.assertRaises(TypeError) as cm:
            p.ods_to_json()
            self.assertEqual(cm.exception.code, 0)

    def test_one_args_odsparsator(self):
        with self.assertRaises(TypeError) as cm:
            p.ods_to_json()("some file")
            self.assertEqual(cm.exception.code, 0)

    def test_bad_args_odsparsator(self):
        with self.assertRaises(TypeError) as cm:
            p.ods_to_json()("some file", "output", "badarg")
            self.assertEqual(cm.exception.code, 0)


class TestLoadFiles(TestCase):
    def setUp(self):
        self.files = (
            "test_minimal.ods",
            "test_formula.ods",
            "test_json.ods",
            "test_use_case.ods",
        )
        for f in self.files:
            output = f + "_test_.json"
            if os.path.isfile(output):
                os.remove(output)

    def tearDown(self):
        for f in self.files:
            output = f + "_test_.json"
            try:
                os.remove(output)
            except IOError:
                pass

    def test_run(self):
        for f in self.files:
            output = f + "_test_.json"
            p.ods_to_json(f, output)
            self.assertTrue(os.path.isfile(output))

    def test_run_min(self):
        for f in self.files:
            output = f + "_test_.json"
            p.ods_to_json(f, output, True)
            self.assertTrue(os.path.isfile(output))

    def test_run_min_styles(self):
        for f in self.files:
            output = f + "_test_.json"
            p.ods_to_json(f, output, True, True)
            self.assertTrue(os.path.isfile(output))

    def test_run_styles(self):
        for f in self.files:
            output = f + "_test_.json"
            p.ods_to_json(f, output, False, True)
            self.assertTrue(os.path.isfile(output))

    def test_load_json(self):
        for f in self.files:
            output = f + "_test_.json"
            p.ods_to_json(f, output)
            with open(output, "r", encoding="utf-8") as r:
                content = json.load(r)
            self.assertIsInstance(content, dict)
            self.assertIsInstance(content["body"], list)


if __name__ == "__main__":
    main()
