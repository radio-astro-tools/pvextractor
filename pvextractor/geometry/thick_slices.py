import numpy as np
from astropy.io import fits



def extract_thick_slice(cube, x, y, width=1.0):

    from shapely.geometry import Polygon

    # Pad with same values at ends, to find slope of perpendicular end lines.
    xp = np.pad(x, 1, mode='edge')
    yp = np.pad(y, 1, mode='edge')

    # Find slope connecting alternating points
    m = -(xp[2:] - xp[:-2]) / (yp[2:] - yp[:-2])
    b = y - m * x

    # Find angle of the intersecting lines
    alpha = np.arctan2(xp[2:] - xp[:-2], yp[:-2] - yp[2:])

    dx = np.cos(alpha)
    dy = np.sin(alpha)

    # Find points offset from main curve, on bisecting lines
    x1 = x - dx * width * 0.5
    x2 = x + dx * width * 0.5
    y1 = y - dy * width * 0.5
    y2 = y + dy * width * 0.5

    # Now loop over all the polygons for the slice

    nx = len(x)
    nz = cube.shape[0]

    slice = np.zeros((nz, nx-1))

    for i in range(len(x)-1):

        # Define polygon for curve chunk
        xp = [x1[i], x1[i+1], x2[i+1], x2[i]]
        yp = [y1[i], y1[i+1], y2[i+1], y2[i]]
        p_chunk = Polygon(zip(xp, yp))

        # Find bounding box
        bbxmin = int(round(np.min(xp))-1)
        bbxmax = int(round(np.max(xp))+1)
        bbymin = int(round(np.min(yp))-1)
        bbymax = int(round(np.max(yp))+1)

        # Loop through pixels that might overlap
        for xmin in np.arange(bbxmin, bbxmax):
            for ymin in np.arange(bbymin, bbymax):

                p_pixel = Polygon([(xmin-0.5, ymin-0.5), (xmin+0.5, ymin-0.5),
                                   (xmin+0.5, ymin+0.5), (xmin-0.5, ymin+0.5)])

                p_int = p_chunk.intersection(p_pixel)

                if p_int.area > 0:
                    slice[:, i] += cube[:, ymin, xmin] * p_int.area

    return slice
