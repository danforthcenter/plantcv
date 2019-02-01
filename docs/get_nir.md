## Get NIR Images

Gets NIR image that matches VIS image 

**plantcv.get_nir**(*path, filename*)

**returns** nir_path

- **Parameters:**
    - path - path to base image (vis image) to match
    - filename - filename of base image (vis image) to match
- **Context:**
    - This is a function that is likely only useful for those with multiple camera types. We use this function to find the matching NIR image to a VIS image,
that is found in the same directory but which contains multiple images (regex). Would need to be modified for different file naming structure / image types / file structures.  

- **Example use:**
 - [Use in VIS/NIR Tutorial](vis_nir_tutorial.md)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Get NIR image
nir_path = pcv.get_nir("/home/images/sorghum/snapshot1", "VIS_SV_90_z300_h1_g0_e85_v500_86939.png")
```

