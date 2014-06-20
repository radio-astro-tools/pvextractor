Slicing in DS9
==============

.. note:: This feature is experimental and does not work with all versions of
          DS9 at this point.

.. TODO: be more specific about which DS9 versions are supported

There is a python command-line script that will be installed into your path
along with ``pvextractor``.  You can invoke it from the command line, but the
preferred approach is to load the
tool into DS9.  First, determine the path to ``ds9_pvextract.ans``;
it is in the ``scripts`` subdirectory of the source code.  Then start
up DS9 with the analysis tool loaded

.. code-block:: bash

    ds9 -analysis load /path/to/pvextractor/scripts/ds9_pvextract.ans  &

Then load any cube in DS9.  You can draw a line, a vector, or a "segment"; only
the first one drawn will have any effect.  To extract the PV diagram, press the
'x' key or click "PV Extractor" in the analysis menu.  Be patient - especially
for big cubes, it may take a little while, and there is no progress bar.