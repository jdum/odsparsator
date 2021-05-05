#!/usr/bin/env python

from unittest import TestCase, main

import json
import odsparsator.odsparsator as p


def canonical(item):
    if isinstance(item, dict):
        if "styles" in item:
            tmp = sorted([(s["definition"], s.get("name")) for s in item["styles"]])
            item["styles"] = tmp
    return json.dumps(item, sort_keys=True, indent=4, ensure_ascii=False)


class TestFileJSONTestFile(TestCase):
    def setUp(self):
        ods_file = "test_json.ods"
        json_file = "result_test_json.json"
        json_file_min = "result_test_json_m.json"
        json_file_all = "result_test_json_a.json"

        self.content = p.ods_to_python(ods_file)
        self.content_min = p.ods_to_python(ods_file, export_minimal=True)
        self.content_all = p.ods_to_python(ods_file, all_styles=True)

        with open(json_file, "r", encoding="utf-8") as r:
            self.result = json.load(r)
        with open(json_file_min, "r", encoding="utf-8") as r:
            self.result_min = json.load(r)
        with open(json_file_all, "r", encoding="utf-8") as r:
            self.result_all = json.load(r)

    def test_json_content(self):
        self.assertEqual(canonical(self.content), canonical(self.result))

    def test_json_content_min(self):
        self.assertEqual(canonical(self.content_min), canonical(self.result_min))

    def test_json_content_all(self):
        self.assertEqual(canonical(self.content_min), canonical(self.result_min))


if __name__ == "__main__":
    main()
