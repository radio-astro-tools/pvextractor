Plotting PV diagrams
--------------------


Once you have extracted a position-velocity diagram, you likely want to plot it
with appropriate units.  This can be done using the WCS associated with the
PV data:


.. code-block:: python

   import pylab as pl
   from spectral_cube import SpectralCube
   from pvextractor import extract_pv_slice, Path

   cube = SpectralCube.read('http://www.astropy.org/astropy-data/l1448/l1448_13co.fits')
   path = Path([(5,5), (10,10)])
   pv = extract_pv_slice(cube, path)

   ww = wcs.WCS(pv.header)
   ax = pl.subplot(111, projection=ww)
   ax.imshow(pv.data)


If you want to change axis units, you can use `astropy.wcsaxes` tools:

https://docs.astropy.org/en/stable/visualization/wcsaxes/controlling_axes.html


.. code-block:: python

   ax0 = ax.coords[0]
   ax0.set_format_unit(u.arcmin)
   ax1 = ax.coords[1]
   ax1.set_format_unit(u.km/u.s)

   ax.set_ylabel("Velocity [km/s]")
   ax.set_xlabel("Offset [arcmin]")

See also the `tutorial <https://github.com/radio-astro-tools/tutorials/blob/6810376c0353f0bdf3be2b9b7231c388e886adba/PVDiagramPlotting.ipynb>`_


Showing the extraction path
---------------------------


To show the extraction path, use the :func:`~pvextractor.Path.show_on_axis` method:


.. code-block:: python

   ax = pl.subplot(111, projection=cube.wcs.celestial)
   ax.imshow(cube.moment0(axis=0).value)

   path.show_on_axis(ax, spacing=1)


The `path` will be shown either as a set of lines if the path's width is zero
or as a set of rectangles if the path has a finite width.

`spacing` should probably be set to the same spacing used for the PV
extraction, but there are cases where coarser or finer display is warranted.
