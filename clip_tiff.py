import os
import re

# lakukan clip dengan fungsi clip_raster, menggunakan command bash
def clip_raster(clip_feature, in_raster, out_raster):
    if os.path.exists(out_raster):
        os.remove(out_raster)
        print(f"Remove the {os.path.basename(output_path)} file and force to update it...")
        print(f"Clip to {os.path.basename(out_raster)}\n")
    else:
        print(f"Clip to {os.path.basename(out_raster)}")

    command = f"gdalwarp -dstnodata 0 -crop_to_cutline -cutline {clip_feature} {in_raster} {out_raster}"
    os.system(command)

# definisikan kategori file input dan output dalam dataset
type_of_file = ["amp", "corr", "dem", "lv_phi", "lv_theta", "unw_phase", "water_mask"]
type_of_file_output = ["amp_clipped", "corr_clipped", "dem_clipped", "lv_phi_clipped", "lv_theta_clipped", "unw_phase_clipped", "water_mask_clipped"]

# pastikan folder hyp3, mintpy, dan geodata berada dalam satu direktori kerja yang sama
folder_path = "./hyp3"
folder_list_name = os.listdir(folder_path)
clip_folder = "./geodata"
shapefiles = [file for file in os.listdir(clip_folder) if file.endswith(".shp")]

# cek adanya file .shp, return FileNotFoundError jika tidak ada
if os.path.exists(clip_folder):
    if shapefiles:
        clip_feature = os.path.join(clip_folder, shapefiles[0])
    else:
        raise FileNotFoundError("No shapefile found in the specified folder")

    for folder_name in folder_list_name:
        folder_name_path = os.path.join(folder_path, folder_name)
        file_name = [file for file in os.listdir(folder_name_path) if (file.endswith(".tif") and not re.search("_clipped", file))]
        for i, file in enumerate(file_name):
            file_path = f"{folder_name_path}/{folder_name}_{type_of_file[i]}.tif"
            output_path = f"{folder_name_path}/{folder_name}_{type_of_file_output[i]}.tif"
            clip_raster(clip_feature, file_path, output_path)
else:
    print(f"The geoddata folder not in the work directory, please recheck it")
