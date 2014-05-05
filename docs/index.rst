.. PV Slice Extractor documentation master file, created by
   sphinx-quickstart on Wed Apr 30 21:14:50 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Position-Velocity Slice Extractor
=================================

The ``pvextractor`` package provides a number of ways of extracting PV slices
from spectral cubes.

Using ``pvextractor``
---------------------

Introduction
^^^^^^^^^^^^

The concept of the ``pvextractor`` package is simple - given a path defined
in sky coordinates, and a spectral cube, extract a slice of the cube along
that path, and along the spectral axis, producing a position-velocity or
position-frequency slice. The path can be defined programmatically in pixel
or world coordinates, but it can also be drawn interactively using a simple
GUI. We also provide a Ds9 analysis plug-in that allows the path to be drawn
in ds9, and the resulting slice shown in a new frame in Ds9.

Defining a path programmatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To define a path in pixel coordinates, import the :class:`~pvextractor.Path`
class::

    >>> from pvextractor import Path

Then initialize it using a list of ``(x,y)`` tuples. The simplest path that
can be defined is a line connecting two points:

    >>> path1 = Path([(0., 0.), (10., 10.)])

Multi-segment paths can also be similarly defined:

    >>> path2 = Path([(0., 0.), (4., 6.), (10., 10.)])

By default, slices are extracted using interpolation along the line, but it
is also possible to define a path with a finite width, and to instead measure
the average flux or surface brightness in finite polygons (rather than
strictly along the line). To give a path a non-zero width, simply use the
``width=`` argument, which is also in pixels by default::

    >>> path3 = Path([(0., 0.), (10., 10.)], width=0.5)

To define a path in world coordinates, you should make use of the
:class:`~pvextractor.WCSPath` class::

    >>> from pvextractor import WCSPath

This class works similarly to :class:`~pvextractor.Path`, but takes a
coordinate object with an array of values instead of a list of tuples. In
addition, the width (if passed) should an Astropy
:class:`~astropy.units.Quantity` object::

    >>> from astropy import units as u
    >>> from astropy.coordinates import Galactic
    >>> g = Galactic([3.4, 3.6] * u.deg, [0.5, 0.56] * u.deg)
    >>> path4 = WCSPath(g, width=1 * u.arcsec)

.. TODO: wcs should not be a property of a path - a path should be defined in
.. absolute world coordinates irrespective of projection.

Extracting a slice
^^^^^^^^^^^^^^^^^^

Once the path has been defined, you can make use of the
:func:`~pvextractor.extract_pv_slice` function to extract the PV slice. The
data to slice can be passed to this function as:

* A 3-d Numpy array
* A :class:`~spectral_cube.SpectralCube` instance
* An HDU object containing a spectral cube
* The name of a FITS file containing a spectral cube

.. TODO: provide a single function as a point of entry?

For example::

    >>> from pvextractor import extract_pv_slice
    >>> slice1 = extract_pv_slice(array, path1)

    >>> from spectral_cube import read
    >>> cube = read('my_cube.fits')
    >>> slice2 = extract_pv_slice(cube, path3)

    >>> slice3 = extract_pv_slice('my_cube.fits', path3)

.. note:: If a :class:`~pvextractor.WCSPath` is passed, the data cannot be a
          plain Numpy array, since it does not contain WCS information.

Advanced paths
^^^^^^^^^^^^^^

This section will describe how to easily set up common paths, e.g. starting
from a point and with a given position angle.

Using the graphical user interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extracting slices from Ds9
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   api.rst