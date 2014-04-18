#!/usr/bin/env python

import sys

if 'develop' in sys.argv or 'build_sphinx' in sys.argv:
    from setuptools import setup, Command
else:
    from distutils.core import setup, Command

with open('README.md') as file:
    long_description = file.read()

#with open('CHANGES') as file:
#    long_description += file.read()

# no versions yet from ???? import __version__ as version

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

#execfile('pvextractor/version.py')

setup(name='pvextractor',
      version=0.0, #__version__,
      description='Position-velocity diagram extractor.',
      long_description=long_description,
      author='Adam Ginsburg',
      author_email='adam.g.ginsburg@gmail.com',
      url='https://github.com/keflavich/pvextractor',
      packages=['pvextractor','pvextractor/utils'],
      cmdclass={'test': PyTest},
      scripts=['scripts/ds9_pvextract.py'],
      )
