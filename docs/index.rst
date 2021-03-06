.. hylas documentation master file, created by
   sphinx-quickstart on Tue Oct 20 14:15:06 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root ``toctree`` directive.

hylas
=====

.. toctree::
    :maxdepth: 4

.. module:: hylas
    :platform: Linux (Debian)
    :synopsis: Process las-files and extract predictor layers for random forest applications.

.. moduleauthor:: Sebastian Schwindt <sebastian.schwindtATiws.uni-stuttgart.de>

*hylas* extracts geo-spatial information from *las* files and converts them to ESRI shapefiles or GeoTIFF rasters. *las* is the typical file format for storing airborne lidar (`Light Detection and Ranging <https://oceanservice.noaa.gov/facts/lidar.html>`_) data. *hylas* is a *Python3* package and this documentation uses a *Sphinx* *readthedocs* theme. The functional core of *hylas* involves the creation of:

* A point shapefile with user-defined point attributes such as *intensity*, *waveform*, or *nir*.
* Digital elevation model (DEM) with user-defined resolution (pixel size).
* *GeoTIFF* rasters with user-defined resolution (pixel size) for any attribute of a *las* file (e.g., *intensity*, *waveform*, or *nir*).

To ensure the best experience with *hylas* and its useful functions, follow the *Installation* instructions for setting up the working environment either on *Linux* or on *Windows*.

.. admonition:: Get the *hylas* docs as PDF

    This documentation is also as available as a style-adapted PDF (`download <https://hylas.readthedocs.io/_/downloads/en/latest/pdf/>`_).

Installation
============

LINUX (Debian/Ubuntu)
---------------------

Optional: Use a Virtual Machine (VM)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Either download a net-installer *ISO* of `Debian Linux <https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/>`_  or `Ubuntu <https://ubuntu.com/download>`_, or use the `OSGeoLive <http://live.osgeo.org/en/download.html>`_, and install one of theses images as a Virtual Machine (VM). To get started with VMs read the introduction to VMs on `hydro-informatics.github.io <https://hydro-informatics.github.io/vm.html#about>`_. Installing the *OSGeoLive* VM works similar, as described on `hydro-informatics.github.io <https://hydro-informatics.github.io/vm.html#create-a-vm-with-virtualbox>`_, but use the *OSGeoLive* image in lieu of the *Debian Linux* *ISO*. After installing *Linux* as a VM, make sure to:

* `Install Guest Additions <https://hydro-informatics.github.io/vm.html#setup-debian>`_ for *Linux* VMs in *VirtualBox*.
* `Enable folder sharing <https://hydro-informatics.github.io/vm.html#share>`_ between the host and guest (*Debian*, *Ubuntu*, or *OSGeoLive* image).

Other system setups described on `hydro-informatics.github.io <https://hydro-informatics.github.io/vm.html>`_ (e.g., *Wine*) are not required in the following.

Prepare your system
^^^^^^^^^^^^^^^^^^^

Open *Terminal*  and update the system:

.. code:: console

    sudo apt update && sudo apt full-upgrade -y


Update Python references
^^^^^^^^^^^^^^^^^^^^^^^^

Most *Linux* distributions still have *Python2* implemented as base interpreter to be used when ``python`` is called in *Terminal*. However, *Python2* usage is deprecated, and therefore, we want to make sure to robustly use *Python3* for running any *Python* script. Check out the installed *Python3* versions:

.. code:: console

   ls /usr/bin/python*


    /usr/bin/python  /usr/bin/python2  /usr/bin/python2.7  /usr/bin/python3  /usr/bin/python3.8  /usr/bin/python3.8m  /usr/bin/python3m

In this example, *Python2.7* and *Python3.8* are installed. To overwrite *Python2* usage, set the ``python`` environment variable so that it points at *Python3*:

.. code:: console

   sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
   alias python=python3


PIP3 and additional libraries for geospatial analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure that `PyGeos <https://pygeos.readthedocs.io>`_ and `tkinter <https://hydro-informatics.github.io/hypy_gui.>`_ are available for use with `geopandas <https://geopandas.org/>`_:

