Extracting slices programmatically
==================================

Defining a path
^^^^^^^^^^^^^^^

Pixel coordinates
~~~~~~~~~~~~~~~~~

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

World coordinates
~~~~~~~~~~~~~~~~~

To define a path in world coordinates, pass a coordinate array to the ``Path``
object.   In addition, the width (if passed) should an Astropy
:class:`~astropy.units.Quantity` object::

    >>> from astropy import units as u
    >>> from astropy.coordinates import Galactic
    >>> g = Galactic([3.4, 3.6] * u.deg, [0.5, 0.56] * u.deg)
    >>> path4 = Path(g, width=1 * u.arcsec)

In additon to the :class:`~pvextractor.Path` class, we provide a convenience
:class:`~pvextractor.PathFromCenter` class that can be used for cases where the
center and position angle of the path are known (rather than the end points of
the path). This class is used as follows:

    >>> from pvextractor import PathFromCenter
    >>> from astropy import units as u
    >>> from astropy.coordinates import Galactic
    >>> g = Galactic(3 * u.deg, 5 * u.deg)
    >>> path5 = PathFromCenter(center=g,
    ...                        length=1 * u.arcmin,
    ...                        angle=30 * u.deg,
    ...                        width=1 * u.arcsec)

The position angle is defined counter-clockwise from North, and the direction
of the path is such that for a position angle of zero, the path is defined from
South to North.

Extracting a slice
^^^^^^^^^^^^^^^^^^

Once the path has been defined, you can make use of the
:func:`~pvextractor.extract_pv_slice` function to extract the PV slice. The
data to slice can be passed to this function as:

* A 3-d Numpy array
* A :class:`~spectral_cube.SpectralCube` instance
* An HDU object containing a spectral cube
* The name of a FITS file containing a spectral cube

For example::

    >>> from pvextractor import extract_pv_slice
    >>> slice1 = extract_pv_slice(array, path1)  # doctest: +SKIP

    >>> from spectral_cube import SpectralCube
    >>> cube = SpectralCube.read('my_cube.fits')  # doctest: +SKIP
    >>> slice2 = extract_pv_slice(cube, path3)  # doctest: +SKIP

    >>> slice3 = extract_pv_slice('my_cube.fits', path3)  # doctest: +SKIP

.. note:: If a path is passed in in world coordinates, and the data are passed
          as a plain Numpy array, the WCS information should be passed as a
          :class:`~astropy.wcs.WCS` object to the ``wcs=`` argument.

Saving the slice
^^^^^^^^^^^^^^^^

The returned slice is an Astropy :class:`~astropy.io.fits.PrimaryHDU` instance,
which you can write to disk using::

    >>> slice1.writeto('my_slice.fits')  # doctest: +SKIP
