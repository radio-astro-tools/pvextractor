Slicing in DS9
==============

There is a python command-line script that will be installed into your path
along with ``pvextractor``.  You can invoke it from the command line, but the
preferred approach is to load the
tool into ds9.  First, determine the path to ``ds9_pvextract.ans``;
it is in the ``scripts`` subdirectory of the source code.  Then start
up ds9 with the analysis tool loaded

.. code-block:: bash

    ds9 -analysis load /path/to/pvextractor/scripts/ds9_pvextract.ans  &

Then load any cube in ds9.  You can draw a line, a vector, or a "segment"; only
the first one drawn will have any effect.  To extract the PV diagram, press the
'x' key or click "PV Extractor" in the analysis menu.  Be patient - especially
for big cubes, it may take a little while, and there is no progress bar.