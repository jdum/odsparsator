# odsparsator, a .ods parser.

Generate a JSON file from an OpenDocument Format `.ods` file.

When used as a script, `odsparsator` parses a `.ods` file and generates a JSON
file using the `odfdo` library.

When used as a library, `odsparsator` parses a `.ods` file and returns a Python
structure.

The resulting data follows the format of the reverse `odsgenerator.py` script,
see https://github.com/jdum/odsgenerator


`odsparsator` is a `Python3` package, using the [odfdo](https://github.com/jdum/odfdo) library. Current version requires Python >= 3.9, see prior versions for older environments.

Project:
    https://github.com/jdum/odsparsator

Author:
    jerome.dumonteil@gmail.com

License:
    MIT


## Installation

This the minimal "one file version".

- no install required for the main script, juste launch it as

```
python odsparsator.py
```

- BUT you need to check that you use Python version >= 3.9 and install manually (with pip) the 2 dependencies:

    - odfdo  (version >=3.4)
    - lxml   (version ~4.0)

For this branch with only the .py script, if you want to test something, you need to make tests manually like:

```
python odsparsator.py -m test_data/json.ods  result.json
```


## CLI usage

```
odsparsator [-h] [--version] [options] input_file output_file
```

### arguments

`input_file`: input file, a .ods file.

`output_file`: output file, JSON file generated from input.

Use ``odsparsator --help`` for more details about options.


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
import odsparsator

content = odsparsator.ods_to_python("sample1.ods")
```


## Documentation

See in the `./doc` folder:


`html/odsparsator.html`


## License

This project is licensed under the MIT License (see the
`LICENSE` file for details).
