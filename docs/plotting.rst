Plotting PV diagrams
--------------------


Once you have extracted a position-velocity diagram, you likely want to plot it
with appropriate units.  This can be done using the WCS associated with the
PV data:


.. code-block:: python

   import pylab as pl
   from astropy.io import fits
   pvfits = fits.open('extracted_pv.fits')
   ww = wcs.WCS(pvfits[0].header)
   ax = pl.subplot(111, projection=ww)


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


To show the extraction path, use the `shiw_on_axis` method:

   
.. code-block:: python

   cube = SpectralCube.read('data.fits')
   ax = pl.subplot(111, projection=cube.wcs.celestial)
   ax.imshow(cube.moment0(axis=0).value)

   path.show_on_axis(ax, spacing=1)


The `path` will be shown either as a set of lines if the path's width is zero
or as a set of rectangles if the path has a finite width.

The spacing should probably be set to the same spacing used for the PV
extraction, but there are cases where coarser or finer display is warranted.
