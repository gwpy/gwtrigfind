# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2014)
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

"""This module provides a discovery mechanism for LIGO_LW XML trigger
files written on the LIGO Data Grid according to the conventions in
LIGO-T1300468.
"""

import glob
import os.path
import re
import datetime
import warnings

from glue.lal import (Cache, CacheEntry)
from glue.segments import segment as Segment

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'

daily_cbc = re.compile('\Adaily[\s_-]cbc\Z')
pycbc_live = re.compile('\Apycbc[\s_-]live\Z')
kleinewelle = re.compile('\A(kw|kleinewelle)\Z', re.I)
dmt_omega = re.compile('\Admt([\s_-])?omega\Z', re.I)
omega = re.compile('\Aomega([\s_-])?(online)?\Z', re.I)
channel_delim = re.compile('[:_-]')

OMICRON_O2_EPOCH = 1146873617


def find_trigger_files(channel, etg, start, end, **kwargs):
    """Find the paths of trigger files for this channel and ETG

    This method uses an ETG-specific finder function to retrieve the
    file paths

    Parameters
    ----------
    channel : `str`
        name of data channel for which to search

    etg : `str`
        name of trigger generator that processed the data

    start : `int`
        GPS start time of search

    end : `int`
        GPS end time of search

    **kwargs
        custom keyword arguments to pass down to the underlying finder

    Returns
    -------
    files : :class:`~glue.lal.Cache`
        a structured list of file URLS

    See Also
    --------
    trigfind.find_detchar_files
    trigfind.find_daily_cbc_files
    trigfind.find_dmt_files
    trigfind.find_omega_online_files

    Examples
    --------
    >>> from trigfind import find_trigger_files
    >>> cache = find_trigger_files('L1:GDS-CALIB_STRAIN', 'Omicron', 1135641617, 1135728017)
    """
    start = int(start)
    end = int(end)

    # construct search
    if daily_cbc.match(etg):
        finder = find_daily_cbc_files
    elif pycbc_live.match(etg):
        finder = find_pycbc_live_files
    elif omega.match(etg):
        finder = find_omega_online_files
    elif kleinewelle.match(etg) or dmt_omega.match(etg):
        finder = find_dmt_files
        kwargs['etg'] = etg
    else:
        finder = find_detchar_files
        kwargs['etg'] = etg
    return finder(channel, start, end, **kwargs)


def find_trigger_urls(*args, **kwargs):
    warnings.warn("this method was renamed find_trigger_files",
                  DeprecationWarning)
    return find_trigger_files(*args, **kwargs)

find_trigger_urls.__doc__ = find_trigger_files.__doc__


def find_detchar_files(channel, start, end, etg='omicron', ext='xml.gz'):
    """Find files in the detchar home directory followind T1300468

    Parameters
    ----------
    channel : `str`
        name of data channel for which to search

    start : `int`
        GPS start time of search

    end : `int`
        GPS end time of search

    etg : `str`, optional
        name of trigger generator that processed the data, defaults to
        ``'omicron'``

    ext : `str`, optional
        file extension, defaults to ``'xml.gz'``

    Returns
    -------
    files : :class:`~glue.lal.Cache`
        a structured list of file URLS
    """
    ifo, name = _format_channel_name(channel).split('-', 1)
    # find base path relative to O1 or O2 formatting
    if start >= OMICRON_O2_EPOCH:
        base = os.path.join(os.path.sep, 'home', 'detchar', 'triggers')
        tag = etg.upper()
        dirtag = '%s_%s' % (name, tag)
    else:
        epoch = '*'
        base = os.path.join(os.path.sep, 'home', 'detchar', 'triggers', '*')
        tag = etg.title()
        dirtag = '%s_%s' % (str(channel).split(':', 1)[1], tag)

    # format file path
    filetag = '%s_%s' % (name, tag)
    trigform = '%s-%s-%s-*.%s' % (ifo, filetag, '[0-9]'*10, ext)

    # test for channel-level directory
    channelbase = os.path.join(base, ifo, dirtag)
    if not glob.glob(channelbase):
        raise ValueError("No channel-level directory found at %s. Either the "
                         "channel name or ETG names are wrong, or this "
                         "channel is not configured for this ETG."
                         % channelbase)

    return _find_in_gps_dirs(os.path.join(channelbase, '{0}', trigform),
                             start, end, ngps=5)


def find_dmt_files(channel, start, end, base=None, etg='kw', ext='xml'):
    """Find DMT-Omega trigger XML files

    Parameters
    ----------
    channel : `str`
        name of data channel for which to search

    start : `int`
        GPS start time of search

    end : `int`
        GPS end time of search

    base : `str, optional
        path of custom base directory, defaults to the LDG standard for
        the given ``etg``

    etg : `str`, optional
        name of trigger generator that processed the data, defaults to
        ``'kw'``

    ext : `str`, optional
        file extension, defaults to ``'xml'``

    Returns
    -------
    files : :class:`~glue.lal.Cache`
        a structured list of file URLS
    """
    # validate ETG is sensible
    if not kleinewelle.match(etg) and not dmt_omega.match(etg):
        raise NotImplementedError("Unrecognised ETG %r for DMT files")

    span = Segment(int(start), int(end))
    ifo, name = _format_channel_name(str(channel)).split('-', 1)
    hoft = name == 'GDS_CALIB_STRAIN'
    # find base path
    site = ifo[0].upper()
    if base is None and kleinewelle.match(etg):
        if hoft:
            tag = '%s-KW_HOFT' % site
        else:
            tag = '%s-KW_TRIGGERS' % site
        base = '/gds-%s/dmt/triggers/%s/%s-{0}' % (ifo.lower(), tag, tag)
    elif base is None and dmt_omega.match(etg):
        if hoft:
            tag = '%s-HOFT_Omega' % site
        else:
            raise NotImplementedError("This method doesn't know how to locate "
                                      "%s files for %r" % (etg, str(channel)))
        base = '/gds-%s/dmt/triggers/%s/{0}' % (ifo.lower(), tag)
    # find file name format
    if dmt_omega.match(etg):
        filename = '%s-%s_OmegaC-*-*.%s' % (ifo, name, ext)
    else:
        filename = '%s-*-*.%s' % (tag, ext)
    # loop over GPS directories and find files
    return _find_in_gps_dirs(os.path.join(base, filename), start, end, ngps=5)


