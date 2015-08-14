# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This is an Astropy affiliated package.
"""

# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *
# ----------------------------------------------------------------------------

if not _ASTROPY_SETUP_:

    from . import utils
    from .pvextractor import extract_pv_slice
    from .utils.wcs_slicing import slice_wcs
    from .geometry import Path, PathFromCenter
    from .pvregions import paths_from_regfile
