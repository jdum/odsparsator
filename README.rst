.. _odsparsator-an-ods-parser:


odsparsator, an .ods parser.
============================

Generate a json file from an OpenDocument Format .ods file.

When used as a script, odsparsator parses an .ods file and generates a json
file using the odfdo library.

When used as a library, odsparsator parses an .ods file and returns a python
structure.

The resulting data follows the format of the reverse odsgenerator.py script,
see https://github.com/jdum/odsgenerator


installation
------------

.. code-block:: bash

    $ pip install odsparsator


usage
-----

::

   odsparsator [-h] [--version] [options] input_file output_file


arguments
---------

``input_file``: input file, a .ods file.

``output_file``: output file, json file generated from input.

Use ``odsparsator --help`` for more details about options.


sample
------

.. code-block:: bash

    $ odsparsator --minimal sample.ods sample_minimal.json


The result:

.. code-block:: python

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


Without the --minimal option:

.. code-block:: bash

    $ odsparsator sample.ods sample_with_styles.json


The result:

.. code-block:: python

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


from python code
----------------

.. code-block:: python

    import odsparsator
    content = odsparsator.ods_to_python("sample1.ods")


documentation
-------------

See in the doc folder:

``html/odsparsator.html``


license
-------

This project is licensed under the MIT License (see the
``LICENSE`` file for details).
