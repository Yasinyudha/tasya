#!/bin/bash
# initial command is extract.py, provide a logic if the data in hyp3 is extracted
python extract.py 
python clip_tiff.py

cd mintpy
smallbaselineApp.py madura_full.txt

cd ..
