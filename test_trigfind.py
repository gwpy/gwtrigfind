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

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import trigfind

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'


class TrigfindTestCase(unittest.TestCase):
    def test_regex(self):
        for var in ['daily-cbc', 'daily_cbc']:
            self.assertRegexpMatches(var, trigfind.daily_cbc)
        for var in ['kw', 'kleinewelle', 'KleineWelle']:
            self.assertRegexpMatches(var, trigfind.kleinewelle)
        for var in ['dmtomega', 'dmt-omega', 'dmt_omega', 'DMT Omega']:
            self.assertRegexpMatches(var, trigfind.dmt_omega)
        for var in ['omega', 'omega_online']:
            self.assertRegexpMatches(var, trigfind.omega)

    def test_format_channel_name(self):
        self.assertEqual(trigfind.format_channel_name('X1:TEST-CHANNEL_NAME'),
                         'X1-TEST_CHANNEL_NAME')
