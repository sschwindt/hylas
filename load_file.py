import laspy
import os

# las_file_name = os.path.abspath("") + "/data/Inn_WWARosenheim_UTM32N_DHHN16_Klasse0_748000_5340000.las"
las_file_name = os.path.abspath("") + "/data/subsample.las"

with laspy.file.File(las_file_name, mode="rw") as las_file:
    pts = las_file.points
    x_dim = las_file.X
    y_dim = las_file.Y
    scale = las_file.header.scale[0]
    offset = las_file.header.offset[0]

    print("x_dim: " + str(x_dim))
    print("y_dim: " + str(y_dim))
    print("scale: " + str(scale))
    print("offset: " + str(offset))

    print("\nHEADER NAMES:")
    headerformat = las_file.header.header_format
    for spec in headerformat:
        print(dir(spec))
        print(spec.name)

    # print point dimensions
    # for dim in las_file.point_format:
    #     print(dim.name)
    # # or grab as xml file
    # las_file.point_format.xml()

