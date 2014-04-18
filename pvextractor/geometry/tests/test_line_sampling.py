from numpy.testing import assert_allclose

from ..path import Path


def test_line_sampling():

    d, x, y = Path(zip([0., 0.], [0., 3.4])).sample_points_edges(spacing=1.0)

    assert_allclose(d, [0., 1., 2., 3.])
    assert_allclose(x, [0., 0., 0., 0.])
    assert_allclose(y, [0., 1., 2., 3.])

    d, x, y = Path(zip([0., 0., 0.], [0., 2.0, 3.4])).sample_points_edges(spacing=1.0)

    assert_allclose(d, [0., 1., 2., 3.])
    assert_allclose(x, [0., 0., 0., 0.])
    assert_allclose(y, [0., 1., 2., 3.])

    d, x, y = Path(zip([0., 0., 0.], [0., 2.0, 3.4])).sample_points_edges(spacing=2.0)

    assert_allclose(d, [0., 2.])
    assert_allclose(x, [0., 0.])
    assert_allclose(y, [0., 2.])

    d, x, y = Path(zip([0., 3.4], [0., 0.])).sample_points_edges(spacing=1.0)

    assert_allclose(d, [0., 1., 2., 3.])
    assert_allclose(x, [0., 1., 2., 3.])
    assert_allclose(y, [0., 0., 0., 0.])

    d, x, y = Path(zip([0., 2.0, 3.4], [0., 0., 0.])).sample_points_edges(spacing=1.0)

    assert_allclose(d, [0., 1., 2., 3.])
    assert_allclose(x, [0., 1., 2., 3.])
    assert_allclose(y, [0., 0., 0., 0.])

    d, x, y = Path(zip([0., 2.0, 3.4], [0., 0., 0.])).sample_points_edges(spacing=2.0)

    assert_allclose(d, [0., 2.])
    assert_allclose(x, [0., 2.])
    assert_allclose(y, [0., 0.])
