import numpy as np

# TODO: implement variable width


class Polygon(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Path(object):
    """
    A path that may have a width.

    Parameters
    ----------
    x, y : `numpy.ndarray`
        The points defining the path
    width : None or float
        The width of the path.
    """

    def __init__(self, x=[], y=[], width=None):

        self.x = x
        self.y = y
        self.width = width


    def add_point(self, x, y):

        self.x.append(x)
        self.y.append(y)

    def sample_points(self, spacing):

        # Find the distance interval between all pairs of points
        dx = np.diff(self.x)
        dy = np.diff(self.y)
        dd = np.hypot(dx, dy)

        # Find the total displacement along the broken curve
        d = np.hstack([0., np.cumsum(dd)])

        # Figure out the number of points to sample, and stop short of the
        # last point.
        n_points = np.floor(d[-1] / spacing)

        if n_points == 0:
            raise ValueError("Path is shorter than spacing")

        d_sampled = np.linspace(0., n_points * spacing, n_points + 1)

        x_sampled = np.interp(d_sampled, d, self.x)
        y_sampled = np.interp(d_sampled, d, self.y)

        x_sampled = 0.5 * (x_sampled[:-1] + x_sampled[1:])
        y_sampled = 0.5 * (y_sampled[:-1] + y_sampled[1:])

        return x_sampled, y_sampled

    def sample_polygons(self, spacing):

        x, y = self.sample_points(spacing)
        
        # Pad with same values at ends, to find slope of perpendicular end
        # lines.
        xp = np.pad(x, 1, mode='edge')
        yp = np.pad(y, 1, mode='edge')

        # Find slope connecting alternating points
        m = -(xp[2:] - xp[:-2]) / (yp[2:] - yp[:-2])
        b = y - m * x

        # Find angle of the intersecting lines
        alpha = np.arctan2(xp[2:] - xp[:-2], yp[:-2] - yp[2:])

        dx = np.cos(alpha)
        dy = np.sin(alpha)

        # Find points offset from main curve, on bisecting lines
        x1 = x - dx * self.width * 0.5
        x2 = x + dx * self.width * 0.5
        y1 = x - dy * self.width * 0.5
        y2 = x + dy * self.width * 0.5

        # Now loop over all the polygons for the slice
        polygons = [Polygon([x1[i], x1[i+1], x2[i+1], x2[i]],
                            [y1[i], y1[i+1], y2[i+1], y2[i]]) for i in range(len(x) - 1)]

        return polygons
