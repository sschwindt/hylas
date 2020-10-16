from LasPoint import *


def get_file_info(las_file):
    """
    Get information of a las file in dictionary format
    :param las_file: laspy.file.File object
    :return: dict
    """
    return {"x_dim": las_file.X, "y_dim": las_file.Y, "x_dim_scaled": las_file.x, "y_dim_scaled": las_file.y,
            "scale": las_file.header.scale[0], "offset": las_file.header.offset[0], "x": las_file.x}


def print_dimensions(las_file):
    """
    Print dimensions of a las file and return it as xml formatted-string
    :param las_file: laspy.file.File object
    :return: string
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


def main():
    # las_file_name = os.path.abspath("") + "/data/Inn_WWARosenheim_UTM32N_DHHN16_Klasse0_748000_5340000.las"
    las_file_name = os.path.abspath("") + "/data/subsample.las"

    with laspy.file.File(las_file_name, mode="r") as las_file:
        pts = las_file.points

        print("\nHEADER NAMES:")


if __name__ == "__main__":
    main()
