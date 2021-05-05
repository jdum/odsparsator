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


class TestFileUseCase(TestCase):
    def setUp(self):
        ods_file = "test_use_case.ods"
        json_file = "result_test_use_case.json"
        json_file_min = "result_test_use_case_m.json"

        self.content = p.ods_to_python(ods_file)
        self.content_min = p.ods_to_python(ods_file, export_minimal=True)

        with open(json_file, "r", encoding="utf-8") as r:
            self.result = json.load(r)
        with open(json_file_min, "r", encoding="utf-8") as r:
            self.result_min = json.load(r)

    def test_json_content(self):
        self.assertEqual(canonical(self.content), canonical(self.result))

    def test_json_content_min(self):
        self.assertEqual(canonical(self.content_min), canonical(self.result_min))


if __name__ == "__main__":
    main()
