## Region of interest to mask

Convert a region of interest/object contour to a binary mask of the same shape 

**plantcv.roi2mask**(*img, contour*)

**returns** mask

- **Parameters:**
    - img - RGB or grayscale image data
    - contour - ROI or other object contour
   
- **Context:**
    - `img` parameter is only used to determine the size of the mask getting created. 
- **Example use:**
    - below

**Original RGB image**

![Screenshot](img/documentation_images/rgb2lab/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Read in the image 
img, filename, filepath = pcv.readimage(filename="plant_image.png")

roi_contour, roi_hierarchy = pcv.roi.custom(img=img, vertices=[[1190,490], [1470,830], [920,1430], [890,950]])
            
# image converted from RGB to LAB, channels are then split. 
# Lightness ('l') channel is outputed.
mask = pcv.roi2mask(img=img, contour=roi_contour)

```

**Lightness channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_lightness.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# image converted from RGB to LAB, channels are then split. 
# Green-Magenta ('a') channel is outputed.
a_channel = pcv.rgb2gray_lab(rgb_img, 'a')

```

**Green-Magenta channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_green-magenta.jpg)
   
```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# image converted from RGB to Lab, channels are then split. 
# Blue-Yellow ('b') channel is outputed.
b_channel = pcv.rgb2gray_lab(rgb_img, 'b')

```

**Blue-Yellow channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_blue-yellow.jpg)
