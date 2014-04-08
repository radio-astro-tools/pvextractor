import numpy as np
from scipy.ndimage import map_coordinates
from astropy.wcs import WCS
from astropy import units as u
from wcs_util import assert_independent_3rd_axis, wcs_spacing
from .geometry import sample_curve, extract_line_slice, extract_thick_slice

def vector_pvdiagram(hdu, startpoint, posang, distance=None, spacing=None,
                     **kwargs):
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

    endpoint = startpoint[0]+dx, startpoint[1]+dy

    return pvdiagram(hdu.data, [startpoint,endpoint],
                     spacing=wcs_spacing(wcs, spacing),
                     **kwargs)


def wcs_pvdiagram(hdu, endpoints, spacing=None, **kwargs):
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
    pixendpoints = wcs.wcs_world2pix([[x,y,wcs.wcs.crval[2]]
                                      for x,y in endpoints], 0)[:,:2]

    return pvdiagram(hdu.data, endpoints=pixendpoints,
                     spacing=wcs_spacing(wcs, spacing)
                     **kwargs)

def pv_slice(cube, x, y, spacing=1.0, interpolation='spline', order=3,
             respect_nan=False, width=None):
    """
    Given a position-position-velocity cube with dimensions (nv, ny, nx), and
    a broken curved defined by ``x``, and ``y``, extract a position-velocity
    slice.

    All units are in *pixels*

    .. note:: If there are NaNs in the cube, they will be treated as zeros when
              using spline interpolation.

    Alternative implementations:
        gipsy::sliceview
        karma::kpvslice
        casaviewer::slice

    Parameters
    ----------
    x, y : `numpy.ndarray`
        The pixel coordinates determining the broken curve
    spacing : float
        The position resolution in the final position-velocity slice.
    interpolation : 'nearest' or 'spline', optional
        Either use naive nearest-neighbor estimate or scipy's map_coordinates,
        which defaults to a 3rd order spline
    order : int, optional
        Spline interpolation order

    Returns
    -------
    slice : `numpy.ndarray`
        The position-velocity slice
    """

    if len(x) != len(y):
        raise ValueError("Length of ``x`` and ``y`` should match")

    if len(x) < 2:
        raise ValueError("``x`` and ``y`` must have length >= 2")

    # Generate sampled curve
    d, x, y = sample_curve(x, y, spacing=spacing)

    if width is None:

        x_mid = (x[1:] + x[:-1]) * 0.5
        y_mid = (y[1:] + y[:-1]) * 0.5

        pv_slice = extract_line_slice(cube, x_mid, y_mid, interpolation=interpolation, order=order)

    else:

        pv_slice = extract_thick_slice(cube, x, y, width=width)

    return pv_slice