.. code:: console

   sudo apt install python3-pip
   sudo apt-get install python3-tk
   sudo apt install tk8.6-dev
   sudo apt install libgeos-dev

Then install *QGIS* and ``GDAL`` for *Linux* (this should work for any *Debian* architecture):

.. code:: console

   sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
   sudo apt-get update
   sudo apt-get install gdal-bin
   sudo apt-get install libgdal-dev
   export CPLUS_INCLUDE_PATH=/usr/include/gdal
   export C_INCLUDE_PATH=/usr/include/gdal
   pip3 install GDAL

.. note::

   Check on the latest GDAL release on the `developers website <https://gdal.org/download.html#current-releases>`_.

More guidance for installing GDAL (also on other platforms) is available at `gdal.org <https://gdal.org/download.html>`_.

Install an IDE (*PyCharm*)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: IDE - your choice
   Any other Python IDE is also OK for working with *hylas*. Setting up PyCharm is explained here as just one option for working with *hylas*.

Install *PyCharm* with snap (requires snap):

.. code:: console

   sudo apt install snapd
   sudo snap install pycharm-community --classic


WINDOWS
-------

Required software
^^^^^^^^^^^^^^^^^
On *Windows*, a convenient option for working with *hylas* is to use a conda environment. In addition, *GitBash* is necessary to clone (download) *hylas* (and to keep posted on updates). In detail:

* Install *Anaconda*, for example, as described on `hydro-informatics.github.io <https://hydro-informatics.github.io/hy_ide.html#anaconda>`_.
* `Download <https://git-scm.com/downloads>`_ and install *GitBash*.

Create a conda environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

Then open *Anaconda Prompt* and create a new environment (e.g., ``ipy-hylas``):

.. code:: console

   conda env create --name ipy-hylas python=3.8

Then, activate the new environment:

.. code:: console

   conda activate ipy-hylas

Install the required Python libraries in the new environment:

.. code:: console

   conda update conda
   conda install -c anaconda numpy
   conda install -c anaconda pandas
   conda install -c conda-forge gdal
   conda install -c conda-forge shapely
   conda install -c conda-forge alphashape
   conda install -c conda-forge rasterstats
   conda install -c anaconda scikit-image
   conda install -c conda-forge geopandas
   conda install -c conda-forge laspy


There are more compact ways to setup the conda environment (e.g., using an environment file). To read more about conda environments go to `hydro-informatics.github.io <https://hydro-informatics.github.io/hypy_install.html#conda-env>`_.

Install an IDE (*PyCharm*)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: IDE - your choice
   Any other Python IDE is also OK for working with *hylas*. Setting up PyCharm is explained here as just one option for working with *hylas*.

`Download <https://www.jetbrains.com/pycharm/>`_  and install *PyCharm Community Edition*. Read more at `hydro-informatics.github.io <https://hydro-informatics.github.io/hy_ide.html#pycharm>`_.

GET HYLAS
---------

Clone hylas
^^^^^^^^^^^^

Open *Terminal* (or *Anaconda Prompt*), create a project folder, and ``cd`` to the project folder:

.. code:: console

   mkdir hylas-project
   cd hylas-project

Clone the *hylas* repository in the new folder:

.. code:: console

   git clone https://github.com/sschwindt/lidar-analysis.git

.. note::
   Cloning the repository creates a new sub-folder. So if you want to work directly in your home folder, skip the ``mkdir`` + ``cd`` commands.

.. admonition:: LINUX / PIP3 USERS

   In *Terminal* ``cd`` to the local *hylas* repository to install and update (upgrade) required Python packages:

   .. code:: console

      pip3 install -r requirements.txt
      pip3 install -r requirements.txt --upgrade

   Clean up obsolete update remainders:

   .. code:: console

      sudo apt-get clean
      sudo apt-get autoclean
      sudo apt-get autoremove
      sudo apt-get autoremove --purge

   Windows / conda users can skip the installation of requirements, because those were already installed in the *conda* environment.

Setup *PyCharm* IDE
^^^^^^^^^^^^^^^^^^^

Start *PyCharm* and create a new project from the ``hylas`` repository:

