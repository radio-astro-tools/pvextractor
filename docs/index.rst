.. PV Slice Extractor documentation master file, created by
   sphinx-quickstart on Wed Apr 30 21:14:50 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Position-Velocity Slice Extractor
=================================

The concept of the ``pvextractor`` package is simple - given a path defined
in sky coordinates, and a spectral cube, extract a slice of the cube along
that path, and along the spectral axis, producing a position-velocity or
position-frequency slice.

The path can be defined programmatically in pixel or world coordinates, but it
can also be drawn interactively using a simple GUI. We also provide a DS9
analysis plug-in that allows the path to be drawn in DS9, and the resulting
slice shown in a new frame in DS9. Finally, the slicing capability is available in Glue_.

.. toctree::
   :maxdepth: 2

   programmatic.rst
   gui.rst
   glue.rst
   ds9.rst
   api.rst

.. _Glue: http://www.glueviz.org/en/latest/
