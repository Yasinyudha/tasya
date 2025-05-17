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

    # Run the gdalinfo command and capture the output
    gdalinfo_text = subprocess.check_output(["gdalinfo", filename], text=True)[:150]

    is_available = re.findall("50S", gdalinfo_text)
    if is_available:
        os.system(f"gdalwarp -s_srs EPSG:32750 -t_srs {target_src} {filename}")


source_folder = "hyp3"
type_of_file = ["amp_clipped", "corr_clipped", "dem_clipped", "lv_phi_clipped", "lv_theta_clipped", "unw_phase_clipped", "water_mask_clipped"]
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