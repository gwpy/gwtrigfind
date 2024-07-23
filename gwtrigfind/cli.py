# Copyright (C) Louisiana State University (2016-2017)
#               Cardiff University (2017-2024)
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

"""Print GW event trigger file paths
"""

from __future__ import print_function

import argparse
import os.path
import sys

try:
    from urllib.parse import urlparse
except ImportError:  # python < 3
    from urlparse import urlparse

from ligo.segments import (segment as Segment, segmentlist as SegmentList)

import gwtrigfind
from .core import _file_segment as file_segment

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"
__version__ = gwtrigfind.__version__


# -- parse command line -------------------------------------------------------

def create_parser():
    """Create a command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="gwtrigfind",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=__version__,
    )

    # arguments
    parser.add_argument(
        "channel",
        help="name of raw data channel",
    )
    parser.add_argument(
        "etg",
        help="name of trigger generator",
    )
    parser.add_argument(
        "gpsstart",
        type=int,
        help="GPS start time of search",
    )
    parser.add_argument(
        "gpsend",
        type=int,
        help="GPS end time of search",
    )

    # options
    parser.add_argument(
        "-g",
        "--gaps",
        action="store_true",
        default=False,
        help=(
            "check for gaps in the recovered files and return "
            "exitcode as follows: 0, no gaps found; "
            "1, some files found with gaps"
        ),
    )
    parser.add_argument(
        "-t",
        "--file-type",
        default=None,
        help="type of files to find, only used for some ETGs",
    )

    outopts = parser.add_argument_group(
        "output options",
    )
    outopts.add_argument(
        "-l",
        "--lal-cache",
        action="store_true",
        default=False,
        help="format output for use as a LAL cache file",
    )
    outopts.add_argument(
        "-n",
        "--names-only",
        action="store_true",
        default=False,
        help="print the names of files, rather than full URLs",
    )

    cbcopts = parser.add_argument_group(
        "daily-cbc options",
    )
    cbcopts.add_argument(
        "-r",
        "--run-type",
        metavar="RUN",
        default="bns_gds",
        choices=[
            "bns",
            "bns_gds",
            "bbh",
            "bbh_gds",
            "lowmass",
        ],
        help="name of daily CBC run, one of: %(choices)s",
    )
    cbcopts.add_argument(
        "-f",
        "--file-tag",
        default="INSPIRAL_30MILLISEC_CLUSTERED",
        help="file tag for daily CBC files",
    )

    return parser


def main(args=None):
    """Run the tool.
    """

    # parse args and simplify variables
    parser = create_parser()
    opts = parser.parse_args(args=args)
    start = int(opts.gpsstart)
    end = int(opts.gpsend)
    gaps = opts.gaps

    # -- find files

    segs = SegmentList([Segment(start, end)])

    # map command-line opts to function kwargs
    kwargs = {}
    argmap = {
        "ext": "file_type",
    }
    for key, arg in argmap.items():
        if (val := getattr(opts, arg)) is not None:
            kwargs[key] = val

    # and map daily-cbc-specific args
    cbcmap = {
        "filetag": "file_tag",
        "run": "run_type",
    }
    if gwtrigfind.daily_cbc.match(opts.etg):
        for key, arg in cbcmap.items():
            kwargs[key] = getattr(opts, arg)

    cache = list()
    for seg in segs:
        cache.extend(gwtrigfind.find_trigger_files(
            opts.channel,
            opts.etg,
            start,
            end,
            **kwargs,
        ))

    known = SegmentList(map(file_segment, cache)) & segs
    if gaps:
        gaps = segs - known
    if gaps:
        print("Missing segments:", file=sys.stderr)
        for seg in gaps:
            print("%f %f" % seg, file=sys.stderr)

    # -- print files

    if opts.lal_cache:
        def fmt(path):
            obs, tag, start, duration = os.path.basename(path).split("-")
            return " ".join((obs, tag, start, duration.split(".")[0], path))
    elif opts.names_only:
        def fmt(path):
            return urlparse(path).path
    else:
        fmt = str
    for e in cache:
        print(fmt(e))

    # exit with appropriate code
    if gaps:
        return 1
    return 0
