#!/bin/bash

# Make sure all Python scripts are executable
chmod +x *.py

# Remove all non-.zip files in the hyp3 directory
NON_ZIP=./hyp3/*Zone.Identifier
rm -rf "${NON_ZIP[@]}"

# Run extract.py and capture its exit status
python extract.py
STATUS=$?

if [ $STATUS -ne 0 ]; then
  echo "Error: extract.py failed! Exiting."
  exit 1
fi

echo "Extract.py completed successfully."

# Check if the dataset contains clipped TIFF files
DIR_FILES=(./hyp3/*)

if [ -d "${DIR_FILES[0]}" ]; then
  for directory in "${DIR_FILES[@]}"; do
    ZIP_FILES=("$directory"/*clipped.tif)

    if [ ${#ZIP_FILES[@]} -eq 0 ]; then
      # Run clip_tiff.py
      python clip_tiff.py
    else
      # Delete first, then clip again
      python delete.py
      python clip_tiff.py
    fi
    break
  done
fi
