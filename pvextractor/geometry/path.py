import numpy as np
from astropy import wcs as astropywcs
from ..utils.wcs_utils import get_wcs_system_name


class Polygon(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def segment_angles(x, y):

    dx = np.diff(x)
    dy = np.diff(y)

    d = np.hypot(dx, dy)

    cos_theta = (-dx[:-1] * dx[1:] - dy[:-1] * dy[1:]) / (d[:-1] * d[1:])
    cos_theta = np.clip(cos_theta, -1., 1.)

    sin_theta = (-dx[:-1] * dy[1:] + dy[:-1] * dx[1:]) / (d[:-1] * d[1:])
    sin_theta = np.clip(sin_theta, -1., 1.)

    theta = np.arctan2(sin_theta, cos_theta)

    theta[0] = np.pi
    theta[-1] = np.pi

    return theta


def get_endpoints(x, y, width):

    # Pad with same values at ends, to find slope of perpendicular end
    # lines.
    xp = np.pad(x, 1, mode='edge')
    yp = np.pad(y, 1, mode='edge')

    dx = np.diff(xp)
    dy = np.diff(yp)

    alpha = segment_angles(xp, yp) / 2.
    beta = np.arctan2(dy, dx)[:-1]
    beta[0] = beta[1]
    gamma = -(np.pi - alpha - beta)

    dx = np.cos(gamma)
    dy = np.sin(gamma)

    angles = segment_angles(xp, yp) / 2.

    # Find points offset from main curve, on bisecting lines
    x1 = x - dx * width * 0.5 / np.sin(angles)
    x2 = x + dx * width * 0.5 / np.sin(angles)
    y1 = y - dy * width * 0.5 / np.sin(angles)
    y2 = y + dy * width * 0.5 / np.sin(angles)

    return x1, y1, x2, y2


class Path(object):
    """
    A curved path that may have a non-zero width and is used to extract
    slices from cubes.

    Parameters
    ----------
    xy : `numpy.ndarray`
        The points defining the path, as a list of (x, y) tuples.
    width : None or float
        The width of the path.
    """

    def __init__(self, xy=None, width=None):

        self.xy = [] if xy is None else xy
        self.width = width

    def add_point(self, xy):
        """
        Add a point to the path

        Parameters
        ----------
        xy : tuple
            A tuple (x, y) containing the coordinates of the point to add
        """
        self.xy.append(xy)

    def sample_points_edges(self, spacing):

        x, y = zip(*self.xy)

        # Find the distance interval between all pairs of points
        dx = np.diff(x)
        dy = np.diff(y)
        dd = np.hypot(dx, dy)

        # Find the total displacement along the broken curve
        d = np.hstack([0., np.cumsum(dd)])

        # Figure out the number of points to sample, and stop short of the
        # last point.
        n_points = np.floor(d[-1] / spacing)

        if n_points == 0:
            raise ValueError("Path is shorter than spacing")

        d_sampled = np.linspace(0., n_points * spacing, n_points + 1)

        x_sampled = np.interp(d_sampled, d, x)
        y_sampled = np.interp(d_sampled, d, y)

        return d_sampled, x_sampled, y_sampled

    def sample_points(self, spacing):

        d_sampled, x_sampled, y_sampled = self.sample_points_edges(spacing)

        x_sampled = 0.5 * (x_sampled[:-1] + x_sampled[1:])
        y_sampled = 0.5 * (y_sampled[:-1] + y_sampled[1:])

        return x_sampled, y_sampled

    def sample_polygons(self, spacing):

        x, y = zip(*self.xy)

        d_sampled, x_sampled, y_sampled = self.sample_points_edges(spacing)

        # Find the distance interval between all pairs of points
        dx = np.diff(x)
        dy = np.diff(y)
        dd = np.hypot(dx, dy)

        # Normalize to find unit vectors
        dx = dx / dd
        dy = dy / dd

        # Find the total displacement along the broken curve
        d = np.hstack([0., np.cumsum(dd)])

        interval = np.searchsorted(d, d_sampled) - 1
        interval[0] = 0

        dx = dx[interval]
        dy = dy[interval]

        polygons = []

        x_beg = x_sampled - dx * spacing * 0.5
        x_end = x_sampled + dx * spacing * 0.5

        y_beg = y_sampled - dy * spacing * 0.5
        y_end = y_sampled + dy * spacing * 0.5

        x1 = x_beg - dy * self.width * 0.5
        y1 = y_beg + dx * self.width * 0.5

        x2 = x_end - dy * self.width * 0.5
        y2 = y_end + dx * self.width * 0.5

        x3 = x_end + dy * self.width * 0.5
        y3 = y_end - dx * self.width * 0.5

        x4 = x_beg + dy * self.width * 0.5
        y4 = y_beg - dx * self.width * 0.5

        for i in range(len(x_sampled) - 1):
            p = Polygon([x1[i], x2[i], x3[i], x4[i]], [y1[i], y2[i], y3[i], y4[i]])
            polygons.append(p)

        return polygons

class WCSPath(Path):

    def __init__(self, coords=None, width=None, wcs=None):
        """
        Takes an astropy Coordinates array
        """

        self.set_wcs(wcs)
        self.coords = coords
        self.width = width

    def _coords_to_wcs(self, coords):

        if self.wcs is None:
            raise ValueError("Must set a WCS first")

        xynative = getattr(coords,self.celsys)
        
        x,y = xynative.lonangle.degree, xynative.latangle.degree

        xy = self.wcs.wcs_world2pix(x,y, 0)
        return xy

    def set_wcs(self, wcs):
        if wcs is not None:
            self.wcs = wcs.sub([astropywcs.WCSSUB_CELESTIAL])
            self.celsys = get_wcs_system_name(self.wcs)
        else:
            self.wcs = None

    def add_point(self, coord):
        """
        Add a point to the path

        Parameters
        ----------
        xy : tuple
            A tuple (x, y) containing the coordinates of the point to add
        """
        if hasattr(coord,'fk5'): # it is a coordinate
            self.xy += self._coords_to_wcs(coord).tolist()


    @property
    def xy(self):
        if self.wcs is not None:
            return zip(*self._coords_to_wcs(self.coords))
        else:
            raise ValueError("Must set a WCS to get xy coordinates")
