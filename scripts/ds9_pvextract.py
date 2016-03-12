#!/usr/bin/env python
"""
PV extract a ds9 image with regions on it
"""
import sys
import pyds9
#import pyregion
from astropy import wcs
import pvextractor
from pvextractor.pvregions import load_regions_stringlist, paths_from_regions
from astropy.io import fits
import tempfile

xpa = sys.argv[1]
dd = pyds9.ds9(xpa)
pf = dd.get_pyfits()
# Have to get the raw header; ds9 processes it to drop length-1 axes
header = fits.Header.fromstring(dd.get('fits header'),sep="\n")

if len(sys.argv) > 2:
    regionid = int(sys.argv[2])
else:
    regionid = 0

mywcs = wcs.WCS(pf[0].header)
#rp = pyregion.RegionParser()

# have to check for ds9 dropping degenerate axes
if pf[0].data.ndim != mywcs.wcs.naxis:
    naxes = ['NAXIS%i' % ii for ii in range(1,mywcs.wcs.naxis+1)]
    # WCS is 1-indexed
    axes_to_keep = [ii+1
                    for ii,nax in enumerate(naxes)
                    if header[nax] > 1]
    mywcs = mywcs.sub(axes_to_keep)
    pf[0].header = mywcs.to_header()


rstringlist = dd.get('regions -system wcs').split("\n")
regions = load_regions_stringlist(rstringlist)
if len(regions) == 0:
    sys.exit("No regions found")

paths = paths_from_regions(regions)

hdu = pvextractor.extract_pv_slice(pf[0], paths[regionid], order=0)

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
