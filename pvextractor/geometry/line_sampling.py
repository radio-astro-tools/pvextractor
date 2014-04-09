import numpy as np


def sample_curve(x, y, spacing, interpolation='linear'):
    """
    Given a set of points x and y, interpolate positions along the curve.

    If the total length of the curve specified by (x, y) is not an integer
    multiple of the spacing, the curve is extrapolated in both directions by
    the same amount.

    Parameters
    ----------
    x, y : iterable
        The points defining the curve
    interpolation : str
        The interpolation technique used to over-sample the curve
    """

    if interpolation == 'linear':

        # Find the distance interval between all pairs of points
        dx = np.diff(x)
        dy = np.diff(y)
        dd = np.hypot(dx, dy)

        # Find the total displacement along the broken curve
        d = np.hstack([0., np.cumsum(dd)])

        # Figure out the number of points to sample
        n_points = np.ceil(d[-1] / spacing) + 1

        # Determine padding at each end
        d_total = (n_points - 1) * spacing
        padding = (d_total - d[-1]) * 0.5

        # Find the start and end points, given padding

        x_start = x[0] - dx[0] * padding / dd[0]
        y_start = y[0] - dy[0] * padding / dd[0]

        x_end = x[-1] + dx[-1] * padding / dd[-1]
        y_end = y[-1] + dy[-1] * padding / dd[-1]

        d = np.hstack([0., d + padding, d_total])
        x = np.hstack([x_start, x, x_end])
        y = np.hstack([y_start, y, y_end])

        d_sampled = np.linspace(0., d_total, n_points)
        x_sampled = np.interp(d_sampled, d, x)
        y_sampled = np.interp(d_sampled, d, y)

    else:

        raise NotImplementedError("Only linear interpolation is supported at this time")

    return d_sampled, x_sampled, y_sampled
