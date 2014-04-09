import numpy as np
from scipy.ndimage import map_coordinates
from astropy.wcs import WCS
from astropy import units as u
from .utils.wcs_utils import assert_independent_3rd_axis, wcs_spacing
from .geometry import extract_slice

def vector_pvdiagram(hdu, startx, starty, posang, distance=None, **kwargs):
    """
    Create a pv diagram of some finite distance starting at a world coordinate
    position at some position angle
    """

    wcs = WCS(hdu.header)
    assert_independent_3rd_axis(wcs)

    if distance is None:
        raise NotImplementedError("Just use a large number okay?")

    dx,dy = (np.cos((90-posang)/180*np.pi)*distance,
             np.sin((90-posang)/180*np.pi)*distance,)

    return wcs_pvdiagram(hdu.data, [startx,startx+dx], [starty,starty+dy],
                         **kwargs)

def wcs_pvdiagram(hdu, x, y, spacing=None, **kwargs):
    """
    Create a PV diagram starting from a set of WCS coordinates

    Parameters
    ----------
    hdu: astropy.io.fits.PrimaryHDU object
        The cube HDU
    endpoints: tuple of float pairs
        The endpoints along which to sample specified in the world coordinates
        of the FITS header
    spacing: float or astropy quantity
        The spacing between samples in the output PV diagram.  Assumed to be
        pixels unless valid units are given
    """

    wcs = WCS(hdu.header)
    assert_independent_3rd_axis(wcs)

    # convert the endpoints from WCS to pixels by assuming that the 3rd axis is
    # independent
    px,py = wcs.wcs_world2pix([[a,b,wcs.wcs.crval[2]]
                               for a,b in zip(x,y)], 0)[:,:2]

    return pvdiagram(hdu.data, px, py,
                     spacing=wcs_spacing(wcs, spacing)
                     **kwargs)

def extract_pv_slice(cube, path, spacing=1.0, order=3, respect_nan=False, width=None):
    """
    Given a position-position-velocity cube with dimensions (nv, ny, nx), and
    a path, extract a position-velocity slice.

    Alternative implementations:
        gipsy::sliceview
        karma::kpvslice
        casaviewer::slice

    Parameters
    ----------
    path : `Path`
        The path along which to define the position-velocity slice
    spacing : float
        The position resolution in the final position-velocity slice.
    order : int, optional
        Spline interpolation order when using line paths. Does not have any
        effect for polygon paths.
    respect_nan : bool, optional
        If set to `False`, NaN values are changed to zero before computing
        the slices.

    Returns
    -------
    slice : `numpy.ndarray`
        The position-velocity slice
    """

    pv_slice = extract_slice(cube, path, order=order, respect_nan=False)

    return pv_slice
