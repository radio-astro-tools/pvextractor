import numpy as np
from .geometry import path
from astropy import coordinates
from astropy import units as u

csystems = {'galactic':coordinates.Galactic,
            'fk5':coordinates.FK5,
            'fk4':coordinates.FK4,
            'icrs':coordinates.ICRS}

def line_to_path(region, wcs=None):
    """
    Convert a line or segment to a path
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

def vector_to_path(vector_region, wcs=None):
    """
    Convert a vector region to a path

    # vector(48.944348,-0.36432694,485.647",124.082) vector=1
    """

    x,y = vector_region.coord_list[:2]
    length = vector_region.coord_list[2] * u.deg
    angle = vector_region.coord_list[3] * u.deg
    
    C1 = csystems[vector_region.coord_format](x*u.deg, y*u.deg)
    tan = np.tan(angle)
    dx,dy = length * tan, length / tan
    C2 = csystems[vector_region.coord_format](C1.lonangle + dx, C1.latangle + dy)

    C = csystems[vector_region.coord_format]([C1.lonangle,C2.lonangle],
                                             [C1.latangle,C2.latangle])

    p = path.WCSPath(C, wcs=wcs)

    return p

region_converters = {'line':line_to_path, 'segment':line_to_path,
                     'vector':vector_to_path}

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
    return paths_from_regions(regions, wcs=wcs)

def paths_from_regions(regions, wcs=None):
    paths = [region_converters[r.name](r, wcs=wcs)
             for r in regions
             if r.name in region_converters]
    return paths
