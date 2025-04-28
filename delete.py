import os
import re

# set directory and requirements
folder_target = "./hyp3"

for folder_name in os.listdir(folder_target):
    folder_name_path = os.path.join(folder_target, folder_name)
    list_file_name = [file for file in os.listdir(folder_name_path) if (re.search("clipped", file) or re.search("fixed", file))]

    if list_file_name == []:
        print(f"Tidak ada file yang harus dihapus")
    else:
        for file_name in list_file_name:
            file_name_path = os.path.join(folder_name_path, file_name)
            os.remove(file_name_path)
            print(f"Remove {file_name} success")