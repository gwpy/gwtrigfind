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

"""Setup for GWTrigFind
"""

import glob
import os.path
import sys

from setuptools import (setup, find_packages)
import versioneer

PY_VERSION = sys.version_info
__version__ = versioneer.get_version()

# collect package data
cmdclass = versioneer.get_cmdclass()
packages = find_packages()
scripts = glob.glob(os.path.join('bin', '*'))

# declare dependencies
setup_requires = ['setuptools']
install_requires = ['python-dateutil', 'ligo-segments', 'lalsuite']
tests_require = ['pytest']
if {'pytest', 'test'}.intersection(sys.argv):
    setup_requires.append('pytest_runner')


# run setup
setup(name='gwtrigfind',
      provides=['gwtrigfind'],
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
      tests_require=tests_require,
      entry_points={'console_scripts': [
          'gwtrigfind=gwtrigfind.__main__:main',
          'gwtrigfind{0.major}=gwtrigfind.__main__:main'.format(PY_VERSION),
          'gwtrigfind{0.major}.{0.minor}=gwtrigfind.__main__:main'.format(
              PY_VERSION),
      ]},
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
