## Read Image

Reads image into numpy ndarray and splits the path and image filename. This is a wrapper for the OpenCV function [imread](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html).

**plantcv.readimage**(*filename, mode = "native"*)

**returns** img, path, image filename

- **Parameters:**
    - filename - image file to be read (possibly including a path)
    - mode     - return mode of image ("native," "rgb,", "rgba", or "gray"), defaults to "native"
    
- **Context:**
    - Reads in file to be processed
- **Note:**
    - In most cases, the alpha channel in RGBA image data is unused (and causes issue when used as RGB image data),
    so unless specificed as `mode='rgba'` the `pcv.readimage()` function will read RGBA data in as an RGB image under
    default settings (`mode='native'`). However, if the alpha channel is needed users can specify `mode='rgba'`. 
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md) 

```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

#read in image
img, path, img_filename = pcv.readimage("home/user/images/test-image.png", "native")

```
