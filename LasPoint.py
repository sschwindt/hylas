from helpers import *


class LasPoint:
    """Load and convert las-files

    Arguments:
        las_file_name: `str`
            Name a las file name
        epsg: `int`
            Authority Code - Geodetic Parameter Dataset ID (default = 3857)
        use_attributes: `str`
            Attributes (properties) to use from the las-file available in pattr (config.py)

    Attributes:
        las_file, las_attributes, epsg, gdf, srs
    """

    def __init__(self, las_file_name, epsg=3857, use_attributes="aciw"):

        self.las_file = laspy.file.File(las_file_name, mode="r")

        self.las_attributes = use_attributes
        self.epsg = epsg
        self.gdf = geopandas.GeoDataFrame()  # void initialization
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(epsg)
        logging.info("Using EPSG = %04i" % epsg)

        self.__shape_file_exists__ = False

        self._build_data_frame()

    def __del__(self):
        self.las_file.close()
        del self.las_file

    def __repr__(self):
        return "%s" % self.__class__.__name__

    def export2shp(self, **kwargs):
        r"""Convert a las-file to shapefile
        :Keyword Arguments:
            * *shapefile_name* (``str``): Optional shapefile name (must end on .shp).
            Default=las_file_name.shp
        :return: shapefile name (``str``)
        """
        if kwargs.get("shapefile_name"):
            shapefile_name = kwargs.get("shapefile_name")
        else:
            shapefile_name = os.path.abspath("") + "/{0}.shp".format(self.las_file.filename)

        logging.info(" * Writing geopandas.GeoDataFrame to shapefile (%s) ..." % shapefile_name)
        self.gdf.to_file(filename=shapefile_name, driver="ESRI Shapefile")
        logging.info("   -- Done.")

    def get_file_info(self):
        """
        Get information of a las file in dictionary format
        :param las_file: laspy.file.File object
        :return: `dict`
        """
        print("Point data formats in file:")
        for f in self.las_file.point_format:
            print("   -- %s" % f.name)
        print("File header info:")
        headers = [str(spec.name) for spec in self.las_file.header.header_format]
        print("   -- " + ", ".join(headers))

        return {"x_raw": self.las_file.X, "y_raw": self.las_file.Y, "x_scaled": self.las_file.x, "y_scaled": las_file.y,
                "scale": self.las_file.header.scale[0], "offset": self.las_file.header.offset[0]}

    def _build_data_frame(self):
        """
        build geopandas GeoDataFrame - auto-runs self._parse_attributes
        :return:
        """
        point_dict = self._parse_attributes()
        # for attr in self.pts_description:
        #     if not re.search("[x-z]", attr):
        #         point_dict.update({attr: pts_df[attr]})
        logging.info(" * Building geopandas.GeoDataFrame ...")
        self.gdf = geopandas.GeoDataFrame(pd.DataFrame(point_dict),
                                          crs="EPSG:%04i" % self.epsg)
        logging.info("   -- Done.")

    def _parse_attributes(self):
        """
        Parse attributes and append entries to point list
        """
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





