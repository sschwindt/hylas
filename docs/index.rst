.. hylas documentation master file, created by
   sphinx-quickstart on Tue Oct 20 14:15:06 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root ``toctree`` directive.

hylas
=====

.. toctree::
    :maxdepth: 3
    :caption: Main file

   hylas

.. module:: hylas
    :platform: Unix, Windows
    :synopsis: Process las-files and extract predictor layers for random forest applications.

.. moduleauthor:: Sebastian Schwindt <sebastian.schwindtATiws.uni-stuttgart.de>

Detect object size and types from airborne lidar data with the *hylas* Python3 package. *hylas* is documented with *Sphinx* and uses *laspy* with a set of other requirements. Therefore, it is recommended to follow the workflow described in this workflow to setup the working environment.


Get ready with the OSGeoLive VM
================================

Install *OSGeoLive* `download ISO image <http://live.osgeo.org/en/download.html>`_ as a Virtual Machine (VM). To get started with VMs read the introduction to VMs on `hydro-informatics.github.io <https://hydro-informatics.github.io/vm.html#about>`_. Installing the *OSGeoLive* VM works similarly as described on `hydro-informatics.github.io <https://hydro-informatics.github.io/vm.html#create-a-vm-with-virtualbox>`_, but use the *OSGeoLive* image in lieu of a *Debian Linux* *ISO*. Afterwards, make sure to:

* `install \ *Guest Additions\* <https://hydro-informatics.github.io/vm.html#setup-debian>`_ for *Linux* VMs in *VirtualBox*
* `enable folder sharing <https://hydro-informatics.github.io/vm.html#share>`_ between the host and guest (*OSGeoLive* image)

The other system setups described on `hydro-informatics.github.io <https://hydro-informatics.github.io/vm.>`_ (e.g., *Wine*) are not required in the following.

.. note:: As an alternative for the *OSGeoLive* VM, get *libLAS* for your operating system (OS):
          - On *Linux* install `*Debian GIS* <https://wiki.debian.org/DebianGis>`_ or try the *Live Image* on a `*Virtual Machine* <https://hydro-informatics.github.io/vm.>`_
          - On *Windows* install *libLAS* through *OSGeo4W* (`see detailed instructions <https://liblas.org/osgeo4w.>`_)

The following instructions refer to the usage of the *OSGeoLive* VM.

Prepare the system
---------------------------------------

Open *Terminal*  and update the system:

.. code:: $ sudo apt update &&    $ sudo apt full-upgrade -y


Update Python references
---------------------------------------

.. code:: $ ls /usr/bin/python*

    /usr/bin/python  /usr/bin/python2  /usr/bin/python2.7  /usr/bin/python3  /usr/bin/python3.6  /usr/bin/python3.6m  /usr/bin/python3m


Now set the ``python`` environment variable so that it points at *Python3*:

.. code:: $ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
          $ alias python=python3


Additional libraries for geospatial analysis
---------------------------------------------
Make sure that `*PyGeos* <https://pygeos.readthedocs.io>`_ and `*tkinter* <https://hydro-informatics.github.io/hypy_gui.>`_ are available for use with `*geopandas* <https://geopandas.org/>`_:

.. code::  $ sudo apt-get install python3-tk
   $ sudo apt install tk8.6-dev
   $ sudo apt install libgeos-dev



Install PIP3 and Python libraries
---------------------------------------

Then install: ``pip3``:

.. code::
   $ sudo apt install python3-pip

Then use the *requirements* file from this repository and copy it to the project folder. In *Terminal* type:

.. code::
   $ pip3 install -r requirements.txt

Clean up obsolete update remainders:

.. code::
   $ sudo apt-get clean
   $ sudo apt-get autoclean
   $ sudo apt-get autoremove
   $ sudo apt-get autoremove --purge


Clone lidar-analysis repository
---------------------------------------

In Clone the *lidar-analysis* repository:

