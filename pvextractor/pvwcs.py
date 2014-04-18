from astropy import wcs
import numpy as np

def pvwcs_from_header(header, cdelt=None):
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
    w3 = wcs.WCS(header).sub([wcs.WCSSUB_CELESTIAL,wcs.WCSSUB_SPECTRAL])

    # HACK: dangerous.
    #if w3.naxis < 3:
    #    w3 = wcs.WCS(header)

    PC = w3.wcs.get_pc() * w3.wcs.cdelt
    if cdelt is None:
        cdelt = (PC[0,0]**2 + PC[1,1]**2)**0.5
    w = wcs.WCS(naxis=2)

    spectral_ctype = w3.wcs.ctype[w3.wcs.spec]

    w.wcs.crpix = [1, w3.wcs.crpix[w3.wcs.spec]]
    w.wcs.cdelt = np.array([cdelt,PC[w3.wcs.spec,w3.wcs.spec],])
    w.wcs.crval = [0, w3.wcs.crval[w3.wcs.spec]]
    w.wcs.ctype = ["OFFSET", spectral_ctype]
    w.wcs.cunit = [w3.wcs.cunit[0], w3.wcs.cunit[w3.wcs.spec]]

    return w
