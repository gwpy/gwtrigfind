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

"""Utility to find files archived by GW event trigger generators
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
install_requires = ['astropy', 'ligo-segments']
tests_require = ['pytest']
if {'pytest', 'test'}.intersection(sys.argv):
    setup_requires.append('pytest_runner')

# add sphinx integration
if {'build_sphinx'}.intersection(sys.argv):
    setup_requires.extend((
        'sphinx',
        'sphinx_rtd_theme',
        'sphinx_automodapi',
        'sphinx_tabs',
        'numpydoc',
    ))
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc

# get long description from README
with open('README.md', 'rb') as f:
    longdesc = f.read().decode().strip()

# run setup
setup(name='gwtrigfind',
      provides=['gwtrigfind'],
      version=__version__,
      description=__doc__.strip(),
      long_description=longdesc,
      long_description_content_type='text/markdown',
      author='Duncan Macleod',
      author_email='duncan.macleod@ligo.org',
      cmdclass=cmdclass,
      packages=packages,
      scripts=scripts,
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
      setup_requires=setup_requires,
      install_requires=install_requires,
      tests_require=tests_require,
      entry_points={'console_scripts': [
          'gwtrigfind=gwtrigfind.__main__:main',
      ]},
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics',
      ],
      )
