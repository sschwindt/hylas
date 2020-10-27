"""This is the hylas config file - do not confuse with docs/conf (sphinx documentation config)
nor geo_utils/geoconfig."""
try:
    import os
    import logging
    import re
    import shutil
except ImportError:
    print("ERROR: Cannot import basic Python libraries.")

try:
    import laspy
except ImportError:
    print("ERROR: Cannot import LasPy.")

try:
    import pandas as pd
    import geopandas
except ImportError:
    print("ERROR: Cannot import pandas and geopandas.")

try:
    import numpy as np
except ImportError:
    print("ERROR: Cannot import numpy.")

try:
    import shapely
except ImportError:
    print("ERROR: Cannot import shapely.")

try:
    from gdal import osr
except ImportError:
    print("ERROR: Cannot import gdal.")

try:
    from geo_utils import *
except ImportError:
    print("ERROR: Cannot import geo_utils.")

# Global variables
cache_folder = os.path.abspath("") + "/__cache__/"
nan_value = 0.0

pattr = {
        "a": "scan_angle",
        "b": "blue",
        "c": "classification_flags",
        "C": "classification",
        "e": "edge_flight_line",
        "g": "green",
        "G": "gps_time",
        "i": "intensity",
        "n": "nir",
        "N": "num_returns",
        "r": "red",
        "R": "return_num",
        "s": "scan_dir_flag",
        "u": "user_data",
        "w": "wave_packet_desc_index",
        "W": "waveform_packet_size"
        }
"""``dict``: ``dict`` of attributes to extract data layers (shapefile columns or multiple GeoTIFFs) from a las file.

All attributes defined in ``pattr.values()`` must be an attribute of a las_file object.
Print all available las file attributes with:

.. code-block:: python

    print(dir(LasPoint.las_file))
"""

wattr = {
        "a": "ScanAngle",
        "b": "Blue",
        "c": "ClassFlag",
        "C": "Class",
        "e": "FlightEdge",
        "g": "Green",
        "G": "GPStime",
        "i": "Intensity",
        "n": "NIR",
        "N": "NumberRet",
        "r": "Red",
        "R": "ReturnNumber",
        "s": "ScanDir",
        "u": "UserData",
        "w": "WaveformDesc",
        "W": "WaveSize"
        }
"""``dict``: ``dict`` with column headers (shapefile attribute table) and GeoTIFF file names to use for parsing attributes."""