.. code::
   $ git clone https://github.com/sschwindt/lidar-analysis.git

Note that this repository is private and you will need to send an inquiry to `Sebastian Schwindt <mailto:sebastian.schwindtATiws.uni-stuttgart.de?subject=GitHub%20Access%20to%lidar%repo>`_.


Get ready with *PyCharm*
---------------------------------------

Install *PyCharm* if not yet done (requires snap):

.. code::
   $ sudo apt install snapd
   $ sudo snap install pycharm-community --classic


Start *PyCharm* and create a new project from the ``lidar-analysis`` repository.
Make sure to use the system interpreter ``/usr/bin/python3`` (*Project* > *Settings* > *Interpreter*). You will probably get a warning message about using the system interpreter for a project, but this is acceptable because we are working on a VM.



   hylas


hylas main
---------------------------------------
.. automodule:: hylas
   :members:

hylas config
---------------------------------------
.. automodule:: config
   :members:

hylas helpers functions
---------------------------------------
.. automodule:: helpers
   :members:

hylas LasPoint class
---------------------------------------
.. automodule:: LasPoint
   :members:

hylas geo_utils master
---------------------------------------
.. automodule:: geo_utils.geo_utils
   :members:

hylas geo_utils geoconfig
---------------------------------------
.. automodule:: geo_utils.geoconfig
   :members:

hylas geo_utils Raster Management
---------------------------------------
.. automodule:: geo_utils.raster_mgmt
   :members:

hylas geo_utils Shapefile Management
---------------------------------------
.. automodule:: geo_utils.shp_mgmt
   :members:

hylas geo_utils Projection Management
---------------------------------------
.. automodule:: geo_utils.srs_mgmt
   :members:

hylas geo_utils Dataset Conversion
---------------------------------------
.. automodule:: geo_utils.dataset_mgmt
   :members:


DEVELOPER GUIDE
***************

Install *Sphinx* and *read-the-docs* (skip already installed packages):

.. code::
   $ sudo apt-get install build-essential
   $ sudo apt-get install python-dev python-pip python-setuptools
   $ sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev
   $ apt-cache search libffi
   $ sudo apt-get install -y libffi-dev
   $ sudo apt-get install python3-dev default-libmysqlclient-dev
   $ sudo apt-get install python3-dev
   $ sudo apt-get install redis-server

Document the code
==================

The hylas docs live in ``/docs/build/html``. So to read the packages contents, open ``/docs/build/html/index.html``.

Setup docs directory
====================

Create a new ``docs`` directory and ``cd`` in the new directory:


mkdir docs
cd docs


Start and setup *Sphinx*
=========================

In the new ``docs`` folder, get start a new *Sphinx* documentation with (follow the instructions during the project setup process):


sphinx-quickstart


Setup **``conf.py``**
---------------------------------

After setting up the new *Sphinx* project, open (edit) ``/docs/source/conf.py``:

* Uncomment/Add the following lines

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.setrecursionlimit(1500)


* Add the project root folder to the documentation source by modifying the relative directory in ``os.path.abspath('.')`` to ``os.path.abspath('../..')``. Note that this change is based on the assumption that the *Python* project will be located in ``/NewProject`` (corresponds to the root directory) and that the docs will live in ``/NewProject/docs``.


Build the docs (*html* and *PDF*)
---------------------------------

Regular push: The docs are available at  `https://hylas.readthedocs.io <https://hylas.readthedocs.io>`_

First-time push: Login to `https://readthedocs.org <https://docs.readthedocs.io>`_ and build the project after pushing changes.

In *Terminal* ``cd`` to the ``/ROOT/docs`` directory and type:
make html
sphinx-build -b rinoh source _build/rinoh

<p>Documentation written by {{ author }} (last updated on {{ date }}.</p>

Indices and tables
==================

* :ref:``genindex``
* :ref:``modindex``
* :ref:``search``

