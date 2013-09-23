def flatten_header(header):
    """
    Attempt to turn an N-dimensional fits header into a 2-dimensional header
    Turns all CRPIX[>2] etc. into new keywords with suffix 'A'

    header must be a pyfits.Header or astropy.io.fits.Header instance
    """

    # astropy.io.fits != pyfits -> sadness
    #if not hasattr(header,'copy')
    #    raise Exception("flatten_header requires a pyfits.Header instance")

    newheader = header.copy()

    for key in newheader.keys():
        try:
            if int(key[-1]) >= 3 and key[:2] in ['CD','CR','CT','CU','NA']:
                newheader.rename_key(key,'A'+key,force=True)
        except ValueError:
            # if key[-1] is not an int
            pass
        except IndexError:
            # if len(key) < 2
            pass
    newheader.update('NAXIS',2)

    return newheader
