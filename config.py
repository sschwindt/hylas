import laspy
from geo_utils import *
import os

# Global variables
pattr = {
        "a": 'scan_angle',
        "c": 'classification_flags',
        "e": 'flightline_edge',
        "g": 'gps_time',
        "i": 'intensity',
        "n": 'number_of_returns',
        "r": 'return_number',
        "s": 'scan_direction',
        "u": 'user_data',
        "w": 'wave_form'
        }


wattr = {
        "a": 'ScanAngle',
        "c": 'Class',
        "e": 'FlightEdge',
        "g": 'GPStime',
        "i": 'Intensity',
        "n": 'NumberRet',
        "r": 'Return',
        "s": 'ScanDir',
        "u": 'UserData',
        "w": 'Waveform'
        }

