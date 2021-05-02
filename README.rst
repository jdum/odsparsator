.. _odsparsator-an-ods-parser:


odsparsator, an .ods parser.
============================

Generate a json file from an OpenDocument Format .ods file.

When used as a script, odsparsator parses an .ods file and generates a json
file using the odfdo library.

When used as a library, odsparsator parses an .ods file and returns a python
structure.

The resulting data follow the format of the reverse odsgenerator.py script.


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

Use ``odsparsator --help`` for more details about options
and look at examples in the tests folder.


from python code
----------------

.. code-block:: python

    import odsparsator
    content = odsparsator.ods_to_python("sample1.ods")


documentation
-------------

Doc is coming.

And see also ``odsgenerator``.


license
-------

This project is licensed under the MIT License (see the
``LICENSE`` file for details).
