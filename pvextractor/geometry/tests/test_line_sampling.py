from numpy.testing import assert_allclose

from ..line_sampling import sample_curve


def test_line_sampling():

    d, x, y = sample_curve([0., 0.], [0., 3.4], spacing=1.0)

    assert_allclose(d, [0., 1., 2., 3., 4.])
    assert_allclose(x, [0., 0., 0., 0., 0.])
    assert_allclose(y, [-0.3, 0.7, 1.7, 2.7, 3.7])

    d, x, y = sample_curve([0., 0., 0.], [0., 2.0, 3.4], spacing=1.0)

    assert_allclose(d, [0., 1., 2., 3., 4.])
    assert_allclose(x, [0., 0., 0., 0., 0.])
    assert_allclose(y, [-0.3, 0.7, 1.7, 2.7, 3.7])

    d, x, y = sample_curve([0., 0., 0.], [0., 2.0, 3.4], spacing=2.0)

    assert_allclose(d, [0., 2., 4.])
    assert_allclose(x, [0., 0., 0.])
    assert_allclose(y, [-0.3, 1.7, 3.7])

    d, x, y = sample_curve([0., 3.4], [0., 0.], spacing=1.0)

    assert_allclose(d, [0., 1., 2., 3., 4.])
    assert_allclose(x, [-0.3, 0.7, 1.7, 2.7, 3.7])
    assert_allclose(y, [0., 0., 0., 0., 0.])

    d, x, y = sample_curve([0., 2.0, 3.4], [0., 0., 0.], spacing=1.0)

    assert_allclose(d, [0., 1., 2., 3., 4.])
    assert_allclose(x, [-0.3, 0.7, 1.7, 2.7, 3.7])
    assert_allclose(y, [0., 0., 0., 0., 0.])

    d, x, y = sample_curve([0., 2.0, 3.4], [0., 0., 0.], spacing=2.0)

    assert_allclose(d, [0., 2., 4.])
    assert_allclose(x, [-0.3, 1.7, 3.7])
    assert_allclose(y, [0., 0., 0.])
