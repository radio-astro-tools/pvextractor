#!/usr/bin/env python
"""
PV extract a ds9 image with regions on it
"""
import sys
import ds9
import pyregion
from astropy import wcs
import pvextractor
from astropy.io import fits
import tempfile

xpa = sys.argv[1]
dd = ds9.ds9(xpa)
pf = dd.get_pyfits()

if len(sys.argv) > 2:
    regionid = int(sys.argv[2])
else:
    regionid = 0

mywcs = wcs.WCS(pf[0].header)
rp = pyregion.RegionParser()

regions = pyregion.parse(dd.get('regions -system wcs'))
if len(regions) == 0:
    sys.exit("No regions found")

paths = pvextractor.paths_from_regions(regions, wcs=mywcs)

hdu = pvextractor.extract_pv_slice_hdu(pf[0], paths[regionid], order=0)

with tempfile.NamedTemporaryFile(suffix='fits', delete=False) as tf:
    hdu.writeto(tf)

# it may be possible to do this by
# ds9_pvextract.py $xpa_method | $image
# or any of the commented methods below...
dd.set('frame new')
#print tf.name
dd.set('fits '+tf.name)
#dd.set_pyfits(fits.HDUList(hdu))
#dd.set_np2arr(slc)
