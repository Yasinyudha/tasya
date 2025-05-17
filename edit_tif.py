import os

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

source_folder = "hyp3"
type_of_file = ["amp_clipped_50", "corr_clipped_50", "dem_clipped_50", "lv_phi_clipped_50", "lv_theta_clipped_50", "unw_phase_clipped_50", "water_mask_clipped_50"]

for folder in os.listdir(source_folder):

    folder_path = os.path.join(source_folder, folder)
    for file in os.listdir(folder_path):
        if file.endswith(".tif"):

            # Check if file matches any type in type_of_file
            if any(t in file for t in type_of_file):

                file_path = os.path.join(folder_path, file)
                new_name = os.path.splitext(file_path)[0]

                # Change coordinate system
                os.system(f"gdalwarp -tr 80 80 -r bilinear {file_path} {new_name + '_fixed.tif'}")