# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2016)
#
# This file is part of GWTrigFind.
#
# GWTrigFind is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWTrigFind is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWTrigFind.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for gwtrigfind
"""

import glob
import os.path

try:  # python >= 3
    from unittest import mock
    OPEN = 'builtins.open'
except ImportError:  # python < 3
    import mock
    OPEN = '__builtin__.open'

import pytest

from . import core

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'


# -- mock methods -------------------------------------------------------------

def mock_open(*args, **kargs):
  """See https://stackoverflow.com/a/41656192/1307974
  """
  f_open = mock.mock_open(*args, **kargs)
  f_open.return_value.__iter__ = lambda self : iter(self.readline, '')
  return f_open


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
            t += d
            yield f
    return mock_gps_glob


# -- tests --------------------------------------------------------------------

@pytest.mark.parametrize('var, regex', [
    ('daily-cbc', core.daily_cbc),
    ('daily_cbc', core.daily_cbc),
    ('kw', core.kleinewelle),
    ('kleinewelle', core.kleinewelle),
    ('KleineWelle', core.kleinewelle),
    ('dmtomega', core.dmt_omega),
    ('dmt-omega', core.dmt_omega),
    ('dmt_omega', core.dmt_omega),
    ('DMT Omega', core.dmt_omega),
    ('Omega', core.omega),
    ('omega_online', core.omega),
])
def test_regex(var, regex):
    assert regex.match(var) is not None


def test_format_channel_name():
    assert core._format_channel_name('X1:TEST-CHANNEL_NAME') == (
        'X1-TEST_CHANNEL_NAME')


def test_find_trigger_files():
    # quick check that this resolves the ETG correctly
    iglob = mock_iglob_factory('L1-OMEGA_TRIGGERS_DOWNSELECT-{0}-{1}.xml')
    with mock.patch('glob.iglob', iglob):
        cache = core.find_trigger_files(
            'L1:GDS-CALIB_STRAIN', 'dmt-omega', 1135641617, 1135728017)
        assert len(cache) == 9
        assert cache[0] == (
            'file:///gds-l1/dmt/triggers/L-HOFT_Omega/11356/'
            'L1-OMEGA_TRIGGERS_DOWNSELECT-1135640000-10000.xml')


def test_find_dmt_omega_files():
    iglob = mock_iglob_factory('L1-OMEGA_TRIGGERS_DOWNSELECT-{0}-{1}.xml')
    with mock.patch('glob.iglob', iglob):
        cache = core.find_dmt_omega_files(
            'L1:GDS-CALIB_STRAIN', 1135641617, 1135728017)
        assert len(cache) == 9
        assert cache[0] == (
            'file:///gds-l1/dmt/triggers/L-HOFT_Omega/11356/'
            'L1-OMEGA_TRIGGERS_DOWNSELECT-1135640000-10000.xml')
        # check wrapper method works
        assert cache == core.find_trigger_files(
            'L1:GDS-CALIB_STRAIN', 'dmt-omega', 1135641617, 1135728017)

    # check error for non-hoft channel with DMT-Omega
    with pytest.raises(NotImplementedError):
        core.find_dmt_omega_files('X1:TEST', 0, 100)


def test_find_kleinewelle_files():
    iglob = mock_iglob_factory('L-KW_TRIGGERS-{0}-{1}.xml')
    with mock.patch('glob.iglob', iglob):
        cache = core.find_kleinewelle_files(
            'L1:TEST-CHANNEL', 1135641617, 1135728017)
        assert len(cache) == 9
        assert cache[0] == (
            'file:///gds-l1/dmt/triggers/L-KW_TRIGGERS/L-KW_TRIGGERS-11356/'
            'L-KW_TRIGGERS-1135640000-10000.xml')
        # check wrapper method works
        assert cache == core.find_trigger_files(
            'L1:TEST-CHANNEL', 'kleinewelle', 1135641617, 1135728017)

    # test h(t)
    iglob = mock_iglob_factory('L-KW_HOFT-{0}-{1}.xml')
    with mock.patch('glob.iglob', iglob):
        cache = core.find_kleinewelle_files(
            'L1:GDS-CALIB_STRAIN', 1135641617, 1135728017)
        assert len(cache) == 9
        assert cache[0] == (
            'file:///gds-l1/dmt/triggers/L-KW_HOFT/'
            'L-KW_HOFT-11356/L-KW_HOFT-1135640000-10000.xml')


def test_find_detchar_files():
    iglob = mock_iglob_factory('L1-GDS_CALIB_STRAIN_OMICRON-{0}-{1}.xml')
    with mock.patch('glob.iglob', iglob):
        with mock.patch('glob.glob', bool):
            cache = core.find_detchar_files(
                'L1:GDS-CALIB_STRAIN', 1135641617, 1135728017,
                etg='omicron')
            assert len(cache) == 9
            assert cache[0] == (
                'file:///home/detchar/triggers/*/L1/GDS-CALIB_STRAIN_Omicron/'
                '11356/L1-GDS_CALIB_STRAIN_OMICRON-1135640000-10000.xml')
            cache2 = core.find_detchar_files(
                'L1:GDS-CALIB_STRAIN', 1146873617, 1146873617+1,
                etg='omicron')
            assert cache2[0] == (
                'file:///home/detchar/triggers/L1/GDS_CALIB_STRAIN_OMICRON/'
                '11468/L1-GDS_CALIB_STRAIN_OMICRON-1146870000-10000.xml')

            # check wrapper method works
            assert cache == core.find_trigger_files(
                'L1:GDS-CALIB_STRAIN', 'omicron', 1135641617, 1135728017)

    # test error for channel that has never been processed
    with pytest.raises(ValueError):
        core.find_detchar_files('X1:DOES-NOT_EXIST:1', 0, 100,
                                etg='fake-etg')


def test_find_pycbc_live_files():
    test_glob = [
        'H1-Live-1126259148.29-4.hdf',
        'H1-Live-1126259228.29-4.hdf',
        'H1-Live-1126259308.29-4.hdf',
        'H1-Live-1126259388.29-4.hdf',
    ]

    with mock.patch('glob.glob', lambda x: test_glob):
        c = core.find_pycbc_live_files(None, 1135641617, 1135728017)
        assert len(c) == 0

        c = core.find_pycbc_live_files(None, 1126259140, 1126269148)
        assert len(c) == 4

        # check wrapper method works
        assert c == core.find_trigger_files(
            None, 'pycbc-live', 1126259140, 1126269148)


def test_find_daily_cbc_files():
    # mock the reader, and make sure we get the right cache
    with mock.patch(OPEN, mock_open(read_data="""
