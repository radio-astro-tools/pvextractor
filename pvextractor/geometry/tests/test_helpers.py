import numpy as np

from astropy.coordinates import SkyCoord, Galactic
from astropy import units as u

from ..helpers import PathFromCenter


def test_path_from_center():

    c = SkyCoord(10, 5., unit=u.deg, frame='galactic')

    # Vertical path

    p = PathFromCenter(c, 2 * u.deg, 0 * u.deg)

    assert isinstance(p._coords, Galactic)

    np.testing.assert_allclose(p._coords.l.degree, [10., 10.])
    np.testing.assert_allclose(p._coords.b.degree, [4., 6.])

    # Horizontal path

    p = PathFromCenter(c, 2 * u.deg, 90 * u.deg, sample=3)

    assert isinstance(p._coords, Galactic)

    np.testing.assert_allclose(p._coords.l.degree, [8.99618094, 10., 11.00381906])
    np.testing.assert_allclose(p._coords.b.degree, [4.999237, 5., 4.999237])

    # Diagonal path

    p = PathFromCenter(c, 2 * u.deg, 40 * u.deg, sample=4)

    assert isinstance(p._coords, Galactic)

    np.testing.assert_allclose(p._coords.l.degree, [9.355472736, 9.785001429, 10.215166296, 10.646036893])
    np.testing.assert_allclose(p._coords.b.degree, [4.233656509, 4.744617410, 5.255312488, 5.765712517])
