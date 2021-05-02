#!/usr/bin/env python
# Copyright 2021 Jérôme Dumonteil
# Licence: MIT
# Authors: jerome.dumonteil@gmail.com
"""Generate a json file from an OpenDocument Format .ods file.

When used as a script, odsparsator parses an .ods file and generates a json
file using the odfdo library.

When used as a library, odsparsator parses an .ods file and returns a python
structure.

The resulting data follow the format of the reverse odsgenerator.py script.
"""

from .odsparsator import main, ods_to_python
