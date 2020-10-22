from helpers import *


class LasPoint:
    """Las file container to convert datasets to ESRI point shapefiles and/or GeoTIFFs.

    Args:
        las_file_name (str): Directory to and name of a las file.
        epsg (int): Authority Code - Geodetic Parameter Dataset ID (default: ``3857``).
        overwrite (bool): Overwrite existing shapefiles and/or GeoTIFFs (default: ``True``).
        use_attributes (str): Attributes (properties) to use from the las-file available in pattr (config.py).
                                (default: ``use_attributes="aciw"``).

    Attributes:
        las_file (laspy.file.File): A laspy file object
        las_attributes (str): Defined with ``use_attributes``
        epsg (int): Authority code
        gdf (geopandas.GeoDataFrame): geopandas data frame containing all points of the las file with the properties (columns) defined by ``use_attributes``
        overwrite (bool): Enable or disable overwriting existing files (default: ``True``).
        srs (osr.SpatialReference): The geo-spatial reference imported from ``epsg``
    """

    def __init__(self, las_file_name, epsg=3857, use_attributes="aciw", overwrite=True):

        self.las_file = laspy.file.File(las_file_name, mode="r")

        self.las_attributes = use_attributes
        self.epsg = epsg
        self.gdf = geopandas.GeoDataFrame()  # void initialization
        self.overwrite = overwrite
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(epsg)
        logging.info("Using EPSG = %04i" % epsg)

        self._build_data_frame()

    def __del__(self):
        self.las_file.close()
        del self.las_file

    def __repr__(self):
        return "%s" % self.__class__.__name__

    def export2shp(self, **kwargs):
        r"""Converts las file points to a point shapefile.

        Keyword Args:
            shapefile_name (:obj:`str`, optional): Optional shapefile name (must end on .shp).
                                        (default: ``'/this/dir/las_file_name.shp'``).
        Returns:
            str: ``/path/to/shapefile.shp``
        """
        if kwargs.get("shapefile_name"):
            shapefile_name = kwargs.get("shapefile_name")
        else:
            shapefile_name = os.path.abspath("") + "/{0}.shp".format(self.las_file.filename)

        if os.path.isfile(shapefile_name) and self.overwrite is False:
            logging.info(" * Using existing shapefile %s." % shapefile_name)
            return shapefile_name

        logging.info(" * Writing geopandas.GeoDataFrame to shapefile (%s) ..." % shapefile_name)
        self.gdf.to_file(filename=shapefile_name, driver="ESRI Shapefile")
        logging.info("   -- Done.")
        return shapefile_name

    def get_file_info(self):
        r""" Prints las file information to console."""

        print("Point data formats in file:")
        for f in self.las_file.point_format:
            print("   -- %s" % f.name)
        print("File header info:")
        headers = [str(spec.name) for spec in self.las_file.header.header_format]
        print("   -- " + ", ".join(headers))

    def _build_data_frame(self):
        """ Builds the geopandas GeoDataFrame - auto-runs ``self._parse_attributes``."""
        point_dict = self._parse_attributes()
        # for attr in self.pts_description:
        #     if not re.search("[x-z]", attr):
        #         point_dict.update({attr: pts_df[attr]})
        logging.info(" * Building geopandas.GeoDataFrame ...")
        self.gdf = geopandas.GeoDataFrame(pd.DataFrame(point_dict),
                                          crs="EPSG:%04i" % self.epsg)
        logging.info("   -- Done.")

    def _parse_attributes(self):
        r"""Parses attributes and append entries to point list."""

        logging.info(" * Extracting transformed point coordinates ...")
        point_dict = {"geometry": geopandas.points_from_xy(self.las_file.x, self.las_file.y, self.las_file.z)}

        logging.info(" * Parsing and extracting user attributes of points ...")
        for attr in self.las_attributes:
            try:
                point_dict.update({wattr[attr]: self.las_file.__getattribute__(pattr[attr])})
                logging.info("   -- added %s" % wattr[attr])
            except AttributeError:
                logging.error("Non-existing attribute %s. Valid attributes are: %s" % (str(attr), dict2str(wattr)))
            except KeyError:
                logging.error("Non-existing las-file key %s - valid are: " % str(attr) + ", ".join(dir(self.las_file)))
        return point_dict





