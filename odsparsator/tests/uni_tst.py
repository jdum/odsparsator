#!/usr/bin/env python

from unittest import TestLoader, TestSuite, TextTestRunner

import test_main
import test_minimal
import test_formula
import test_json
import test_use_case
import test_styles

modules = [test_main, test_minimal, test_formula, test_json, test_use_case, test_styles]

loader = TestLoader()

if __name__ == "__main__":
    suite = TestSuite()
    for m in modules:
        suite.addTest(loader.loadTestsFromModule(m))

    TextTestRunner(verbosity=1).run(suite)
