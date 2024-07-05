# GWTrigFind

A utility to find GW trigger files produced by event trigger generators and archived on the LIGO Data Grid.

[![PyPI version](https://badge.fury.io/py/gwtrigfind.svg)](http://badge.fury.io/py/gwtrigfind)
[![Documentation Status](https://readthedocs.org/projects/gwtrigfind/badge/?version=stable)](https://gwtrigfind.readthedocs.io/en/stable/?badge=stable)
[![Build status](https://git.ligo.org/detchar/tools/gwtrigfind/badges/main/pipeline.svg)](https://git.ligo.org/computing/software/requests-ecp/-/pipelines)
![Code coverage](https://git.ligo.org/detchar/tools/gwtrigfind/badges/main/coverage.svg)

## Quickstart for python

To discover trigger files for a given channel:

```python
>>> from gwtrigfind import find_trigger_files
>>> cache = find_trigger_files(channel, etg, gpsstart, gpsend)
```

The resulting cache can then be read easily into a table using [`gwpy`](//gwpy.github.io/):

```python
>>> from gwpy.table import EventTable
>>> t = EventTable.read(cache, format='ligolw', tablename='sngl_burst')
```

The format argument depends on the etg you use, but is likely to be one of `'hdf5'`, `'ligolw'`, or `'root'`.

## Quickstart for command-line

The same query can be performed from the command line by passing each of the functional arguments above as arguments to the `gwtrigfind` executable script:

```bash
gwtrigfind <channel> <etg> <gpsstart> <gpsend>
```
