import os
import re
import subprocess
from pyproj import Proj, transform

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def change_coor_sys(target_src, filename):
    """
        Change coordinates from each file based on given source coordinate system,
        hence all of the datasets have one uniform coordinate system
    """
    os.system(f"gdal_edit.py -a_srs {target_src} -a_ullr 720606 9293100 1015886 9048860 {filename}")


source_folder = "hyp3"
type_of_file = ["amp", "corr", "dem", "lv_phi", "lv_theta", "unw_phase", "water_mask"]
COORDINATE_SYSTEM = "EPSG:32749" # This is 49S zone, change it based on your region

for folder in os.listdir(source_folder):

    folder_path = os.path.join(source_folder, folder)
    for file in os.listdir(folder_path):

        if file.endswith(".tif"):
            # Check if file matches any type in type_of_file
            if any(t in file for t in type_of_file):
                file_path = os.path.join(folder_path, file)

                # Change coordinate system
                change_coor_sys(COORDINATE_SYSTEM, file_path)
                print(f"Coordinate system has been changed for {file}")