def _find_in_gps_dirs(globpath, start, end, ngps=5):
    span = Segment(start, end)
    form = '%%.%ss' % ngps
    gps5 = max(0, int(form % start) - 1)
    end5 = int(form % end)
    out = Cache()
    append = out.append
    while gps5 <= end5:
        for f in glob.iglob(globpath.format(gps5)):
            ce = CacheEntry.from_T050017(os.path.realpath(f))
            if ce.segment.intersects(span):
                append(ce)
        gps5 += 1
    out.sort(key=lambda e: e.path)
    return out.unique()


def _format_channel_name(channel):
    return channel_delim.sub('_', channel).replace('_', '-', 1)


def find_pycbc_live_files(channel, start, end, run='official'):
    """ Find CBC pycbc live trigger files

    Parameters
    ----------
    channel : `str`
        name of data channel for which to search

    start : `int`
        GPS start time of search

    end : `int`
        GPS end time of search

    run : `str`, optional
        name of daily CBC analysis that generated the files, defaults to
        ``'official'``

    ext : `str`, optional
        file extension, defaults to ``'xml.gz'``

    Returns
    -------
    files : :class:`~glue.lal.Cache`
        a structured list of file URLS
    """
    from lal import gpstime

    #FIXME This will need to be updated when the triggers are moved to a
    # dedicated account and will then allow for alternate run directories
    base = os.path.join(os.path.sep, 'home', 'ahnitz', 'pycbc_live', 'data')

    date = gpstime.gps_to_utc(start).date()
    date_end = gpstime.gps_to_utc(end).date()
    oneday = datetime.timedelta(days=1)

    cache = Cache()
    while date <= date_end:
        date_fol = date.strftime('%Y_%m_%d').replace('_0', '_')
        full_path = os.path.join(base, date_fol, '*.hdf')
        files = glob.glob(full_path)

        for file in files:
            fname = os.path.splitext(os.path.basename(file))[0]
            ifos, name, fstart, dur = fname.split('-')

            if float(fstart) + float(dur) < start or float(fstart) > end:
                continue

            url = os.path.abspath(file)
            cache.append(CacheEntry("%s %s %s %s %s" % (ifos, name,
                                                        fstart,
                                                        dur, url)))
        date += oneday
    return cache


def find_daily_cbc_files(channel, start, end, run='bns_gds',
                         filetag='30MILLISEC_CLUSTERED', ext='xml.gz'):
    """Find daily CBC analysis trigger files

    Parameters
    ----------
    channel : `str`
        name of data channel for which to search

    start : `int`
        GPS start time of search

    end : `int`
        GPS end time of search

    run : `str`, optional
        name of daily CBC analysis that generated the files, defaults to
        ``'bns_gds'``

    filetag : `str`, optional
        tag describing which kind of clustering was applied, defaults to
        ``'30MILLISEC_CLUSTERED'``

    ext : `str`, optional
        file extension, defaults to ``'xml.gz'``

    Returns
    -------
    files : :class:`~glue.lal.Cache`
        a structured list of file URLS
    """
    from lal import gpstime
    span = Segment(start, end)
    ifo = channel.split(':')[0]
    base = os.path.join(os.path.sep, 'home', 'cbc', 'public_html',
                        'daily_cbc_offline', run)
    date = gpstime.gps_to_utc(start).date()
    end = gpstime.gps_to_utc(end).date()
    oneday = datetime.timedelta(days=1)
    filename = '%s-INSPIRAL_%s.cache' % (ifo, filetag)
    out = Cache()
    while date <= end:
        day = date.strftime('%Y%m%d')
        month = day[:6]
        cachefile = os.path.join(base, month, day, 'cache', filename)
        try:
            with open(cachefile, 'r') as f:
                out.extend(Cache.fromfile(f).sieve(segment=span))
        except IOError:
            pass
        date += oneday
    return out.unique()


def find_omega_online_files(channel, start, end, filetag='DOWNSELECT',
                            ext='txt'):
    """Find Omega triggers produced by online processes

    This is only tested to work for the Omega online processing for GEO600

    Parameters
    ----------
    channel : `str`
        name of data channel for which to search

    start : `int`
        GPS start time of search

    end : `int`
        GPS end time of search

    filetag : `str`, optional
        tag describing which king of Omega files you want, defaults to
        ``'DOWNSELECT'``

    ext : `str`, optional
        file extension, defaults to ``'txt'``

    Returns
    -------
    files : :class:`~glue.lal.Cache`
        a structured list of file URLS
    """

    # find base path
    ifo, name = channel.split(':', 1)
    if ifo == 'G1':
        dirtag = '%s_%s' % (ifo, name)
        base = os.path.join(os.path.sep, 'home', 'omega', 'online',
                            dirtag, 'segments', '{0}', '*')
    else:
        raise NotImplementedError("Unrecognised channel for omega online %r"
                                  % channel)

    trigform = '%s-OMEGA_TRIGGERS_%s-*-*.%s' % (ifo, filetag, ext)

    return _find_in_gps_dirs(os.path.join(base, trigform), start, end, ngps=5)
