# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2016)
#
# This file is part of Trigfind.
#
# Trigfind is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Trigfind is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Trigfind.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for trigfind
"""

import os.path
import glob
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from glue.lal import (Cache, CacheEntry)
from glue.segments import segment as Segment

import trigfind
from trigfind import core

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'


# -- mock methods -------------------------------------------------------------

def realpath(f):
    return f

os.path.realpath = realpath  # mock realpath for testing


def mock_iglob_factory(fileformat):
    def mock_gps_glob(globstr):
        parent = os.path.split(globstr)[0]
        while True:
            globstr = os.path.split(globstr)[0]
            try:
                gps5 = int(os.path.basename(globstr).rsplit('-')[-1])
            except ValueError:
                pass
            else:
                break
        ngps = len(str(gps5))
        gpsstart = gps5 * 10**ngps
        gpsend = (gps5 + 1) * 10**ngps
        d = int(10 ** ngps // 10)
        t = gpsstart
        while t < gpsend:
            f = os.path.join(parent, fileformat.format(t, d))
            print(f)
            t += d
            yield f
    return mock_gps_glob


def mock_find_detchar_glob(globstr):
    if globstr.lower().endswith('_omicron'):
        return True
    else:
        return list(glob.iglob(globstr))


# -- tests --------------------------------------------------------------------

class TrigfindTestCase(unittest.TestCase):
    def test_regex(self):
        for var in ['daily-cbc', 'daily_cbc']:
            self.assertRegexpMatches(var, core.daily_cbc)
        for var in ['kw', 'kleinewelle', 'KleineWelle']:
            self.assertRegexpMatches(var, core.kleinewelle)
        for var in ['dmtomega', 'dmt-omega', 'dmt_omega', 'DMT Omega']:
            self.assertRegexpMatches(var, core.dmt_omega)
        for var in ['omega', 'omega_online']:
            self.assertRegexpMatches(var, core.omega)

    def test_format_channel_name(self):
        self.assertEqual(core._format_channel_name('X1:TEST-CHANNEL_NAME'),
                         'X1-TEST_CHANNEL_NAME')

    def test_find_trigger_files(self):
        # quick check that this resolves the ETG correctly
        iglob = mock_iglob_factory('L1-GDS_CALIB_STRAIN_OmegaC-{0}-{1}.xml')
        with mock.patch('glob.iglob', iglob):
            cache = trigfind.find_trigger_files(
                'L1:GDS-CALIB_STRAIN', 'dmt-omega', 1135641617, 1135728017)
            self.assertIsInstance(cache, Cache)
            self.assertEqual(len(cache), 9)
            self.assertEqual(cache[0].path,
                             '/gds-l1/dmt/triggers/L-HOFT_Omega/11356/'
                             'L1-GDS_CALIB_STRAIN_OmegaC-1135640000-10000.xml')

    def test_find_dmt_files(self):
        # check error for unknown ETG
        self.assertRaises(NotImplementedError, trigfind.find_dmt_files,
                          None, 0, 100, etg='fake-etg')

    def test_find_dmt_files_dmt_omega(self):
        iglob = mock_iglob_factory('L1-GDS_CALIB_STRAIN_OmegaC-{0}-{1}.xml')
        with mock.patch('glob.iglob', iglob):
            cache = trigfind.find_dmt_files(
                'L1:GDS-CALIB_STRAIN', 1135641617, 1135728017, etg='dmt-omega')
            self.assertIsInstance(cache, Cache)
            self.assertEqual(len(cache), 9)
            self.assertEqual(cache[0].path,
                             '/gds-l1/dmt/triggers/L-HOFT_Omega/11356/'
                             'L1-GDS_CALIB_STRAIN_OmegaC-1135640000-10000.xml')
        # check error for non-hoft channel with DMT-Omega
        self.assertRaises(NotImplementedError, trigfind.find_dmt_files,
                          'X1:TEST', 0, 100, etg='dmt-omega')

    def test_find_dmt_files_kleinewelle(self):
        iglob = mock_iglob_factory('L-KW_TRIGGERS-{0}-{1}.xml')
        with mock.patch('glob.iglob', iglob):
            cache = trigfind.find_dmt_files('L1:TEST-CHANNEL', 1135641617,
                                            1135728017, etg='kleinewelle')
            self.assertIsInstance(cache, Cache)
            self.assertEqual(len(cache), 9)
            self.assertEqual(cache[0].path,
                             '/gds-l1/dmt/triggers/L-KW_TRIGGERS/'
                             'L-KW_TRIGGERS-11356/'
                             'L-KW_TRIGGERS-1135640000-10000.xml')
        # test h(t)
        iglob = mock_iglob_factory('L-KW_HOFT-{0}-{1}.xml')
        with mock.patch('glob.iglob', iglob):
            cache = trigfind.find_dmt_files('L1:GDS-CALIB_STRAIN', 1135641617,
                                            1135728017, etg='kleinewelle')
            self.assertIsInstance(cache, Cache)
            self.assertEqual(len(cache), 9)
            self.assertEqual(cache[0].path,
                             '/gds-l1/dmt/triggers/L-KW_HOFT/'
                             'L-KW_HOFT-11356/L-KW_HOFT-1135640000-10000.xml')

    def test_find_detchar_files(self):
        iglob = mock_iglob_factory('L1-GDS_CALIB_STRAIN_OMICRON-{0}-{1}.xml')
        glob_ = mock_find_detchar_glob
        with mock.patch('glob.iglob', iglob):
            with mock.patch('glob.glob', glob_):
                cache = trigfind.find_detchar_files(
                    'L1:GDS-CALIB_STRAIN', 1135641617, 1135728017,
                    etg='omicron')
                self.assertIsInstance(cache, Cache)
                self.assertEqual(len(cache), 9)
                self.assertEqual(
                    cache[0].path,
                    '/home/detchar/triggers/*/L1/GDS-CALIB_STRAIN_Omicron/'
                    '11356/L1-GDS_CALIB_STRAIN_OMICRON-1135640000-10000.xml')
                cache = trigfind.find_detchar_files(
                    'L1:GDS-CALIB_STRAIN', 1146873617, 1146873617+1,
                    etg='omicron')
                self.assertEqual(
                    cache[0].path,
                    '/home/detchar/triggers/L1/GDS_CALIB_STRAIN_OMICRON/11468/'
                    'L1-GDS_CALIB_STRAIN_OMICRON-1146870000-10000.xml')
        # test error for channel that has never been processed
        self.assertRaises(ValueError, trigfind.find_detchar_files,
                          'X1:DOES-NOT_EXIST:1', 0, 100, etg='fake-etg')

    def test_find_pycbc_live_files(self):
        test_glob = ['H1-Live-1126259148.29-4.hdf',
                     'H1-Live-1126259228.29-4.hdf', 
                     'H1-Live-1126259308.29-4.hdf',
                     'H1-Live-1126259388.29-4.hdf',
                    ]

        # outside times, so no return expected
        try:
            with mock.patch('glob.glob', lambda x: test_glob):
                c = trigfind.find_pycbc_live_files(None, 1135641617, 1135728017)
                self.assertIsInstance(c, Cache)
                self.assertEqual(len(c), 0)

                c = trigfind.find_pycbc_live_files(None, 1126259140, 1126269148)
                self.assertEqual(len(c), 4)
        except ImportError as e:
            self.skipTest(str(e))
            
    def test_find_daily_cbc_files(self):
        # can't do much without faking the entire thing
        try:
            cache = trigfind.find_daily_cbc_files('L1:GDS-CALIB_STRAIN', 0, 100)
        except ImportError as e:
            self.skipTest(str(e))
        else:
            self.assertIsInstance(cache, Cache)

    def test_find_omega_online_files(self):
        iglob = mock_iglob_factory('G1-OMEGA_TRIGGERS_DOWNSELECT-{0}-{1}.txt')
        with mock.patch('glob.iglob', iglob):
            cache = trigfind.find_omega_online_files(
                'G1:DER_DATA_H', 1135641617, 1135728017)
            self.assertIsInstance(cache, Cache)
            self.assertEqual(len(cache), 9)
            self.assertEqual(
                cache[0].path,
                '/home/omega/online/G1_DER_DATA_H/segments/11356/*/'
                'G1-OMEGA_TRIGGERS_DOWNSELECT-1135640000-10000.txt')
        self.assertRaises(NotImplementedError,
                          trigfind.find_omega_online_files, 'L1:TEST-CHANNEL',
                          0, 100)

    def test_find_trigger_urls(self):
        # make sure a DeprecationWarning is presented
        with pytest.warns(DeprecationWarning):
            # simplest test is to throw an error from find_detchar_files
            self.assertRaises(ValueError, trigfind.find_trigger_urls,
                              'X1:DOES-NOT_EXIST:1', 'fake-etg', 0, 100)
