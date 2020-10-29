import hylas
import os

#las_file_name = os.path.abspath("") + "/data/Inn_WWARosenheim_UTM32N_DHHN16_Klasse0_748000_5340000.las"
las_file_name = os.path.abspath("") + "/data/sub_UTM32N_DHHN16_Klasse0_x.las"
shp_file_name = os.path.abspath("") + "/data/sub.shp"
epsg = 25832
methods = ["las2shp", "las2dem"]
attribs = "aci"
px_size = 2
tif_prefix = os.path.abspath("") + "/data/sub"

hylas.process_file(las_file_name,
                   epsg=epsg,
                   methods=methods,
                   extract_attributes=attribs,
                   pixel_size=px_size,
                   shapefile_name=shp_file_name,
                   tif_prefix=tif_prefix,
                   smoothing=10.0,
                   power=2.0)
