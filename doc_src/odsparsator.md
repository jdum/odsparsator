# odsparsator, a .ods parser.

Generate a JSON file from an OpenDocument Format `.ods` file.

When used as a script, `odsparsator` parses a `.ods` file and generates a JSON
file using the `odfdo` library.

When used as a library, `odsparsator` parses a `.ods` file and returns a Python
structure.

The resulting data follows the format of the reverse `odsgenerator.py` script,
see https://github.com/jdum/odsgenerator


`odsparsator` is a `Python` package, using the [odfdo](https://github.com/jdum/odfdo) library. Current version requires Python >= 3.9, see prior versions for older environments.

Project:
    https://github.com/jdum/odsparsator

Author:
    jerome.dumonteil@gmail.com

License:
    MIT


## Installation

Installation from Pypi (recommended):


```bash
pip install odsparsator
```

Installation from sources:

```bash
uv sync
```

## CLI usage

```
odsparsator [-h] [--version] [options] input_file output_file
```

### arguments

`input_file`: input file, a .ods file.

`output_file`: output file, JSON file generated from input.

Use ``odsparsator --help`` for options:

```
options:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  -m, --minimal      keep only rows and cells, no styles, no formula, no column width
  -a, --all-styles   collect all styles from the input
  -c, --color        collect background color of cells
  -k, --keep-styled  keep styled cells with empty value
  -s, --see-hidden   parse also the hidden sheets

```


### sample

```sh
$ odsparsator --minimal sample.ods sample_minimal.json
```

The result:

```python
{
    "body": [
        {
            "name": "first tab",
            "table": [
                ["a", "b", "c"],
                [10, 20, 30]
            ]
        }
    ]
}
```

Without the --minimal option:

```sh
$ odsparsator sample.ods sample_with_styles.json
```

The result:

```python

{
"body": [
    {
        "name": "first tab",
        "table": [
            {
                "row": [
                    {
                        "value": "a",
                        "style": "bold_center_bg_gray_grid_06pt"
                    },
                    {
                        "value": "b",
                        "style": "bold_center_bg_gray_grid_06pt"
                        ...
```


## Usage from python code


```python
from odsparsator import odsparsator

content = odsparsator.ods_to_python("sample1.ods")
```

## Principle

-  A document is a list or dict containing tabs,
-  a tab is a list or dict containing rows,
-  a row is a list or dict containing cells.


A **cell** can be:

- int, float or str,
- a dict, with the following keys (only the 'value' key is mandatory):
    - value: int, float or str,
    - style: str or list of str, a style name or a list of style names,
    - text: str, a string representation of the value (for ODF readers
      who use it),
    - formula: str, content of the 'table:formula' attribute, some "of:"
      OpenFormula string,
    - colspanned: int, the number of spanned columns,
    - rowspanned: int, the number of spanned rows.

A **row** can be:

- a list of cells,
- a dict, with the following keys (only the 'row' key is mandatory):
    - row: a list of cells, see above,
    - style: str or list of str, a style name or a list of style names.

A **tab** can be:

- a list of rows,
- a dict, with the following keys (only the 'table' key is mandatory):
    - table: a list of rows,
    - width: a list containing the width of each column of the table
    - name: str, the name of the tab,
    - style: str or list of str, a style name or a list of style names.

A tab may have some post transformation:

- a list of span areas, cell coordinates are defined in the tab after
  its creation using odfo method Table.set_span(), with either
  coordiante system: "A1:B3" or [0, 0, 2, 1].

A **document** can be:

- a list of tabs,
- a dict, with the following keys (only the 'body' key is mandatory):
    - body: a list of tabs,
    - styles: a list of dict of styles definitions,
    - defaults: a dict, for the defaults styles.

A **style** definition is a dict with 2 items:

- the name of the style (optional, if not present the attribute
  style:name of the definition is used),
- an XML definition of the ODF style, see list below.
