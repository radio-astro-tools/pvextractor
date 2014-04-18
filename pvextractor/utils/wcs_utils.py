import numpy as np
from astropy import units as u
from astropy import wcs

def get_pixel_scales(mywcs, assert_square=True):
    # borrowed from aplpy
    cdelt = np.matrix(mywcs.wcs.get_cdelt())
    pc = np.matrix(mywcs.wcs.get_pc())
    scale = np.array(cdelt * pc)
    
    if (assert_square and
        (abs(cdelt[0,0]) != abs(cdelt[0,1]) or
         abs(pc[0,0]) != abs(pc[1,1]) or
         abs(scale[0,0]) != abs(scale[0,1]))):
        raise ValueError("Non-square pixels.  Please resample data.")

    return abs(scale[0,0])

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
            if 'VELO' in ctype3 or 'FELO' in ctype3:
                mywcs.wcs.ctype[2] = 'VELO'
            elif 'FREQ' in ctype3:
                mywcs.wcs.ctype[2] = 'FREQ'
            elif 'WAVE' in ctype3:
                mywcs.wcs.ctype[2] = 'WAVE'
            else:
                raise ValueError("Could not determine type of 3rd axis.")
        else:
            raise ValueError("Cube axes not in expected orientation: PPV")
    return mywcs

def wcs_spacing(mywcs, spacing):
    """
    Return spacing in pixels

    Parameters
    ----------
    wcs : `~astropy.wcs.WCS`
    spacing : `~astropy.units.Quantity` or float
    """

    if spacing is not None:
        if hasattr(spacing,'unit'):
            if not spacing.unit.is_equivalent(u.arcsec):
                raise TypeError("Spacing is not in angular units.")
            else:
                platescale = get_pixel_scales(mywcs)
                newspacing = spacing.to(u.deg).value / platescale
        else:
            # if no units, assume pixels already
            newspacing = spacing
    else:
        # if no spacing, return pixscale
        newspacing = 1

    return newspacing

def pixel_to_wcs_spacing(mywcs, pspacing):
    """
    Return spacing in degrees

    Parameters
    ----------
    wcs : `~astropy.wcs.WCS`
    spacing : float
    """
    platescale = get_pixel_scales(mywcs)
    wspacing = platescale * pspacing * u.deg
    return wspacing

def get_wcs_system_name(mywcs):
    """TODO: move to astropy.wcs.utils"""
    ct = mywcs.sub([wcs.WCSSUB_CELESTIAL]).wcs.ctype
    if 'GLON' in ct[0]:
        return 'galactic'
    elif 'RA' in ct[0]:
        return 'icrs'
    else:
        raise ValueError("Unrecognized coordinate system")
