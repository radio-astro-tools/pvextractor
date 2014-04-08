import numpy as np
from astropy import units as u

def get_pixel_scales(wcs, assert_square=True):
    # borrowed from aplpy
    cdelt = np.matrix(wcs.wcs.get_cdelt())
    pc = np.matrix(wcs.wcs.get_pc())
    scale = np.array(cdelt * pc)
    
    if (assert_square and
        (cdelt[0] != cdelt[1] or
         pc[0,0] != pc[1,1] or
         abs(scale[0] != abs(scale[1])))):
        raise ValueError("Non-square pixels.  Please resample data.")

    return abs(scale[0])

def assert_independent_3rd_axis(wcs):
    pc = np.matrix(wcs.wcs.get_pc())
    if (pc[:,2].sum() != pc[2,2] or pc[2,:].sum() != pc[2,2]):
        raise ValueError("Non-independent 3rd axis.")
    axtypes = wcs.get_axis_types()
    if (axtypes[0]['coordinate_type'] != 'celestial' or
        axtypes[1]['coordinate_type'] != 'celestial' or
        axtypes[2]['coordinate_type'] != 'spectral'):
        raise ValueError("Cube axes not in expected orientation: PPV")

def wcs_spacing(wcs, spacing):

    if spacing is not None:
        if hasattr(spacing,'unit'):
            if not spacing.unit.is_equivalent(u.arcsec):
                raise TypeError("Spacing is not in angular units.")
            else:
                platescale = get_pixel_scales(wcs)
                newspacing = spacing.to(u.deg).value / platescale
    else:
        newspacing = spacing

    return newspacing
