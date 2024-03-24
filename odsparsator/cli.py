# Copyright 2021-2024 Jérôme Dumonteil
# Licence: MIT
# Authors: jerome.dumonteil@gmail.com
"""CLI interface to odsparsator.
"""
from __future__ import annotations

import argparse
import sys

import odfdo

from odsparsator.odsparsator import __doc__, __version__, ods_to_json

ODFDO_REQUIREMENT = (3, 7, 5)


def check_odfdo_version() -> bool:
    """Utility to verify we have the minimal version of the odfdo library."""
    if tuple(int(x) for x in odfdo.__version__.split(".")) >= ODFDO_REQUIREMENT:
        return True
    print(  # pragma: no cover
        "Error: odfdo version >= "
        f"{'.'.join(str(x) for x in ODFDO_REQUIREMENT)} is required"
    )
    return False  # pragma: no cover


def main() -> None:  # pragma: no cover
    """Read parameters from STDIN and apply the required command.

    Usage:
    odsparsator [-h] [--version] [options] input_file output_file

    Arguments:
        input_file: Input file, a .ods file.

        output_file: Output file, json file generated from input.
    """
    if not check_odfdo_version():
        sys.exit(1)
    parser = argparse.ArgumentParser(
        description="Generate a json file from an OpenDocument Format .ods file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument("input_file", help="input file, a .ods ODF file.")
    parser.add_argument(
        "output_file", help="output file, exported content in JSON format."
    )
    parser.add_argument(
        "-m",
        "--minimal",
        help="keep only rows and cells, no styles, no formula, no column width",
        action="store_true",
    )
    parser.add_argument(
        "-a",
        "--all-styles",
        help="collect all styles from the input",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--color",
        help="collect background color of cells",
        action="store_true",
    )
    parser.add_argument(
        "-k",
        "--keep-styled",
        help="keep styled cells with empty value",
        action="store_true",
    )
    args = parser.parse_args()
    ods_to_json(
        args.input_file,
        args.output_file,
        args.minimal,
        args.all_styles,
        args.color,
        args.keep_styled,
    )


if __name__ == "__main__":
    main()  # pragma: no cover
