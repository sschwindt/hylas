from helpers import *
from shapely.geometry import Point


class LasPoints:
    """Load and convert las-files

    Arguments:
        las_file_name: A string of name a las file name
        epsg: An integer of Geodetic Parameter Dataset ID (default = 3857)
        use_attributes: A string of attributes to use from the las-file available in pattr (config.py)

    Attributes:
        las_file, las_attributes, epsg, gdf, pts, srs
    """

    def __init__(self, las_file_name, epsg=3857, use_attributes="aciw"):

        self.las_file = laspy.file.File(las_file_name, mode="r")

        self.las_attributes = use_attributes
        self.epsg = epsg
        self.gdf = geopandas.GeoDataFrame()  # void initialization
        self.point_dict = {}  # void init of dict of las points
        # self.pts = []  # void init of list of points with attributes
        # self.pts_description = []  # void init of list of point attributes
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

        # # create new shapefile and get layer
        # shp_file = self._make_shp(shp_file_name)
        # lyr = shp_file.GetLayer()
        #
        # # add fields
        # for prop in parse:
        #     new_field = ogr.FieldDefn(wattr[prop], ogr.OFTReal)
        #     lyr.CreateField(new_field)
        #
        # # get point formats
        # point_formats = [spec.name for spec in self.las_file.point_format.specs]
        logging.info(" * Writing geopandas.GeoDataFrame to shapefile (%s) ..." % shapefile_name)
        self.gdf.to_file(filename=shapefile_name, driver="ESRI Shapefile")
        logging.info("   -- Done.")

    def _build_data_frame(self):
        """
        build geopandas GeoDataFrame - auto-runs self._parse_attributes
        :return:
        """
        self._parse_attributes()
        # pts_df = pd.DataFrame(np.array(self.pts),
        #                       columns=self.pts_description)
        #point_dict = {"geometry": geopandas.points_from_xy(pts_df['x'], pts_df['y'], pts_df['z'])}

        # for attr in self.pts_description:
        #     if not re.search("[x-z]", attr):
        #         point_dict.update({attr: pts_df[attr]})
        logging.info(" * Building geopandas.GeoDataFrame ...")
        self.gdf = geopandas.GeoDataFrame(pd.DataFrame(self.point_dict),
                                          crs="EPSG:%04i" % self.epsg)
        #gdf.set_crs(epsg=self.epsg)

    def _parse_attributes(self):
        """
        Parse attributes and append entries to point list
        """
        logging.info(" * Extracting transformed point coordinates ...")
        self.point_dict = {"geometry": geopandas.points_from_xy(self.las_file.x, self.las_file.y, self.las_file.z)}
        #self.pts = [self.las_file.x, self.las_file.y, self.las_file.z]
        #self.pts_description = ['x', 'y', 'z']

        logging.info(" * Parsing and extracting user attributes of points ...")
        for attr in self.las_attributes:
            try:
                self.point_dict.update({wattr[attr]: self.las_file.__getattribute__(pattr[attr])})
                logging.info("   -- added %s" % wattr[attr])
            except AttributeError:
                logging.error("Non-existing attribute %s. Valid attributes are: %s" % (str(attr), dict2str(wattr)))
            except KeyError:
                logging.error("Non-existing las-file key %s - valid are: " % str(attr) + ", ".join(dir(self.las_file)))


    #
    # def _make_shp(self, shp_file_name=None):
    #     """
    #     Create a new shapefile - pseudo private method
    #     :param shp_file_name: string or None
    #     :return: shapefile name
    #     """
    #
    #     if (shp_file_name is None) or not (os.path.exists(os.path.split(shp_file_name)[0])):
    #         las_path, file_ext = os.path.split(os.path.abspath(self.las_file.filename))
    #         las_name = os.path.splitext(file_ext)[0]
    #         shp_file_name = "{0}/{1}.shp".format(las_path, las_name)
    #
    #     # add projection
    #     with open(shp_file_name.split(".shp")[0] + ".prj", "w+") as prj:
    #         prj.write(get_esriwkt(self.epsg))
    #
    #     return create_shp(shp_file_dir=shp_file_name, layer_name="lidar", layer_type="point")







