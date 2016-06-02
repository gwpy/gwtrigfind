.. trigfind documentation master file, created by
   sphinx-quickstart on Fri May 20 16:50:21 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. .. currentmodule:: trigfind

``trigfind`` documentation
==========================

``trigfind`` is a utility module for discovery of gravitational-wave event trigger files produced and stored on the LIGO Data Grid.
Each 'event trigger' represents a transient signal in a data channel, possibly indicative of an astrophysical gravitational-wave signal, but also possibly an instrumental or environmental noise glitch.

Installing trigfind
-------------------

Trigfind can be installed via pip:

.. code-block:: bash

   pip install git+https://github.com/ligovirgo/trigfind.git

If you prefer to install tagged release, please go to https://github.com/ligovirgo/trigfind/releases/latest/ and install from the linked `tar.gz` file.

`trigfind` on the command-line
------------------------------

The ``trigfind`` package includes a command-line executable with the same name, which takes in a channel name, ETG name, GPS start time, and GPS stop time, and will display the locations of known files, for example to find all Omicron files for ``L1:GDS-CALIB_STRAIN`` for the day of January 1 2016 (UTC):

.. code-block:: bash

   $ trigfind L1:GDS-CALIB_STRAIN omicron 1135641617 1135728017

For a full listing of all arguments and options, run:


.. code-block:: bash

   $ trigfind --help

`~trigfind.find_trigger_urls`
-----------------------------

The ``trigfind`` module provides a convience function to find files for any Event Trigger Generator:

.. autosummary::
   :toctree: api/

   trigfind.find_trigger_urls

::

   >>> from trigfind import find_trigger_urls
   >>> files = find_trigger_urls('L1:GDS-CALIB_STRAIN', 'omicron', 1135641617, 1135728017)

The above method passes information along to one of the following that actually finds the files for a given Event Trigger Generator:

.. autosummary::
   :toctree: api/

   trigfind.find_detchar_files
   trigfind.find_dmt_files
   trigfind.find_daily_cbc_files
   trigfind.find_omega_online_files

Contributing to ``trigfind``
----------------------------

All contributions for the ``trigfind`` module are welcomed, please post bug reports, feature requests, and pull requests on the GitHub web interace at https://github.com/ligovirgo/trigfind/.
