from astropy.io import fits
from astropy import units as u
import numpy as np

def get_cube_info(filename, unit=None):
    """
    Utility tool to extract the data cube, velocity axis, and cdelt along the
    velocity axis.

    Parameters
    ==========
    unit: astropy.unit
        The units of the velocity axis.  Overrides CUNIT3 if present.

    """

    cube = fits.getdata(filename).squeeze()
    header = fits.getheader(filename)

    cd3 = 'CDELT3' if 'CDELT3' in header else 'CD3_3'
    cd1 = 'CDELT1' if 'CDELT1' in header else 'CD1_1'

    if unit is None:
        unit = u.Unit(header['CUNIT3'])

    velocity = (((-header['CRPIX3'] +
                  np.arange(header['NAXIS3'])+1)*header[cd3]
                 + header['CRVAL3']) * unit)
    velocity = velocity.to('km/s')

    # cdelt in arceconds
    cdelt = np.abs(header[cd1]) * 3600

    return cube,velocity,cdelt
