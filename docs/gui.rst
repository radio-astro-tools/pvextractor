Using the built-in graphical user interface
===========================================

The extractor GUI provdes the most direct interface available to the
pixel-matched version of the position-velocity extractor.  It is simple to
initialize:

.. code-block:: python

    from pvextractor.gui import PVSlicer
    pv = PVSlicer('cube.fits')

Click to select "control points" along the path, then press "enter" to expand
the width of the slice, then click.  Optionally, "y" will show the exact
regions extracted.
