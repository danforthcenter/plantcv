## Read Image

Reads image into numpy ndarray and splits the path and image filename. This is a wrapper for the OpenCV function [imread](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html).

**plantcv.readimage**(*filename, mode = "native"*)

**returns** img, path, image filename

- **Parameters:**
    - filename - image file to be read (possibly including a path)
    - mode     - return mode of image ("native," "rgb," or "gray"), defaults to "native"
    
- **Context:**
    - Reads in file to be processed
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md) 

```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

#read in image
img, path, img_filename = pcv.readimage("home/user/images/test-image.png", "native")
```
