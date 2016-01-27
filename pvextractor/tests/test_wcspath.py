import os

import pytest
import numpy as np
from astropy import wcs
from astropy.io import fits

from .. import pvregions


def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    return os.path.join(data_dir, filename)


@pytest.mark.xfail
@pytest.mark.parametrize('regfile', ('tests.reg', 'tests_fk5.reg'))
def test_wcspath(regfile):
    p1,p2 = pvregions.paths_from_regfile(data_path(regfile))
    w = wcs.WCS(fits.Header.fromtextfile(data_path('w51.hdr')))
    p1.set_wcs(w)

    shouldbe = (61.593585, 75.950471, 88.911616, 72.820463, 96.025686,
                88.470505, 113.95314, 95.868707, 186.80123, 76.235017,
                226.35546, 100.99054)
    xy = (np.array(zip(shouldbe[::2],shouldbe[1::2])) - 1)
    np.testing.assert_allclose(np.array((p1.xy)), xy, rtol=1e-5)

"""
TODO:
    fix this test

/Users/adam/anaconda/envs/astropy35/lib/python3.5/site-packages/numpy/core/function_base.py:115: ValueError
______________________________________________________________________________________________ test_wcspath[tests.reg] _______________________________________________________________________________________________

regfile = 'tests.reg'

    @pytest.mark.parametrize('regfile', ('tests.reg', 'tests_fk5.reg'))
    def test_wcspath(regfile):
>       p1,p2 = pvregions.paths_from_regfile(data_path(regfile))
E       ValueError: too many values to unpack (expected 2)

pvextractor/tests/test_wcspath.py:18: ValueError
____________________________________________________________________________________________ test_wcspath[tests_fk5.reg] _____________________________________________________________________________________________

regfile = 'tests_fk5.reg'

    @pytest.mark.parametrize('regfile', ('tests.reg', 'tests_fk5.reg'))
    def test_wcspath(regfile):
>       p1,p2 = pvregions.paths_from_regfile(data_path(regfile))
E       ValueError: too many values to unpack (expected 2)
"""
