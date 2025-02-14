from zipfile import ZipFile
import os

target_folder = "./hyp3"

for zip_file in os.listdir(target_folder):
    zip_path = os.path.join(target_folder, zip_file)
    name_zip_file = os.path.basename(zip_path)

    if not os.path.isdir(zip_path):
        # splitted text, to get name
        name_zip_file = name_zip_file.split(".")[0]
        path_name_zip = os.path.join(target_folder, name_zip_file)
    
        try:
            # extract the appropriate file
            with ZipFile(zip_path, "r") as filename:
                filename.extractall(path=target_folder)

            os.remove(zip_path)
            print (f"extracted file {name_zip_file}.zip success") 

        except:
            print(f"file {name_zip_file}.zip is corrupted, can't be extracted")
    else:
        print(f"file {zip_path} is extracted earlier, skip the process")