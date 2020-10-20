from LasPoint import *
import webbrowser


def lookup_epsg(file_name):
    """
    Google information from file name
    :param file_name: file name string with words separated by "-" or "_"
    :return: open google search
    """
    search_string = file_name.replace("_", "+").replace(".", "+").replace("-", "+")
    google_qry = "https://www.google.com/?#q=projection+crs+epsg+"
    webbrowser.open(google_qry + search_string)



def print_dimensions(las_file):
    """
    Print dimensions of a las file and return it as xml formatted-string
    :param las_file: `laspy.file.File`
    :return: `str`
    """
    for dim in las_file.point_format:
        print(dim.name)
    return las_file.point_format.xml()


def print_header(las_file):
    """
    Print header specs of a las file
    :param las_file: laspy.file.File object
    :return: None
    """
    for spec in las_file.header.header_format:
        print(spec.name)


@log_actions
@cache
def process_file(source_file_name, epsg, **opts):
    r"""Load a las-file and convert it to another geospatial file format (**opts)
    :param source_file_name: (`str`) Full directory of the source file to use with methods
                             * if method="las2*" > provide a las-file name
                             * if method="shp2*" > provide a shapefile name
    :param epsg: Authority code to use (try lashy.lookup_epsg(las_file_name) to look up the epsg online).

    :keyword arguments **opts:
        extract_attributes (`str`): Attributes to extract from the las-file available in pattr (config.py)
        methods(`list` [`str`]): Enabled list strings are las2shp, las2tif, shp2tif
        tar_shapefile_name (`str`): Name of the point shapefile to produce with las2*
        tar_tif_prefix (`str`): Prefix include folder path to use for GeoTiFFs (defined extract_attributes are appended to file name)
        create_dem (`bool`): Default=False - set to True for creating a digital elevation model (DEM)
        pixel_size (`int`): Use with *2tif  to set the size of pixels relative to base units (pixel_size=5 > 5-m pixels)

    :return:
    """
    epsg = 25832
    # las_file_name = os.path.abspath("") + "/data/Inn_WWARosenheim_UTM32N_DHHN16_Klasse0_748000_5340000.las"
    las_file_name = os.path.abspath("") + "/data/sub_UTM32N_DHHN16_Klasse0_x.las"
    las_inn = LasPoint(las_file_name=las_file_name, epsg=25832, use_attributes="aci")

    las_pts_shp = os.path.abspath("") + "/data/laspts.shp"
    las_inn.export2shp(shapefile_name=las_pts_shp)

    tar_dir = os.path.abspath("") + "/data/lasras.tif"
    rasterize(in_shp_file_name=las_pts_shp, out_raster_file_name=tar_dir, pixel_size=5,
              field_name=wattr["i"])


if __name__ == "__main__":
    process_file()
