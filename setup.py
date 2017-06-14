#!/usr/bin/env python
# Copyright (C) 2016 Duncan Macleod
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""setup for trigfind
"""

import glob
import os.path
import sys

from setuptools import (setup, find_packages)
import versioneer

__version__ = versioneer.get_version()

# collect package data
cmdclass = versioneer.get_cmdclass()
packages = find_packages()
scripts = glob.glob(os.path.join('bin', '*'))

# declare dependencies
setup_requires = ['setuptools', 'pytest-runner']
install_requires = ['lscsoft-glue>=1.56', 'python-dateutil']
requires = ['glue', 'dateutil']
tests_require = ['pytest']
if sys.version_info < (2, 7):
    tests_require.append('unittest2')

# run setup
setup(name='trigfind',
      provides=['trigfind'],
      version=__version__,
      description='Utility to find files archived by GW event trigger '
                  'generators',
      author='Duncan Macleod',
      author_email='duncan.macleod@ligo.org',
      cmdclass=cmdclass,
      packages=packages,
      scripts=scripts,
      setup_requires=setup_requires,
      install_requires=install_requires,
      requires=requires,
      tests_require=tests_require,
      use_2to3=False,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
      )
