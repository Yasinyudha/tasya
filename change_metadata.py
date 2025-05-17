import rasterio
import os
from rasterio.transform import from_bounds

# New bounds for descending
new_bounds = (743400.0, 9187720.0, 853880.0, 9240840.0)

# path
path = "hyp3"

# Open original file
for folder_dataset in os.listdir(path):
    folder_path = os.path.join(path, folder_dataset)
    for file in os.listdir(folder_path):
        if file.endswith("_clipped.tif"):
            file_path = os.path.join(folder_path, file)

            with rasterio.open(file_path) as src:
                data = src.read(1)
                height, width = data.shape
                crs = src.crs
                profile = src.profile.copy()

            # Create a new transform based on new bounds and image dimensions
            new_transform = from_bounds(*new_bounds, width=width, height=height)
        
            # Update metadata with new transform
            profile.update({
                "transform": new_transform,
                "crs": crs,
                "height": height,
                "width": width
            })

            os.remove(file_path)
            # Save the file with new georeferencing
            with rasterio.open(file_path, "w", **profile) as dst:
                dst.write(data, 1)

            print(f"Change file {os.path.basename(file_path)} is succeed")