* Open *PyCharm*, click on ``+ Create New Project`` and select the directory where you cloned *hylas* (e.g., ``/ROOT/git/hylas``).
* Define a *Project Interpreter* depending on if you use *Linux / pip3* or *Windows / *Anaconda*. So choose ``New`` > ``Add Python Interpreter``

.. admonition:: LINUX / PIP3 USERS

   Make sure to use the system interpreter ``/usr/bin/python3`` (*Project* > *Settings* > *Interpreter*). You will probably get a warning message about using the system interpreter for a project, but this is acceptable when you are working on a VM.


.. admonition:: WINDOWS / ANACONDA USERS

   * Enable the *View hidden folders* option to see the ``AppData`` folder in *Windows Explorer*. *Microsoft* explains how this works on their `support website <https://support.microsoft.com/en-us/help/14201/windows-show-hidden-files>`_. Then, you can copy-paste folder directories from *Windows Explorer* to *PyCharm*.
   * Identify the system path where the conda environment (e.g. ``ipy-hylas``) lives. Typically, this is something like ``C:\users\<your-user-name>\AppData\Local\Continuum\anaconda3\envs\ipy-hylas`` .
   * In the **Add Python Interpreter** window, go to the *Conda Environment* tab, select *New environment*, and make the following settings:

      * Location: ``C:\users\<your-user-name>\AppData\Local\Continuum\anaconda3\envs\ipy-hylas``
      * Python version: ``3.8``
      * Conda executable: ``C:\users\<your-user-name>\AppData\Local\Continuum\anaconda3\bin\conda``

   There is also a detailed tutorial for setting up *PyCharm* with *Anaconda* available at `docs.anaconda.com <https://docs.anaconda.com/anaconda/user-guide/tasks/pycharm/>`_.


Usage
===========

Basic usage
-----------

To convert a *las* file to an ESRI shapefile or GeoTIFF, load *hylas* in Python from the directory where you downloaded (cloned) *hylas*:

.. code-block:: python

   import hylas
   las_file_name = "path/to/a/las-file.las"
   methods = ["las2shp", "las2tif"]
   hylas.process_file(las_file_name, epsg=3857, methods=methods)


The above code block defines a ``las_file_name`` variable and ``methods`` to be used with ``hylas.process_file`` (see :ref:`hylas-code`). The function accepts many more optional arguments:

.. automodule:: hylas.process_file
   :special-members:

.. note::
   The ``LasPoint`` class (see :ref:`las-point-code`) can also be directly called in any script with ``hylas.LasPoint``. Have a look at the ``hylas.process_file`` function (:ref:`hylas-code`) to see how an instance of the ``LasPoint`` class is used.

Application example
-------------------

The file ``ROOT/test.py`` provides and example for using ``hylas`` with a las-file stored in a new folder ``ROOT/data``:

.. code-block:: python

   import hylas
   import os

   las_file_name = os.path.abspath("") + "/data/las-example.las"
   shp_file_name = os.path.abspath("") + "/data/example.shp"
   epsg = 25832
   methods = ["las2tif"]
   attribs = "aci"
   px_size = 2
   tif_prefix = os.path.abspath("") + "/data/sub"

   hylas.process_file(las_file_name,
                      epsg=epsg,
                      methods=methods,
                      extract_attributes=attribs,
                      pixel_size=px_size,
                      shapefile_name=shp_file_name,
                      tif_prefix=tif_prefix)


.. note::
   The method ``las2tif`` automatically calls the ``las2shp`` (``hylas.LasPoint.export2shp``) method because the GeoTIFF pixel values are extracted from the attribute table of the point shapefile. So ``las2shp`` is the baseline for any other operation.

Geo-utils
---------

