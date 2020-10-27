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
        attributes (str): Defined with ``use_attributes``
        epsg (int): Authority code
        gdf (geopandas.GeoDataFrame): geopandas data frame containing all points of the las file with the properties (columns) defined by ``use_attributes``
        offset (laspy.file.File().header.offset): Offset of las points (auto-read)
        overwrite (bool): Enable or disable overwriting existing files (default: ``True``)
        scale (laspy.file.File().header.scale): Scale of las points relative to the offset (auto-read)
        shapefile_name (str): The name and dicrectorty of a point shapefile where all las-file data is stored
        srs (osr.SpatialReference): The geo-spatial reference imported from ``epsg``
    """

    def __init__(self, las_file_name, epsg=3857, use_attributes="aciw", overwrite=True):

        self.las_file = laspy.file.File(las_file_name, mode="r")

        self.attributes = use_attributes
        self.epsg = epsg
        self.gdf = geopandas.GeoDataFrame()  # void initialization
        self.offset = np.array(self.las_file.header.offset, dtype=np.float64)
        self.overwrite = overwrite
        self.scale = np.array(self.las_file.header.scale, dtype=np.float64)
        self.shapefile_name = ""
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(epsg)
        logging.info("Using EPSG = %04i" % epsg)

    def __del__(self):
        self.las_file.close()
        del self.las_file

    def __repr__(self):
        return "%s" % self.__class__.__name__

    def create_dem(self, target_file_name="", pixel_size=1, **kwargs):
        """Creates a digital elevation model (DEM) in GeoTIFF format from the *las* file points.

        Args:
            target_file_name (str): A file name including an existing directory where the dem  will be created< must end on ``.tif``.
            pixel_size (int): The size of one pixel relative to the spatial reference system

        Keyword Args:
            src_shp_file_name (str): Name of a shapefile from which elevation information is to be extracted (default: name of the las-point shapefile)
            elevation_field_name (str): Name of the field from which elevation data is to be extracted (default: ``"elevation"``)

        Hint:
            This function works independently and does not require the prior creation of a shapefile.

        Returns:
            int: ``0`` if successful, otherwise ``-1``
        """
        logging.info(" * Creating GeoTIFF DEM %s ..." % target_file_name)

        default_keys = {"src_shp_file_name": self.shapefile_name,
                        "elevation_field_name": "elevation",
                        }

        for k in default_keys.keys():
            if kwargs.get(k):
                default_keys[k] = str(kwargs.get(k))

        if not os.path.isfile(default_keys["src_shp_file_name"]):
            logging.info(" * Need to create a point shapefile first (%s does not exist) ..." % default_keys["src_shp_file_name"])
            self.export2shp(shapefile_name=default_keys["src_shp_file_name"])

        if os.path.isfile(target_file_name) and self.overwrite:
            logging.info("   -- Overwriting %s ..." % target_file_name)
            geo_utils.remove_tif(target_file_name)

        geo_utils.rasterize(self.shapefile_name, target_file_name, pixel_size=pixel_size,
                            field_name=default_keys["elevation_field_name"])


        """
        np_dem = self._get_xyz_array()
        np.savetxt(np_dem)
        self.srs.
        import gdal
        gdal.Grid(destName=target_file_name, srcDS=np_dem, format="GTiff", outputSRS=self.srs,
                  width=pixel_size, height)

        # tweak points into a regularly spaced grid
        # zi, yi, xi = np.histogram2d(np_dem[1], np_dem[0],
        #                             bins=(pixel_size, pixel_size),
        #                             weights=np_dem[2],
        #                             normed=False)
        #
        # counts, _, _ = np.histogram2d(np_dem[1], np_dem[0], bins=(pixel_size, pixel_size))
        # zi = np.ma.masked_invalid(zi / counts)
        #
        #
        # geo_utils.create_raster(file_name=target_file_name,
        #                         raster_array=np_dem,
        #                         pixel_height=pixel_size,
        #                         pixel_width=pixel_size,
        #                         origin=(self.offset[0], self.offset[1]),
        #                         epsg=self.epsg)
        logging.info("   -- Done.")
        """

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
            self.shapefile_name = kwargs.get("shapefile_name")
        else:
            self.shapefile_name = os.path.abspath("") + "/{0}.shp".format(self.las_file.filename)

        if os.path.isfile(self.shapefile_name) and self.overwrite is False:
            logging.info(" * Using existing shapefile %s." % self.shapefile_name)
            return self.shapefile_name

        self._build_data_frame()

        logging.info(" * Writing geopandas.GeoDataFrame to shapefile (%s) ..." % self.shapefile_name)
        self.gdf.to_file(filename=self.shapefile_name, driver="ESRI Shapefile")
        logging.info("   -- Done.")
        return self.shapefile_name

    def get_file_info(self):
        """ Prints las file information to console."""

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

    def _get_xyz_array(self):
        """Extract x-y-z data from las records in a faster way than using ``las_file.x``, ``y``, or ``z``.

        Returns:
            ndarray: The DEM information extracted from the las file.
        """
        pts = self.las_file.points['point'].copy().view(np.recarray)

        # read and transform data (from raw - fast than las_file.x)
        dem_array = np.empty((3, len(pts)), dtype=np.float64)
        dem_array[0, :] = pts.X * self.scale[0] + self.offset[0]
        dem_array[1, :] = pts.Y * self.scale[1] + self.offset[1]
        dem_array[2, :] = pts.Z * self.scale[2] + self.offset[2]

        return dem_array

    def _parse_attributes(self):
        """Parses attributes and append entries to point list."""

        logging.info(" * Extracting transformed point coordinates ...")
        dem = self._get_xyz_array()
        point_dict = {"geometry": geopandas.points_from_xy(x=dem[0], y=dem[1], z=dem[2])}
        # add elevation field to facilitate DEM export
        point_dict.update({"elevation": dem[2]})

        logging.info(" * Parsing and extracting user attributes of points ...")
        for attr in self.attributes:
            try:
                point_dict.update({wattr[attr]: self.las_file.__getattribute__(pattr[attr])})
                logging.info("   -- added %s" % wattr[attr])
            except AttributeError:
                logging.error("Non-existing attribute %s. Valid attributes are: %s" % (str(attr), dict2str(wattr)))
            except KeyError:
                logging.error("Non-existing las-file key %s - valid are: " % str(attr) + ", ".join(dir(self.las_file)))
        return point_dict





