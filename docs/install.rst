Installing ``pvextractor``
==========================

Requirements
------------

This package has the following dependencies:

* `Python <http://www.python.org>`_ 3.10 or later
* `Numpy <http://www.numpy.org>`_ 1.24 or later
* `Astropy <http://www.astropy.org>`__ 6.1 or later
* `scipy <https://scipy.org>`_ 1.8 or later
* `matplotlib <https://matplotlib.org>`_ 3.5 or later
* `spectral-cube <https://spectral-cube.readthedocs.io>`_ 0.6.7 or later
* `radio-beam <https://radio-beam.readthedocs.io>`_ 0.3.10 or later
* `qtpy <https://github.com/spyder-ide/qtpy>`_ 2.0 or later
* A Qt binding, e.g. `PyQt6 <https://pypi.org/project/PyQt6/>`_, optional
  (required for the GUI)

Installation
------------

To install the latest stable release, you can type::

    pip install pvextractor

To also install PyQt6 for the GUI::

    pip install "pvextractor[viz]"

Developer version
-----------------

If you want to install the latest developer version of the pvextractor code, you
can do so from the git repository::

    git clone https://github.com/radio-astro-tools/pvextractor.git
    cd pvextractor
    pip install -e .

You can also install the latest developer version in a single line with pip::

    pip install git+https://github.com/radio-astro-tools/pvextractor.git
