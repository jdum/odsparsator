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
------

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


## Documentation

See in the `./doc` folder:


`html/odsparsator.html`


## License

This project is licensed under the MIT License (see the
`LICENSE` file for details).
