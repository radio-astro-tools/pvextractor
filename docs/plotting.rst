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
