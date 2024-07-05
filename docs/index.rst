##########
GWTrigFind
##########

============
Installation
============

.. tabs::

   .. tab:: Pip

      .. code-block:: bash

          $ python -m pip install gwtrigfind

      Supported python versions: 2.7, 3.4+.

   .. tab:: Conda

      .. code-block:: bash

          $ conda install -c conda-forge gwtrigfind

      Supported python versions: 2.7, 3.5+.

   .. tab:: Scientific Linux

      .. code-block:: bash

          $ yum install python2-gwtrigfind

      Supported python versions: 2.7, `click here for instructions on how to add
      the required yum repositories
      <https://wiki.ligo.org/DASWG/ScientificLinux>`__.

   .. tab:: Macports

      .. code-block:: bash

          $ port install py37-gwtrigfind

      Supported python versions: 2.7, 3.6+.

================
Package overview
================

.. automodapi:: gwtrigfind
   :no-inheritance-diagram:
   :no-heading:
   :skip: urlparse

========
See Also
========

===========================
Running on the command line
===========================

The `gwtrigfind` package includes a command-line executable with the same name,
which takes in a channel name, ETG name, GPS start time, and GPS stop time,
and will display the locations of known files, for example to find all
Omicron files for L1:GDS-CALIB_STRAIN for the day of January 1 2016 (UTC):

.. code-block:: bash

   $ gwtrigfind L1:GDS-CALIB_STRAIN omicron 1135641617 1135728017

For a full listing of all arguments and options, run:

.. code-block:: bash

   $ gwtrigfind --help

.. note::

   The command-line interface can also be accessed via

   .. code-block:: bash

      $ python -m gwtrigfind --help
