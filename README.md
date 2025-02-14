## Welcome to the support file for MintPy
_Created by: Tasya Mutiara Dewi and Yasin Yudha Praditha_

According to official release of Miami INsar Time-series software in PYthon (MintPy), MintPy is an open-source package for Interferometric Synthetic Aperture Radar (InSAR) time series analysis. It reads the stack of interferograms (coregistered and unwrapped) in ISCE, ARIA, FRInGE, HyP3, GMTSAR, SNAP, GAMMA or ROI_PAC format, and produces three dimensional (2D in space and 1D in time) ground surface displacement in line-of-sight direction. It includes a routine time series analysis (`smallbaselineApp.py`) and some independent toolbox. This repository consists about support action for MintPy, like clip tiff image from dataset from given ".shp" file, delete the current clipped tiff, and many more. If you want to use this, please use this script with the following step:

1. If you want to clip file tiff from dataset, use clip_tiff.py with command
```bash
python clip_tiff.py

3. If you want to delete the clipped tiff from dataset, use delete.py with command
```bash
python delete.py
