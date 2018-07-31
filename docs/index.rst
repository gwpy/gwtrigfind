.. gwtrigfind documentation master file, created by
   sphinx-quickstart on Fri May 20 16:50:21 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. .. currentmodule:: gwtrigfind

GWTrigFind documentation
========================

``gwtrigfind`` is a utility module for discovery of gravitational-wave event trigger files produced and stored on the LIGO Data Grid.
Each 'event trigger' represents a transient signal in a data channel, possibly indicative of an astrophysical gravitational-wave signal, but also possibly an instrumental or environmental noise glitch.

Installing GWTrigFind
---------------------

GWTrigFind can be installed via pip:

.. code-block:: bash

   pip install git+https://github.com/gwpy/gwtrigfind.git

If you prefer to install tagged release, please go to https://github.com/gwpy/gwtrigfind/releases/latest/ and install from the linked `tar.gz` file.

`gwtrigfind` on the command-line
------------------------------

The ``gwtrigfind`` package includes a command-line executable with the same name, which takes in a channel name, ETG name, GPS start time, and GPS stop time, and will display the locations of known files, for example to find all Omicron files for ``L1:GDS-CALIB_STRAIN`` for the day of January 1 2016 (UTC):

.. code-block:: bash

   $ gwtrigfind L1:GDS-CALIB_STRAIN omicron 1135641617 1135728017

For a full listing of all arguments and options, run:


.. code-block:: bash

   $ gwtrigfind --help

`~gwtrigfind.find_trigger_files`
-----------------------------

The ``gwtrigfind`` module provides a convience function to find files for any Event Trigger Generator:

.. autosummary::
   :toctree: api/

   gwtrigfind.find_trigger_files

::

   >>> from gwtrigfind import find_trigger_files
   >>> files = find_trigger_files('L1:GDS-CALIB_STRAIN', 'omicron', 1135641617, 1135728017)

The above method passes information along to one of the following that actually finds the files for a given Event Trigger Generator:

.. autosummary::
   :toctree: api/

   gwtrigfind.find_detchar_files
   gwtrigfind.find_dmt_files
   gwtrigfind.find_daily_cbc_files
   gwtrigfind.find_omega_online_files

Contributing to ``gwtrigfind``
----------------------------

All contributions for the ``gwtrigfind`` module are welcomed, please post bug reports, feature requests, and pull requests on the GitHub web interace at https://github.com/gwpy/gwtrigfind/.
