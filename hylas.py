import geo_utils
from LasPoint import *
import webbrowser


def lookup_epsg(file_name):
    """
    Start a google search to retrieve information from a file name (or other ``str``) with information such as *UTM32*.
    Args:
        file_name (``str): file name  or other string with words separated by "-" or "_"
    Note:
        Opens a google search in the default web browser.
    """
    search_string = file_name.replace("_", "+").replace(".", "+").replace("-", "+")
    google_qry = "https://www.google.com/?#q=projection+crs+epsg+"
    webbrowser.open(google_qry + search_string)


@log_actions
@cache
def process_file(source_file_name, epsg, **opts):
    r"""Load a las-file and convert it to another geospatial file format (**opts)

    Args:
        source_file_name (`str`): Full directory of the source file to use with methods
                             * if method="las2*" > provide a las-file name
                             * if method="shp2*" > provide a shapefile name
        epsg (int): Authority code to use (try lashy.lookup_epsg(las_file_name) to look up the epsg online).
        **opts: optional keyword arguments

    Keyword Args:
        extract_attributes (str): Attributes to extract from the las-file available in pattr (config.py)
        methods(`list` [`str`]): Enabled list strings are las2shp, las2tif, shp2tif
        tar_shapefile_name (str): Name of the point shapefile to produce with las2*
        tar_tif_prefix (str): Prefix include folder path to use for GeoTiFFs (defined extract_attributes are appended to file name)
        create_dem (bool): Default=False - set to True for creating a digital elevation model (DEM)
        pixel_size (int): Use with *2tif  to set the size of pixels relative to base units (pixel_size=5 > 5-m pixels)

    Returns:
        bool: True if successful, False otherwise
    """
    epsg = 25832

    las_inn = LasPoint(las_file_name=las_file_name, epsg=25832, use_attributes="aci")

    las_pts_shp = os.path.abspath("") + "/data/laspts.shp"
    las_inn.export2shp(shapefile_name=las_pts_shp)

    tar_dir = os.path.abspath("") + "/data/lasras.tif"
    geo_utils.rasterize(in_shp_file_name=las_pts_shp, out_raster_file_name=tar_dir, pixel_size=5,
                        field_name=wattr["i"])


# if __name__ == "__main__":
#     process_file()
