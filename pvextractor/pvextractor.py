import numpy as np
from scipy.ndimage import map_coordinates

def pvdiagram(cube, endpoints=(), spacing=1.0, interpolation='spline', order=3):
    """
    Given a datacube with dimensions [z,y,x], accepts a 2xN tuple with N [x,y]
    endpoints.

    All units are in *pixels*

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
        for ii,(x,y) in enumerate(zip(xinds,yinds)):
            if interpolation == 'nearest':
                pvd[:,ii] = cube[:,y,x]
            elif interpolation == 'spline':
                pvd[:,ii] = map_coordinates(cube,
                                            [velinds, [y]*nvel, [x]*nvel],
                                            order=order)
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
