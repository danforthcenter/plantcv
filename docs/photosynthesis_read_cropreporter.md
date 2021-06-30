## Read CropReporter Fluorescence Image Files

Reads .INF/.DAT image data into a PSII_data instance containing xarray DataArrays with labeled frames. 

**plantcv.photosynthesis.read_cropreporter**(*filename*)

**returns** ps, imgpath, inf_filename

- **Parameters:**
    - filename - INF metadata file to be read (possibly including a path). DAT files are automatically detected.
    
- **Context:**
    - Reads in binary image files to be processed and does so using the metadata contained within a corresponding .INF file. Measurements from dark-adapted plant state are stored in the attribute `darkadapted`. Frames F0 and Fm are labeled according to the metadata in .inf. The default measurement label is 't0'. Measurements from light-adapted plant state are stored in the attribute `lightadapted`. Frames Fp and Fmp are labeled according to the metadata in .inf. The default measurement label is 't1'.
- **Notes:**
    - This function assumes a specific pattern between .INF metadata file and their corresponding .DAT binary image filenames. 
    We assume that for every metadata file `xx_HDR_xxx.INF` there will be a corresponding image files with the same path
    named `xx_XXX_xxx.DAT` where XXX is the analysis protocol (e.g. PSD, PSL, etc.). Some crop reporter imaging protocols will results in multiple binary image .DAT files per .INF metadata file.  
- **Example use:**
    - [Use In PSII Tutorial](psII_tutorial.md) 


```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

#read in image
ps, imgpath, filename = pcv.photosynthesis.read_cropreporter(filename="PSII_HDR_20200826_22_rep6.INF")

# you can check which variables were imported at the prompt with:
ps


```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/photosynthesis/read_cropreporter.py)
