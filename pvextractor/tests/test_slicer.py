import numpy as np
from numpy.testing import assert_allclose

from astropy.io import fits
import pytest
from astropy.wcs import WCS

from ..pvextractor import extract_pv_slice
from ..geometry.path import Path

# Use a similar header as in the spectral_cube package
HEADER_STR = """
SIMPLE  =                    T  /
BITPIX  =                  -32  /
NAXIS   =                    3  /
NAXIS1  =                    3  /
NAXIS2  =                    4  /
NAXIS3  =                    5  /
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
DATE-OBS= '1998-06-18T16:30:25.4'  /
RESTFREQ=    1.42040571841E+09  /
CELLSCAL= 'CONSTANT'  /
BUNIT   = 'K'  /
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

SLICE_HEADER = """
SIMPLE  =                    T / conforms to FITS standard
BITPIX  =                  -64 / array data type
NAXIS   =                    2 / number of array dimensions
NAXIS1  =                   10
NAXIS2  =                    5
WCSAXES =                    2 / Number of coordinate axes
CRPIX1  =                  1.0 / Pixel coordinate of reference point
CRPIX2  =                  1.0 / Pixel coordinate of reference point
CDELT1  =    0.000222222224507 / [deg] Coordinate increment at reference point
CDELT2  =        1288.21496879 / [m s-1] Coordinate increment at reference point
CUNIT1  = 'deg'                / Units of coordinate increment and value
CUNIT2  = 'm/s'                / Units of coordinate increment and value
CTYPE1  = 'OFFSET'             / Coordinate type code
CTYPE2  = 'VOPT'               / Optical velocity (linear)
CRVAL1  =                  0.0 / [deg] Coordinate value at reference point
CRVAL2  =       -321214.698632 / [m s-1] Coordinate value at reference point
LONPOLE =                180.0 / [deg] Native longitude of celestial pole
LATPOLE =        30.5765277962 / [deg] Native latitude of celestial pole
RESTFRQ =        1420405718.41 / [Hz] Line rest frequency
SPECSYS = 'BARYCENT'           / Reference frame of spectral coordinates
MJD-OBS =         50982.687794 / [d] MJD of observation matching DATE-OBS
DATE-OBS= '1998-06-18T16:30:25.4' / ISO-8601 observation date matching MJD-OBS
"""


def make_test_hdu():
    header = fits.header.Header.fromstring(HEADER_STR, sep='\n')
    hdu = fits.PrimaryHDU(header=header)
    import numpy as np
    hdu.data = np.zeros((5, 4, 3))
    hdu.data[:, 0, :] = 1.
    hdu.data[:, 2, :] = 2.
    hdu.data[:, 3, :] = np.nan
    return hdu


def make_test_fits_file(tmp_path):
    hdu = make_test_hdu()
    filename = tmp_path / 'example.fits'
    hdu.writeto(filename)
    return filename


def make_test_spectralcube():
    header = fits.header.Header.fromstring(HEADER_STR, sep='\n')
    assert header['NAXIS']==3
    hdu = make_test_hdu()
    assert hdu.header['NAXIS']==3
    import spectral_cube.io.fits
    cube = spectral_cube.io.fits.load_fits_cube(hdu)
    assert cube.unit == 'K'
    return cube


def make_test_data_wcs():
    cube = make_test_spectralcube()
    return cube.filled_data[:], cube.wcs


@pytest.mark.parametrize('data', (make_test_hdu(), make_test_spectralcube()))
class TestExtraction:

    def test_pv_slice_hdu_line_path_order_0(self, data):
        path = Path([(1., -0.5), (1., 3.5)])
        slice_hdu = extract_pv_slice(data, path, spacing=0.4, order=0)
        assert_allclose(slice_hdu.data[0], np.array([1., 1., 0., 0., 0., 2., 2., 2., np.nan, np.nan]))

    def test_pv_slice_hdu_line_path_order_3(self, data):
        path = Path([(1., -0.5), (1., 3.5)])
        slice_hdu = extract_pv_slice(data, path, spacing=0.4, order=3)
        assert_allclose(slice_hdu.data[0], np.array([np.nan, 0.9648, 0.4, -0.0368, 0.5622,
                                                     1.6478, 1.9278, np.nan, np.nan, np.nan]))

    def test_pv_slice_hdu_poly_path(self, data):
        path = Path([(1., -0.5), (1., 3.5)], width=0.001)
        slice_hdu = extract_pv_slice(data, path, spacing=0.4)
        assert_allclose(slice_hdu.data[0], np.array([1., 1., 0.5, 0., 0., 2., 2., 2., np.nan, np.nan]))

    def test_pv_slice_hdu_line_path_order_0_no_nan(self, data):
        path = Path([(1., -0.5), (1., 3.5)])
        slice_hdu = extract_pv_slice(data, path, spacing=0.4, order=0, respect_nan=False)
        assert_allclose(slice_hdu.data[0], np.array([1., 1., 0., 0., 0., 2., 2., 2., 0., 0.]))

    def test_pv_slice_hdu_line_path_order_3_no_nan(self, data):
        path = Path([(1., -0.5), (1., 3.5)])
        slice_hdu = extract_pv_slice(data, path, spacing=0.4, order=3, respect_nan=False)
        assert_allclose(slice_hdu.data[0], np.array([np.nan, 0.9648, 0.4, -0.0368, 0.5622,
                                                     1.6478, 1.9278, 0.975, 0.0542, np.nan]))

    def test_pv_slice_hdu_poly_path_no_nan(self, data):
        path = Path([(1., -0.5), (1., 3.5)], width=0.001)
        slice_hdu = extract_pv_slice(data, path, spacing=0.4, respect_nan=False)
        assert_allclose(slice_hdu.data[0], np.array([1., 1., 0.5, 0., 0., 2., 2., 1., 0., 0.]))


@pytest.mark.parametrize('make_data', (make_test_hdu, make_test_spectralcube, make_test_data_wcs))
def test_output_wcs(make_data):

    data = make_data()

    if isinstance(data, tuple):
        data, wcs = data
    else:
        wcs = None

    path = Path([(1., -0.5), (1., 3.5)])

    slice_hdu = extract_pv_slice(data, path, wcs=wcs, spacing=0.4, order=0)

    assert_allclose(slice_hdu.data[0], np.array([1., 1., 0., 0., 0., 2., 2., 2., np.nan, np.nan]))

    reference = fits.header.Header.fromstring(SLICE_HEADER.strip(), sep='\n')
    for key in reference:
        try:
            # for floats, test that they're close because wcsutils is not always
            # consistent between versions
            np.testing.assert_almost_equal(slice_hdu.header[key], reference[key])
        except TypeError:
            assert slice_hdu.header[key] == reference[key]