H1 INSPIRAL 0 50 /test/H1-INSPIRAL-0-50.xml.gz
H1 INSPIRAL 50 50 /test/H1-INSPIRAL-50-50.xml.gz
H1 INSPIRAL 100 50 /test/H1-INSPIRAL-100-50.xml.gz
"""[1:])):
        cache = core.find_daily_cbc_files('L1:GDS-CALIB_STRAIN', 0, 100)
        assert cache == core.find_trigger_files(
            'L1:GDS-CALIB_STRAIN', 'daily-cbc', 0, 100)
    assert len(cache) == 2
    assert cache[0] == 'file:///test/H1-INSPIRAL-0-50.xml.gz'

    # without mock, check that we just get an empty cache
    assert not core.find_daily_cbc_files('X1:GDS-CALIB_STRAIN', 0, 100)


def test_find_omega_online_files():
    iglob = mock_iglob_factory('G1-OMEGA_TRIGGERS_DOWNSELECT-{0}-{1}.txt')
    with mock.patch('glob.iglob', iglob):
        cache = core.find_omega_online_files(
            'G1:DER_DATA_H', 1135641617, 1135728017)
        assert len(cache) == 9
        assert cache[0] == (
            'file:///home/omega/online/G1_DER_DATA_H/segments/11356/*/'
            'G1-OMEGA_TRIGGERS_DOWNSELECT-1135640000-10000.txt')

        # check wrapper method works
        assert cache == core.find_trigger_files(
            'G1:DER_DATA_H', 'omega', 1135641617, 1135728017)

    with pytest.raises(NotImplementedError):
        core.find_omega_online_files('L1:TEST-CHANNEL', 0, 100)


def test_find_trigger_urls():
    # make sure a DeprecationWarning is presented
    with pytest.warns(DeprecationWarning):
        # simplest test is to throw an error from find_detchar_files
        with pytest.raises(ValueError):
            core.find_trigger_urls('X1:DOES-NOT_EXIST:1', 'fake-etg', 0, 100)
