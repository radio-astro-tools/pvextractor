import numpy as np
from scipy.ndimage import map_coordinates

def pvdiagram(cube, endpoints=(), spacing=1.0, interpolation='spline', order=3,
              respect_nan=False):
    """
    Given a datacube with dimensions [z,y,x], accepts a 2xN tuple with N [x,y]
    endpoints.

    All units are in *pixels*

    .. note:: If there are NaNs in the cube, they will be treated as zeros when
              using spline interpolation.

    Parameters
    ----------
    endpoints: list or tuple
        A list or tuple of x,y pairs, with minimum length 2
    spacing: float
        The number of pixels per point.  Used to scale the hypotenuse of the
        slice.  A smaller number will result in higher sampling.
    interpolation: 'nearest' or 'spline'
        Either use naive nearest-neighbor estimate or scipy's map_coordinates,
        which defaults to a 3rd order spline
    order: int
        Spline interpolation order

    Returns
    -------
    Two arrays: the position-velocity diagram stitched together from a series
    of endpoints and a list of the pixel lengths of the individual slices.

    Raises
    ------
    ValueError if the endpoints are incorrectly specified

    Examples
    --------
    >>> data = np.arange(500).reshape(5,10,10)
    >>> pvdiagram(data, endpoints=[(1,2),(3.5,6.5),(8.2,7.1)])
    (array([[  10.,   22.,   34.,   46.,   57.,   57.,   61.,   65.,   68.],
           [ 110.,  122.,  134.,  146.,  157.,  157.,  161.,  165.,  168.],
           [ 210.,  222.,  234.,  246.,  257.,  257.,  261.,  265.,  268.],
           [ 310.,  322.,  334.,  346.,  357.,  357.,  361.,  365.,  368.],
           [ 410.,  422.,  434.,  446.,  457.,  457.,  461.,  465.,  468.]]),
     [5.1478150704935, 4.738143096192853])

    """

    if len(endpoints) < 2:
        raise ValueError("Must specify at least 2 endpoints")
    if not all(len(e) == 2 for e in endpoints):
        raise ValueError("All endpoints must be x,y tuples")

    nvel = cube.shape[0]
    velinds = np.arange(nvel,dtype='int')

    def make_pv(startx,starty,endx,endy,npts):
        pvd = np.empty([nvel,npts])
        xinds = np.linspace(startx,endx,npts)
        yinds = np.linspace(starty,endy,npts)
        if interpolation == 'nearest':
            for ii,(x,y) in enumerate(zip(xinds,yinds)):
                    pvd[:,ii] = cube[:,y,x]
        elif interpolation == 'spline':
            vi = np.outer(velinds, np.ones(npts))
            xi = np.outer(np.ones(nvel), xinds)
            yi = np.outer(np.ones(nvel), yinds)
            pvd = map_coordinates(np.nan_to_num(cube), [vi,yi,xi], order=order)
            if respect_nan:
                pvbad = map_coordinates(np.nan_to_num(np.isnan(cube)),
                                        [vi,yi,xi], order=order)
                pvd[pvbad > 0] = np.nan
        return pvd

    pvs = []
    nptsarr = []

    # loop through endpoints
    for ii,((sx,sy),(ex,ey)) in enumerate(zip(endpoints[:-1],endpoints[1:])):
        dx = (ex-sx)
        dy = (ey-sy)
        npts = (dx**2 + dy**2)**0.5 / spacing
        pv = make_pv(endx=ex-1,endy=ey-1,startx=sx-1,starty=sy-1,npts=npts)
        pvs.append(pv)
        nptsarr.append(npts)

    return np.hstack(pvs), nptsarr
