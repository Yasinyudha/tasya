import os
import re
import subprocess
from pyproj import Proj, transform

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def hms_to_decimal(degrees, minutes, seconds, direction):
    """
    Convert degrees, minutes, and seconds to decimal degrees.
    Negative for South or West.
    """
    decimal = degrees + minutes/60 + seconds/3600
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

def parse_hms(hms_string):
    """
    Parse an HMS string like "111d58'36.95\"E" or "6d24' 1.16\"S"
    into (degrees, minutes, seconds, direction).
    """
    # This regex allows for optional whitespace between minutes and seconds.
    hms_pattern = r"(\d+)d(\d+)'\s*([\d.]+)\"([EWNS])"
    m = re.match(hms_pattern, hms_string)
    if m:
        deg = int(m.group(1))
        minu = int(m.group(2))
        sec = float(m.group(3))
        direc = m.group(4)
        return deg, minu, sec, direc
    else:
        raise ValueError(f"Cannot parse HMS string: {hms_string}")

def extract_corners(target_src, filename):
    # Run gdalinfo and capture the output
    gdalinfo_output = subprocess.check_output(["gdalinfo", filename], text=True)

    # Updated regex to capture Upper Left and Lower Right lines.
    # It captures:
    #   group 1: The corner label ("Upper Left" or "Lower Right")
    #   group 2: First coordinate (projected, not used here)
    #   group 3: Second coordinate (projected, not used here)
    #   group 4: HMS string for Longitude (e.g., 111d58'36.95"E)
    #   group 5: HMS string for Latitude  (e.g., 6d24' 1.16"S)
    pattern = (r"(Upper Left|Lower Right)\s*\(\s*[\d.]+,\s*[\d.]+\s*\)\s*\(\s*"
               r"(\d+d\d+'[\d.]+\"[EW]),\s*"
               r"(\d+d\d+'\s*[\d.]+\"[NS])\s*\)")
    
    matches = re.findall(pattern, gdalinfo_output)
    if not matches:
        print("No matching corner coordinates found.")
        return None

    # Set up coordinate transformations
    wgs84 = Proj(init="epsg:4326")    # WGS84 (lat/lon)
    utm = Proj(init=target_src)     # UTM Zone 49M

    corners = {}
    for match in matches:
        # match[0] = corner label ("Upper Left" or "Lower Right")
        label = match[0]
        lon_hms = match[1]  # e.g., "111d58'36.95\"E"
        lat_hms = match[2]  # e.g., "6d24' 1.16\"S"

        # Parse the HMS strings
        lon_deg, lon_min, lon_sec, lon_dir = parse_hms(lon_hms)
        lat_deg, lat_min, lat_sec, lat_dir = parse_hms(lat_hms)

        # Convert to decimal degrees
        longitude_dd = hms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)
        latitude_dd = hms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)

        # Transform from geographic (WGS84) to UTM coordinates
        easting, northing = transform(wgs84, utm, longitude_dd, latitude_dd)
        corners[label] = (round(easting), round(northing))
    
    return corners


def change_coor_sys(target_src, filename):
    """
        Change coordinates from each file based on given source coordinate system,
        hence all of the datasets have one uniform coordinate system
    """
    # Extract coordinate from initial file and then extract it
    coords = extract_corners(target_src, filename)
    
    # Define spatial resolution and their size
    spatial_res = 80.0
    size = (3691, 3053)

    try:
        # Obtain their coordinates for Upper Left (ul) and Lower Right (lr)
        X_upper_left = coords.get("Upper Left")[0]
        X_lower_right = spatial_res * size[0] + X_upper_left

        Y_upper_left = coords.get("Upper Left")[1]
        Y_lower_right = Y_upper_left - (spatial_res * size[1])

        # gdal_edit command
        os.system(f"gdal_edit.py -a_srs {target_src} -a_ullr {round(X_upper_left)} {round(Y_upper_left)} {round(X_lower_right)} {round(Y_lower_right)} {filename}")
    except TypeError:
        print(f"{filename} can't be handled, return to default its coordinate system")

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