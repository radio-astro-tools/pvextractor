import numpy as np
from scipy.ndimage import map_coordinates
from .geometry import sample_curve, extract_line_slice, extract_thick_slice

def pv_slice(cube, x, y, spacing=1.0, interpolation='spline', order=3,
             respect_nan=False, width=None):
    """
    Given a position-position-velocity cube with dimensions (nv, ny, nx), and
    a broken curved defined by ``x``, and ``y``, extract a position-velocity
    slice.

    All units are in *pixels*

    .. note:: If there are NaNs in the cube, they will be treated as zeros when
              using spline interpolation.

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
