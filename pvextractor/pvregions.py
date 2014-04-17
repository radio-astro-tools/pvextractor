import numpy as np
from .geometry import path
from astropy import coordinates
from astropy import units as u

csystems = {'galactic':coordinates.Galactic,
            'fk5':coordinates.FK5,
            'fk4':coordinates.FK4,
            'icrs':coordinates.ICRS}

def pv_from_regfile(regfile):
    """
    Given a ds9 region file, extract pv diagrams for each:
        group of points [NOT IMPLEMENTED]
        panda [NOT IMPLEMENTED]
        vector [NOT IMPLEMENTED]
        segment [NOT IMPLEMENTED]
        group of lines [NOT IMPLEMENTED]
    """
    import pyregion
    return pyregion.open(regfile)

def pv_from_region(region):
    """
    Given a pyregion shape object, extract a pv diagram
    """

    l,b = None,None

    endpoints = []
    otherpars = []

    for x in region.params:
        if 'HMS' in str(type(x)):
            if region.coord_format == 'celestial':
                l = x.degree
            else:
                l = x.v
            continue
        elif 'DMS' in str(type(x)):
            b = x.v
            if l is not None and b is not None:
                endpoints.append[(l,b)]
                l,b = None,None
            else:
                raise ValueError("unmatched l,b")
        else:
            otherpars.append(x)

    lbarr = np.array(endpoints)
    C = csystems[region.coord_format](lbarr[:,0]*u.deg, lbarr[:,1]*u.deg)

    p = path.WCSPath(C)

    return p
