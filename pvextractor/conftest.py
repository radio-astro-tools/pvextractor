# this contains imports plugins that configure py.test for astropy tests.
# by importing them here in conftest.py they are discoverable by py.test
# no matter how it is invoked within the source tree.
import os
from distutils.version import LooseVersion
from astropy.version import version as astropy_version

if astropy_version < '3.0':
    from astropy.tests.pytest_plugins import *
    del pytest_report_header
else:
    from pytest_astropy_header.display import PYTEST_HEADER_MODULES, TESTED_VERSIONS


def pytest_configure(config):

    config.option.astropy_header = True

    PYTEST_HEADER_MODULES['Astropy'] = 'astropy'
    PYTEST_HEADER_MODULES['regions'] = 'regions'
    PYTEST_HEADER_MODULES['APLpy'] = 'aplpy'

app = None


def pytest_configure(config):
    global app
    try:
        from qtpy.QtWidgets import QApplication
        app = QApplication([''])
    except Exception:
        pass


def pytest_unconfigure(config):
    global app
    if app is not None:
        app.quit()
        app = None
