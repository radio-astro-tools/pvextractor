import numpy as np
from .geometry import path
from astropy import coordinates
from astropy import units as u

csystems = {'galactic':coordinates.Galactic,
            'fk5':coordinates.FK5,
            'fk4':coordinates.FK4,
            'icrs':coordinates.ICRS}

valid_regions = ['line','segment']

def paths_from_regfile(regfile, wcs=None):
    """
    Given a ds9 region file, extract pv diagrams for each:
        group of points [NOT IMPLEMENTED]
        panda [NOT IMPLEMENTED]
        vector [NOT IMPLEMENTED]
        segment [NOT IMPLEMENTED]
        group of lines [NOT IMPLEMENTED]
    """
    import pyregion
    regions = pyregion.open(regfile)
    paths = [paths_from_region(r, wcs=wcs)
             for r in regions
             if r.name in valid_regions]
    return paths

def paths_from_region(region, wcs=None):
    """
    Given a pyregion shape object, extract a pv diagram
    """

    l,b = None,None

    endpoints = []
    otherpars = []

    for x in region.params:
        if 'HMS' in str(type(x)) or 'Number' in str(type(x)) and l is None:
            if region.coord_format == 'celestial':
                l = x.degree
            else:
                l = x.v
        elif 'DMS' in str(type(x)) or 'Number' in str(type(x)):
            b = x.v
            if l is not None and b is not None:
                endpoints.append((l,b))
                l,b = None,None
            else:
                raise ValueError("unmatched l,b")
        else:
            otherpars.append(x)

    lbarr = np.array(endpoints)
    C = csystems[region.coord_format](lbarr[:,0]*u.deg, lbarr[:,1]*u.deg)

    # TODO: add widths for projection

    p = path.WCSPath(C, wcs=wcs)

    return p
