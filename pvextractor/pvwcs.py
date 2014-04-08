from astropy import wcs
import numpy as np

def pvwcs_from_header(header, cdelt=None, velo_ctype='VELO-LSR'):
    """
    Convert a cube header (with velocity/frequency along 3rd axis)
    to a Position-Velocity WCS, with ctype "OFFSET" for the spatial
    offset direction

    Parameters
    ----------
    header: astropy.io.fits.Header
    cdelt: float
        a cdelt to override the header cdelt along the velocity (3rd) axis
    velo_ctype: str
        A length-8 str, a FITS header keyword indicating the velocity axis
        ctype
    """
    # Create a new WCS object.  The number of axes must be set
    # from the start
    w3 = wcs.WCS(header)
    if cdelt is None:
        if hasattr(w3.wcs,'pc'):
            cdelt = np.abs(w3.wcs.pc[0,0])
            PC = w3.wcs.pc * w3.wcs.cdelt
        else:
            cdelt = np.abs(w3.wcs.cd[0,0])
            PC = w3.wcs.cd * w3.wcs.cdelt
    w = wcs.WCS(naxis=2)

    # Set up an "Airy's zenithal" projection
    # Vector properties may be set with Python lists, or Numpy arrays
    w.wcs.crpix = [1,1]
    w.wcs.cdelt = np.array([cdelt,PC[2,2],])
    w.wcs.crval = [0, w3.wcs.crval[2]]
    w.wcs.ctype = ["OFFSET", velo_ctype]

    # there must be a reason for this
    w.wcs.set_pv([(2, 1, 45.0)])

    return w

