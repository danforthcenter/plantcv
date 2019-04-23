## Watershed Segmentation

This function is based on code contributed by Suxing Liu, Arkansas State University.
For more information see [https://github.com/lsx1980/Leaf_count](https://github.com/lsx1980/Leaf_count).
This function uses the watershed algorithm to detect boundary of objects.
Needs a mask file which specifies area which is object is white, and background is black.
Requires cv2 version 3.0+

**plantcv.watershed_segmentation**(*rgb_img, mask, distance=10*)**

**returns** analysis_images

- **Parameters:**
    - rgb_img - RGB image data
    - mask - binary image, single channel, object in white and background black
    - distance - min_distance of local maximum, lower values are more sensitive, and segments more objects (default: 10)
    - filename - if user wants to output analysis images change filenames from False (default)
- **Context:**
    - Used to segment image into parts
    - Data automatically gets stored into the [Outputs class](outputs.md). Users can look at the data collected at any point during 
    the workflow by using [pcv.print_results](print_results.md) which prints all stored data to a .json file.

**Original image**

![Screenshot](img/documentation_images/watershed/543_auto_cropped.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Segment image with watershed function
analysis_images = pcv.watershed_segmentation(crop_img, thresh, 10)

```

**Watershed Segmentation**

![Screenshot](img/documentation_images/watershed/watershed.jpg)
