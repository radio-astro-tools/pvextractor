import numpy as np
from astropy.utils.console import ProgressBar

from .polygon import square_polygon_overlap_area

def extract_poly_slice(cube, polygons, width=1.0):

    nx = len(polygons)
    nz = cube.shape[0]

    slice = np.zeros((nz, nx))

    p = ProgressBar(len(polygons))

    for i, polygon in enumerate(polygons):

        p.update()

        # Find bounding box
        bbxmin = int(round(np.min(polygon.x))-1)
        bbxmax = int(round(np.max(polygon.x))+2)
        bbymin = int(round(np.min(polygon.y))-1)
        bbymax = int(round(np.max(polygon.y))+2)

        # Loop through pixels that might overlap
        for xmin in np.arange(bbxmin, bbxmax):
            for ymin in np.arange(bbymin, bbymax):

                area = square_polygon_overlap_area(xmin-0.5, xmin+0.5,
                                                   ymin-0.5, ymin+0.5,
                                                   polygon.x, polygon.y)

                if area > 0:
                    slice[:, i] += cube[:, ymin, xmin] * area

    print ""

    return slice
