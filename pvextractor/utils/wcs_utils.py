import numpy as np
from astropy import units as u
from astropy.wcs import WCSSUB_CELESTIAL, WCSSUB_SPECTRAL
from astropy.wcs.utils import proj_plane_pixel_scales


def get_spatial_scale(wcs, assert_square=True):

    # Code initially adapted from APLpy

    wcs = wcs.sub([WCSSUB_CELESTIAL])
    scale = proj_plane_pixel_scales(wcs)

    if assert_square:
        try:
            np.testing.assert_almost_equal(scale[0], scale[1])
        except AssertionError:
            raise ValueError("Non-square pixels.  Please resample data.")

    return scale[0] * u.Unit(wcs.wcs.cunit[0])


def get_spectral_scale(wcs):

    # Code adapted from APLpy

    wcs = wcs.sub([WCSSUB_SPECTRAL])
    cdelt = np.matrix(wcs.wcs.get_cdelt())
    pc = np.matrix(wcs.wcs.get_pc())
    scale = np.array(cdelt * pc)

    return abs(scale[0,0]) * u.Unit(wcs.wcs.cunit[0])


def sanitize_wcs(mywcs):
    pc = np.matrix(mywcs.wcs.get_pc())
    if (pc[:,2].sum() != pc[2,2] or pc[2,:].sum() != pc[2,2]):
        raise ValueError("Non-independent 3rd axis.")
    axtypes = mywcs.get_axis_types()
    if ((axtypes[0]['coordinate_type'] != 'celestial' or
         axtypes[1]['coordinate_type'] != 'celestial' or
         axtypes[2]['coordinate_type'] != 'spectral')):
        cunit3 = mywcs.wcs.cunit[2]
        ctype3 = mywcs.wcs.ctype[2]
        if cunit3 != '':
            cunit3 = u.Unit(cunit3)
            if cunit3.is_equivalent(u.m/u.s):
                mywcs.wcs.ctype[2] = 'VELO'
            elif cunit3.is_equivalent(u.Hz):
                mywcs.wcs.ctype[2] = 'FREQ'
            elif cunit3.is_equivalent(u.m):
                mywcs.wcs.ctype[2] = 'WAVE'
            else:
                raise ValueError("Could not determine type of 3rd axis.")
        elif ctype3 != '':
            if 'VELO' in ctype3:
                mywcs.wcs.ctype[2] = 'VELO'
            elif 'FELO' in ctype3:
                mywcs.wcs.ctype[2] = 'VELO-F2V'
            elif 'FREQ' in ctype3:
                mywcs.wcs.ctype[2] = 'FREQ'
            elif 'WAVE' in ctype3:
                mywcs.wcs.ctype[2] = 'WAVE'
            else:
                raise ValueError("Could not determine type of 3rd axis.")
        else:
            raise ValueError("Cube axes not in expected orientation: PPV")
    return mywcs


