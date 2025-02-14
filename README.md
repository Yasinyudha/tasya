## Welcome to the support file for MintPy
_Created by: Tasya Mutiara Dewi and Yasin Yudha Praditha_

According to official release of Miami INsar Time-series software in PYthon (MintPy), MintPy is an open-source package for Interferometric Synthetic Aperture Radar (InSAR) time series analysis. It reads the stack of interferograms (coregistered and unwrapped) in ISCE, ARIA, FRInGE, HyP3, GMTSAR, SNAP, GAMMA or ROI_PAC format, and produces three dimensional (2D in space and 1D in time) ground surface displacement in line-of-sight direction. It includes a routine time series analysis (`smallbaselineApp.py`) and some independent toolbox. This repository consists about support action for MintPy, like clip tiff image from dataset from given `.shp` file, delete the current clipped tiff, and many more. If you want to use this, please use this script with the following step:

#### 1. Extract file with `extract.py`
If you process the InSAR with HyP3, the downloaded data must be originally in `.zip` file. Then we must to extract it with `extract.py` with the following command
```bash
python extract.py
```
#### 2. Clip the tiff dataset with `clip_tiff.py`
Then data must be clipped to our AoI (Area of Interest). We give example of what requirement should have before clipped the tiff file in the **geodata** folder, the given example can be done with Google Earth Pro to produce `.kml` or `.kmz` and then converted to `.shp`, `.shx`, etc. Then run following command
```bash
python clip_tiff.py
```
#### 3. Delete the tiff dataset with `delete.py`
If you want to delete the clipped tiff from dataset, use `delete.py` with command
```bash
python delete.py
```
and then run `clip_tiff.py` again to clip the tiff data.
#### 4. Or, if you want to automatic the process, just write bash command (EXPERIMENTAL)
```bash
bash process_data.sh
```