The implemented ``geo_utils`` package is forked from `hydro-informatics <https://github.com/hydro-informatics/geo-utils>`_ on *GitHub*. ``geo_utils`` provides routines for creating, modifying, and transforming geo-spatial datasets. A detailed documentation of ``geo_utils`` is available at `geo-utils.readthedocs.io <https://geo-utils.readthedocs.io>`_."""


to enable creating correctly geo-referenced GeoTIFF rasters (``rasterize`` function - see :ref:`geo-utils-code`).

Code documentation
==================

.. _hylas-code:

The main file: hylas.py
-----------------------

.. automodule:: hylas
   :members:
   :private-members:

.. topic:: ``process_file(source_file_name, epsg, **opts)``

   Loads a las-file and convert it to another geospatial file format (keyword arguments ``**opts``).

   Note that this function documentation is currently manually implemented because of *Sphinx* having troubles to look behind decorators.

Arguments:
      * **source_file_name** (``str``): Full directory of the source file to use with methods
         * if ``method="las2*"``: provide a las-file name
         * if ``method="shp2*"``: provide a shapefile name
      * **epsg** (``int``): Authority code to use (try ``hylas.lookup_epsg(las_file_name)`` to look up the epsg online).

Keyword Arguments (``**opts``):
      * **create_dem** (``bool``): Set to True for creating a digital elevation model (DEM - default: ``False``)
      * **extract_attributes** (``str``): Attributes to extract from the las-file available in ``pattr`` (``config.py``)
      * **methods** (``list`` [``str``]): Enabled list strings are ``las2shp``, ``las2tif``, ``shp2tif``, ``las2dem``
      * **overwrite** (``bool``): Overwrite existing shapefiles and/or GeoTIFFs (default: ``True``).
      * **pixel_size** (``float``): Use with *2tif  to set the size of pixels relative to base units (``pixel_size=5`` indicates 5x5-m pixels)
      * **shapefile_name** (``str``): Name of the point shapefile to produce with ``las2*``
      * **tif_prefix** (``str``): Prefix include folder path to use for GeoTiFFs (defined extract_attributes are appended to file name)
      * **interpolate_gap_pixels** (``bool``): Fill empty pixels that are not touched by a shapefile point with interpolated values (default: ``True``)
      * **radius1** (``float``): Define the x-radius for interpolating pixels (default: ``-1``, corresponding to infinity). Only applicable ``with interpolate_gap_pixels``.
      * **radius2** (``float``): Define the y-radius for interpolating pixels (default: ``-1``, corresponding to infinity). Only applicable ``with interpolate_gap_pixels``.
      * **power** (``float``): Power of the function for interpolating pixel values (default: ``1.0``, corresponding to linear).
      * **smoothing** (``float``): Smoothing parameter for interpolating pixel values (default: ``0.0``).
      * **min_points** (``int``): Minimum number of points to use for interpolation. If the interpolator cannot find at least ``min_points`` for a pixel, it assigns a ``no_data`` value to that pixel  (default: ``0``).
      * **max_points** (``int``): Maximum number of points to use for interpolation. The interpolator will not use more than ``max_points`` closest points to interpolate a pixel value (default: ``0``).

Returns:
      ``bool``: ``True`` if successful, ``False`` otherwise.

More information on pixel value interpolation:
* ``interpolate_gap_pixels=True`` interpolates values at pixels that are not touched by any las point.
* The pixel value interpolation uses ``gdal_grid`` (i.e., its Python bindings through ``gdal.Grid()``).
* Control the interpolation parameters with the keyword arguments ``radius1``, ``radius2``, ``power``, ``max_points``, ``min_points``,  and ``smoothing``.

.. seealso:: All variables are illustratively explained on the `GDAL website <https://gdal.org/tutorials/gdal_grid_tut.html?highlight=grid>`_.


Basic parameters: config.py
----------------------------

.. automodule:: config
   :members:
   :private-members:

Global functions: helpers.py
----------------------------

.. automodule:: helpers
   :members:

.. _las-point-code:

The ``LasPoint`` class
-----------------------

.. autoclass:: LasPoint.LasPoint
   :members:
   :private-members:

.. _geo-utils-code:

geo_utils
---------


geo_utils MASTER (geo_utils.py)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: geo_utils.geo_utils
   :members:

geo_utils raster management (raster_mgmt.py)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: geo_utils.raster_mgmt
   :members:

geo_utils shapefile management (shp_mgmt.py)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: geo_utils.shp_mgmt
   :members:

geo_utils projection management (srs_mgmt.py)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: geo_utils.srs_mgmt
   :members:

geo_utils dataset Conversion (dataset_mgmt.py)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: geo_utils.dataset_mgmt
   :members:

Troubleshooting
===============

Memory errors
-------------

.. admonition:: MemoryError

   **Cause**: *las* file may have size of several GiB, which may quickly cause a ``MemoryError`` (e.g., ``MemoryError: Unable to allocate 9.1 GiB for an array with shape ...``). In particular the *Linux* kernel will not attempt to run actions that exceed the commit-able memory.

   **Solution**: Enable memory over-committing:
      * Check the current over-commit mode in *Terminal*:
         ``cat /proc/sys/vm/overcommit_memory``
      * If ``0`` is the answer, the system calculates array dimensions and the required memory (e.g., an array with dimensions ``(266838515, 12, 49)`` requires a memory of ``266838515 * 12 *49 / 1024.0**3`` = ``146`` GiB, which is unlikely to fit in the memory).
      * To enable over-committing, set the commit mode to ``1``:
         ``echo 1 | sudo tee /proc/sys/vm/overcommit_memory``



Contribute (developers)
=======================

How to document hylas
---------------------

This package uses *Sphinx* `readthedocs <https://readthedocs.org/>`_ and the documentation regenerates automatically after pushing changes to the repositories ``main`` branch.

To set styles, configure or add extensions to the documentation use ``ROOT/.readthedocs.yml`` and ``ROOT/docs/conf.py``.

Functions and classes are automatically parsed for `docstrings <https://www.python.org/dev/peps/pep-0257/>`_ and implemented in the documentation. ``hylas`` docs use `google style <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_ docstring formats - please familiarize with the style format and strictly apply in all commits.

To modify this documentation file, edit ``ROOT/docs/index.rst`` (uses `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ format).

In the class or function docstrings use the following section headers:

* ``Args (alias of Parameters)``
* ``Arguments (alias of Parameters)``
* ``Attention``
* ``Attributes``
* ``Caution``
* ``Danger``
* ``Error``
* ``Example``
* ``Examples``
* ``Hint``
* ``Important``
* ``Keyword Args (alias of Keyword Arguments)``
* ``Keyword Arguments``
* ``Methods``
* ``Note``
* ``Notes``
* ``Other Parameters``
* ``Parameters``
* ``Return (alias of Returns)``
* ``Returns``
* ``Raise (alias of Raises)``
* ``Raises``
* ``References``
* ``See Also``
* ``Tip``
* ``Todo``
* ``Warning``
* ``Warnings (alias of Warning)``
* ``Warn (alias of Warns)``
* ``Warns``
* ``Yield (alias of Yields)``
* ``Yields``

For local builds of the documentation, the following packages are required:

.. code:: console

   sudo apt-get install build-essential
   sudo apt-get install python-dev python-pip python-setuptools
   sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev
   apt-cache search libffi
   sudo apt-get install -y libffi-dev
   sudo apt-get install python3-dev default-libmysqlclient-dev
   sudo apt-get install python3-dev
   sudo apt-get install redis-server

To generate a local html version of the ``hylas`` documentation, ``cd`` into the  ``docs`` directory  and type:

.. code:: console

   make html

Learn more about *Sphinx* documentation and the automatic generation of *Python* code docs through docstrings in the tutorial provided at `github.com/sschwindt/docs-with-sphinx <https://github.com/sschwindt/docs-with-sphinx>`_.

Indices and tables
==================

* :ref:``genindex``
* :ref:``modindex``
* :ref:``search``

Disclaimer and License
======================

Disclaimer (general)
--------------------

No warranty is expressed or implied regarding the usefulness or completeness of the information provided for *hylas* and its documentation. References to commercial products do not imply endorsement by the Authors of *hylas*. The concepts, materials, and methods used in the codes and described in the docs are for informational purposes only. The Authors have made substantial effort to ensure the accuracy of the code and the docs and the Authors shall not be held liable, nor their employers or funding sponsors, for calculations and/or decisions made on the basis of application of *hylas*. The information is provided "as is" and anyone who chooses to use the information is responsible for her or his own choices as to what to do with the code, docs, and data and the individual is responsible for the results that follow from their decisions.

BSD 3-Clause License
--------------------

Copyright (c) 2020, Sebastian Schwindt and all other the Authors of *hylas*.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

