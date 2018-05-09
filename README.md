# GW trigfind

A utility to find GW trigger files produced by event trigger generators and archived on the LIGO Data Grid.

[![Build Status](https://travis-ci.org/ligovirgo/trigfind.svg?branch=master)](https://travis-ci.org/ligovirgo/trigfind)
[![Coverage Status](https://coveralls.io/repos/github/ligovirgo/trigfind/badge.svg?branch=master)](https://coveralls.io/github/ligovirgo/trigfind?branch=master)

## Quickstart for python

To discover trigger files for a given channel:

```python
>>> from trigfind import find_trigger_files
>>> cache = find_trigger_files(channel, etg, gpsstart, gpsend)
```

The resulting cache can then be read easily into a table using [`gwpy`](//gwpy.github.io/):

```python
>>> from gwpy.table import EventTable
>>> t = EventTable.read(cache, format='ligolw', tablename='sngl_burst')
```

The format argument depends on the etg you use, but is likely to be one of `'ligolw.sngl_burst'`, `'ligolw.sngl_inspiral'`, or `'root'`.

## Quickstart for command-line

The same query can be performed from the command line by passing each of the functional arguments above as arguments to the `trigfind` executable script:

```bash
trigfind <channel> <etg> <gpsstart> <gpsend>
```
