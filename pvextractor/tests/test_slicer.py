import numpy as np

from astropy.io import fits

from ..pvextractor import extract_pv_slice_hdu
from ..geometry.path import Path

# Use a similar header as in the spectral_cube package
HEADER_STR = """
SIMPLE  =                    T / Written by IDL:  Fri Feb 20 13:46:36 2009
BITPIX  =                  -32  /
NAXIS   =                    4  /
NAXIS1  =                    3  /
NAXIS2  =                    4  /
NAXIS3  =                    5  /
NAXIS4  =                    1  /
EXTEND  =                    T  /
BSCALE  =    1.00000000000E+00  /
BZERO   =    0.00000000000E+00  /
BLANK   =                   -1  /
TELESCOP= 'VLA     '  /
CDELT1  =   -5.55555561268E-04  /
CRPIX1  =    1.37300000000E+03  /
CRVAL1  =    2.31837500515E+01  /
CTYPE1  = 'RA---SIN'  /
CDELT2  =    5.55555561268E-04  /
CRPIX2  =    1.15200000000E+03  /
CRVAL2  =    3.05765277962E+01  /
CTYPE2  = 'DEC--SIN'  /
CDELT3  =    1.28821496879E+03  /
CRPIX3  =    1.00000000000E+00  /
CRVAL3  =   -3.21214698632E+05  /
CTYPE3  = 'VELO-HEL'  /
CDELT4  =    1.00000000000E+00  /
CRPIX4  =    1.00000000000E+00  /
CRVAL4  =    1.00000000000E+00  /
CTYPE4  = 'STOKES  '  /
DATE-OBS= '1998-06-18T16:30:25.4'  /
RESTFREQ=    1.42040571841E+09  /
CELLSCAL= 'CONSTANT'  /
BUNIT   = 'JY/BEAM '  /
EPOCH   =    2.00000000000E+03  /
OBJECT  = 'M33     '           /
OBSERVER= 'AT206   '  /
VOBS    =   -2.57256763070E+01  /
LTYPE   = 'channel '  /
LSTART  =    2.15000000000E+02  /
LWIDTH  =    1.00000000000E+00  /
LSTEP   =    1.00000000000E+00  /
BTYPE   = 'intensity'  /
DATAMIN =   -6.57081836835E-03  /
DATAMAX =    1.52362231165E-02  /"""


def make_test_hdu():
    header = fits.header.Header.fromstring(HEADER_STR, sep='\n')
    hdu = fits.PrimaryHDU(header=header)
    import numpy as np
    np.random.seed(12345)
    hdu.data = np.random.random(60).reshape(1,5,4,3)
    return hdu


def test_pv_slice_hdu_line_path_order_0():
    hdu = make_test_hdu()
    path = Path([(0., 0.), (3., 3.), (6., 4.)])
    slice_hdu = extract_pv_slice_hdu(hdu, path, spacing=1., order=0)


def test_pv_slice_hdu_line_path_order_3():
    hdu = make_test_hdu()
    path = Path([(0., 0.), (3., 3.), (6., 4.)])
    slice_hdu = extract_pv_slice_hdu(hdu, path, spacing=1., order=3)


def test_pv_slice_hdu_poly_path():
    hdu = make_test_hdu()
    path = Path([(0., 0.), (3., 3.), (6., 4.)], width=0.001)
    slice_hdu = extract_pv_slice_hdu(hdu, path, spacing=1.)
