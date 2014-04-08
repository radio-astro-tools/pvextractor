import numpy as np

from scipy.ndimage import map_coordinates


def extract_line_slice(cube, x, y, interpolation='spline', order=3, respect_nan=False):
    """
    Given an array with shape (z, y, x), extract a (z, n) slice by
    interpolating at n (x, y) points.

    All units are in *pixels*.

    .. note:: If there are NaNs in the cube, they will be treated as zeros when
              using spline interpolation.

    Parameters
    ----------
    cube : `~numpy.ndarray`
        The data cube to extract the slice from
    curve : list or tuple
        A list or tuple of (x, y) pairs, with minimum length 2
    interpolation : 'nearest' or 'spline', optional
        Either use naive nearest-neighbor estimate or scipy's map_coordinates,
        which defaults to a 3rd order spline.
    order : int, optional
        Spline interpolation order if spline interpolation is used.

    Returns
    -------
    slice : `numpy.ndarray`
        The (z, d) slice
    """

    if interpolation == 'nearest':

        slice = cube[:, np.round(y).astype(int), np.round(x).astype(int)]

    elif interpolation == 'spline':

        nx = len(x)
        nz = cube.shape[0]

        zi = np.outer(np.arange(nz, dtype=int), np.ones(nx))
        xi = np.outer(np.ones(nz), x)
        yi = np.outer(np.ones(nz), y)

        slice = map_coordinates(np.nan_to_num(cube), [zi,yi,xi-0.5], order=order)

        if respect_nan:
            slice_bad = map_coordinates(np.nan_to_num(np.isnan(cube)),
                                        [zi,yi-0.5,xi-0.5], order=order)
            slice[np.nonzero(slice_bad)] = np.nan

    return slice

