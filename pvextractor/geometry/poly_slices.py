import numpy as np
from astropy.io import fits
from astropy.utils.console import ProgressBar

def extract_poly_slice(cube, polygons, width=1.0):

    from shapely.geometry import Polygon

    nx = len(polygons)
    nz = cube.shape[0]

    slice = np.zeros((nz, nx))

    p = ProgressBar(len(polygons))

    for i, polygon in enumerate(polygons):

        p.update()

        # Define polygon for curve chunk
        p_chunk = Polygon(zip(polygon.x, polygon.y))

        # TODO: at the moment polygons may be overlapping

        if not p_chunk.is_valid:
            p_chunk = p_chunk.convex_hull

        # Find bounding box
        bbxmin, bbymin, bbxmax, bbymax = p_chunk.bounds
        bbxmin = int(round(bbxmin)-1)
        bbxmax = int(round(bbxmax)+2)
        bbymin = int(round(bbymin)-1)
        bbymax = int(round(bbymax)+2)

        # Loop through pixels that might overlap
        for xmin in np.arange(bbxmin, bbxmax):
            for ymin in np.arange(bbymin, bbymax):

                p_pixel = Polygon([(xmin-0.5, ymin-0.5), (xmin+0.5, ymin-0.5),
                                   (xmin+0.5, ymin+0.5), (xmin-0.5, ymin+0.5)])

                p_int = p_chunk.intersection(p_pixel)

                if p_int.area > 0:
                    slice[:, i] += cube[:, ymin, xmin] * p_int.area

    print ""

    return slice
