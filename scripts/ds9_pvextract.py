import sys
import ds9
import pyregion
from astropy import wcs
import pvextractor

xpa = sys.argv[1]
dd = ds9.ds9(xpa)
pf = dd.get_pyfits()

if len(sys.argv) > 2:
    regionid = int(sys.argv[2])
else:
    regionid = 0

mywcs = wcs.WCS(pf[0].header)
rp = pyregion.RegionParser()

regions = [rp.parseLine(x) for x in dd.get_regions().split("\n")]
paths = pvextractor.paths_from_regions(regions)

slc = pvextractor.extract_pv_slice(pf[0].data, paths[regionid])
