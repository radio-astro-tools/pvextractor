Plotting PV diagrams
--------------------


Plotting the PV diagrams can be a challenge.


.. code-block:: python

   pvfits = fits.open('extracted_pv.fits')
   ww = wcs.WCS(pvfits[0].header)
   ax = pl.subplot(111, projection=ww)


   you might want to change the WCS units
                    ww = wcs.WCS(extracted.header)
                    ww.wcs.cdelt[1] /= 1000.0
                    ww.wcs.crval[1] /= 1000.0
                    ww.wcs.cunit[1] = u.km/u.s
                    ww.wcs.cdelt[0] *= 3600
                    ww.wcs.cunit[0] = u.arcsec
                    ww.wcs.crval[0] = -origin.to(u.arcsec).value
