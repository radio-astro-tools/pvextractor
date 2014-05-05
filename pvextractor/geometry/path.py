from __future__ import print_function

import numpy as np
from astropy.wcs import WCSSUB_CELESTIAL
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
    coords : list or array coordinate object
        The points defining the path. This can be passed as a list of (x, y)
        tuples, which is interpreted as being pixel positions, or it can be
        an Astropy coordinate object containing an array of 2 or more
        coordinates.
    width : None or float or :class:`~astropy.units.Quantity`
        The width of the path. If ``coords`` is passed as a list of pixel
        positions, the width should be given (if passed) as a floating-point
        value in pixels. If ``coords`` is a coordinate object, the width
        should be passed as a :class:`~astropy.units.Quantity` instance with
        units of angle.
    """

    def __init__(self, coords=None, width=None):
        self.coords = coords
        self.width = width

    @property
    def path_type(self):
        if isinstance(self.coords, list):
            return 'pixel'
        else:
            return 'world'

    def add_point(self, coord):
        """
        Add a point to the path

        Parameters
        ----------
        xy : tuple or Astropy coordinate
            A tuple (x, y) containing the coordinates of the point to add (if
            the path is defined in pixel space), or an Astropy coordinate
            object (if it is defined in world coordinates).
        """
        if self.path_type == 'pixel':
            if isinstance(coord, tuple):
                self.coords.append(coord)
            else:
                raise TypeError("Path is defined as a list of pixel "
                                "coordinates, so ``coord`` should be "
                                "a tuple of ``(x,y)`` pixel coordinates.")
        else:
            if isinstance(coord, BaseCoordinateFrame):
                raise NotImplementedError("Cannot yet append world coordinates to path")
            else:
                raise TypeError("Path is defined in world coordinates, "
                                "so ``coord`` should be an Astropy "
                                "coordinate object.")

    def get_xy(self, wcs=None):
        """
        Return the pixel coordinates of the path.

        If the path is defined in world coordinates, the appropriate WCS
        transformation should be passed.

        Parameters
        ----------
        wcs : :class:`~astropy.wcs.WCS`
            The WCS transformation to assume in order to transform the path
            to pixel coordinates.
        """
        if self.path_type == 'pixel':
            return self.coords
        else:
            if wcs is None:
                raise ValueError("``wcs`` is needed in order to compute "
                                 "the pixel coordinates")
            else:

                # Extract the celestial component of the WCS
                wcs_sky = wcs.sub([WCSSUB_CELESTIAL])

                # Find the astropy name for the coordinates
                # TODO: return a frame class with Astropy 0.4, since that can
                # also contain equinox/epoch info.
                celestial_system = get_wcs_system_name(wcs_sky)

                world_coords = getattr(self.coords, celestial_system)

                xw, yw = world_coords.lonangle.degree, world_coords.latangle.degree

                return zip(*wcs_sky.wcs_world2pix(xw, yw, 0))

    def sample_points_edges(self, spacing):

        x, y = zip(*self.get_xy())

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

        x, y = zip(*self.get_xy())

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
