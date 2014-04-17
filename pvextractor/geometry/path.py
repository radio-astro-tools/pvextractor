import numpy as np
from astropy import wcs as astropywcs


class Polygon(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_endpoints(x, y, width):

    # Pad with same values at ends, to find slope of perpendicular end
    # lines.
    xp = np.pad(x, 1, mode='edge')
    yp = np.pad(y, 1, mode='edge')

    # Find angle of the intersecting lines
    alpha = np.arctan2(xp[2:] - xp[:-2], yp[:-2] - yp[2:])

    dx = np.cos(alpha)
    dy = np.sin(alpha)

    # Find points offset from main curve, on bisecting lines
    x1 = x - dx * width * 0.5
    x2 = x + dx * width * 0.5
    y1 = y - dy * width * 0.5
    y2 = y + dy * width * 0.5

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

    def sample_points(self, spacing):

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

        x_sampled = 0.5 * (x_sampled[:-1] + x_sampled[1:])
        y_sampled = 0.5 * (y_sampled[:-1] + y_sampled[1:])

        return x_sampled, y_sampled

    def sample_polygons(self, spacing):

        x, y = self.sample_points(spacing)

        x1, y1, x2, y2 = get_endpoints(x, y, self.width)

        # Now loop over all the polygons for the slice
        polygons = [Polygon([x1[i], x1[i+1], x2[i+1], x2[i]],
                            [y1[i], y1[i+1], y2[i+1], y2[i]]) for i in range(len(x) - 1)]

        return polygons

def get_wcs_system_name(wcs):
    """TODO: move to astropy.wcs.utils"""
    ct = wcs.sub([astropywcs.WCSSUB_CELESTIAL]).wcs.ctype
    if 'GLON' in ct[0]:
        return 'galactic'
    elif 'RA' in ct[0]:
        return 'icrs'
    else:
        raise ValueError("Unrecognized coordinate system")

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
