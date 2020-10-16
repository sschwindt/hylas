from config import *


class LasPoints:
    def __init__(self, las_file_name, epsg=3857):
        """
        Get information of a las file in dictionary format
        :param las_file_name: STR of name a las file name
        :param epsg: INT of Geodetic Parameter Dataset ID (default = 3857)
        """
        self.las_file = laspy.file.File(las_file_name, mode="r")
        self.epsg = epsg

    def __del__(self):
        self.las_file.close()
        del self.las_file

    def export2shp(self, shp_file_name=None, parse='irnseca'):
        """
        Convert a lasfile to a shapefile
        :param las_file: laspy.file.File object
        :param shp_file_name: OPTIONAL string of shapefile name (must end on .str)
        :param parse:
        :return:
        """

        # create new shapefile and get layer
        shp_file = self._make_shp(shp_file_name)
        lyr = shp_file.GetLayer()

        # add fields
        for prop in parse:
            new_field = ogr.FieldDefn(wattr[prop], ogr.OFTReal)
            lyr.CreateField(new_field)

        # get point formats
        point_formats = [spec.name for spec in las_file.point_fomat.specs]

        for p in las_file.points:
            w.point(p, p.y)
            pdata = [p.z] + [getattr(p, pattr[key]) for key in parse]
            pdata = map(float, pdata)
            w.record(*pdata)

    def _build_points(self):


    def _make_shp(self, shp_file_name=None):
        """
        Create a new shapefile - pseudo private method
        :param shp_file_name: string or None
        :return: shapefile name
        """

        if (shp_file_name is None) or not (os.path.exists(os.path.split(shp_file_name)[0])):
            las_path, file_ext = os.path.split(os.path.abspath(self.las_file.filename))
            las_name = os.path.splitext(file_ext)[0]
            shp_file_name = "{0}/{1}.shp".format(las_path, las_name)

        # add projection
        with open(shp_file_name.split(".shp")[0] + ".prj", "w+") as prj:
            prj.write(get_esriwkt(self.epsg))

        return create_shp(shp_file_dir=shp_file_name, layer_name="lidar", layer_type="point")







