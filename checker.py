import os
import re

hyp3_folder = "./hyp3"
zip_folder = "./zip"

for file in os.listdir(zip_folder):
    zip_path = os.path.join(zip_folder, file)
    name_file = os.path.basename(zip_path)
    name = name_file.split(".")[0]

    if name not in os.listdir(hyp3_folder):
        print(f"The folder {name} is not exist in hyp3 dataset")
