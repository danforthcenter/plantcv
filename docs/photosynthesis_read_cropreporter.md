## Read CropReporter Fluorescence Image Files

Reads .DAT image data into numpy ndarray and reshapes the frames into a datacube before identifying and extracting `fdark`, `fmin`, and `fmax` as separate numpy ndarrays. 

**plantcv.photosynthesis.read_cropreporter**(*filename*)

**returns** fdark, fmin, fmax

- **Parameters:**
    - filename - image file to be read (possibly including a path)
    
- **Context:**
    - Reads in file to be processed and does so using the metadata contained within a corresponding .INF file
- **Notes:**
    - This function assumes a specific pattern between .DAT image files and their corresponding .INF file. 
    We assume that for every image file `xx_PSD_xxx.DAT` there will be a corresponding metadata file with the same path
    named `xx_HDR_xxx.INF` 
- **Example use:**
    - [Use In PSII Tutorial](tutorials/psII_tutorial.md) 


```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

#read in image
fdark, fmin, fmax = pcv.photosynthesis.read_cropreporter(filename="PSII_PSD_20200826_22_rep6.DAT")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/photosynthesis/read_dat.py)
