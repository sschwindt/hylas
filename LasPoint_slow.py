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

    def create_dem(self, target_file_name="", pixel_size=1.0, overwrite=True):
        """Creates a digital elevation model (DEM) in GeoTIFF format from the *las* file points.

        Args:
            target_file_name (str): A file name including an existing directory where the dem  will be created< must end on ``.tif``.
            pixel_size (float): The size of one pixel relative to the spatial reference system.

        Hint:
            This function works independently and does not require the prior creation of a shapefile.

        Returns:
            int: ``0`` if successful, otherwise ``-1``
        """
        logging.info(" * Creating GeoTIFF DEM %s ..." % target_file_name)

        pts = self.las_file.points['point'].copy().view(np.recarray)
        scale = np.array(self.las_file.header.scale, dtype=np.float64)
        offset = np.array(self.las_file.header.offset, dtype=np.float64)
        las_file_fields = [str(dim.name.encode().decode()) for dim in self.las_file.point_format]

        # read and transform data (from raw - fast than las_file.x)
        dem_array = np.empty((len(pts), 3), dtype=np.float64)
        dem_array[:, 0] = pts.X * scale[0] + offset[0]
        dem_array[:, 1] = pts.Y * scale[1] + offset[1]
        dem_array[:, 2] = pts.Z * scale[2] + offset[2]

        geo_utils.create_raster(file_name=target_file_name,
                                raster_array=dem_array,
                                pixel_height=pixel_size,
                                pixel_width=pixel_size,
                                epsg=self.epsg)
        return 0

    def export2shp(self, **kwargs):
        """Converts las file points to a point shapefile.

        Keyword Args:
            shapefile_name (`str`): Optional shapefile name (must end on .shp).
                                        (default: ``'/this/dir/las_file_name.shp'``).
        Returns:
            str: ``/path/to/shapefile.shp``, which is a point shapefile created by the function.
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




