from __future__ import print_function

from astropy import wcs
from astropy import units as u
from astropy.io import fits

from .utils.wcs_utils import (sanitize_wcs, wcs_spacing,
                              get_wcs_system_name, pixel_to_wcs_spacing)
from .geometry import extract_slice
from .pvwcs import pvwcs_from_header

from spectral_cube import StokesSpectralCube, SpectralCube
from spectral_cube.io.fits import load_fits_hdu

def extract_pv_slice_hdu(hdu, path, spacing=None, **kwargs):
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

    sc = load_fits_hdu(hdu)
    mywcs = sanitize_wcs(sc._wcs)
    header = mywcs.to_header()

    pspacing = wcs_spacing(mywcs, spacing)
    wspacing = pixel_to_wcs_spacing(mywcs, pspacing)

    pvwcs = pvwcs_from_header(header, cdelt=wspacing.to(u.deg).value)
    header = pvwcs.to_header()

    celwcs = mywcs.sub([wcs.WCSSUB_CELESTIAL])
    xy = path.get_xy(wcs=mywcs)
    starting_point = celwcs.wcs_pix2world(xy[0][0], xy[0][1], 0)
    header['STARTLON'] = float(starting_point[0])
    header['STARTLAT'] = float(starting_point[1])
    header['CSYSOFFS'] = get_wcs_system_name(mywcs)

    pvslice = extract_pv_slice(sc.filled_data[:,:,:], path, spacing=pspacing, **kwargs)

    return fits.PrimaryHDU(data=pvslice, header=header)

def extract_pv_slice(cube, path, spacing=1.0, order=3, respect_nan=True):
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
        the slices. If set to `True`, in the case of line paths a second
        computation is performed to ignore the NaN value while interpolating,
        and set the output values of NaNs to NaN.

    Returns
    -------
    slice : `numpy.ndarray`
        The position-velocity slice
    """

    pv_slice = extract_slice(cube, path, spacing=spacing, order=order, respect_nan=respect_nan)

    return pv_slice
