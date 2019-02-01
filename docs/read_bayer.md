## Read Image with Bayer Mosaic

Reads image into numpy ndarray and splits the path and image filename. This is a wrapper for the OpenCV function [imread](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html). In contrast to `readimage`, this function is specifically designed to read images with Bayer mosaic pixel pattern and return a demosaicked image.

**plantcv.readbayer**(*filename, bayerpattern = 'BG', alg = "default"*)

**returns** img, path, image filename

- **Parameters:**
    - filename - image file to be read (possibly including a path)
    - bayerpattern  - arrangement of the pixels. Often found by trial and error. Either "BG" (default), "GB", "RG", "GR".
    - alg - algorithm with which to demosaic the image. Either "default" (default), "EdgeAware", "VariableNumberGradients". Not case sensitive.

- **Context:**
    - Reads in an image file with Bayer mosaic pixel pattern to be processed
- **Example use:**
    - Not exactly available, but could substitute for `readimage` [in VIS Tutorial](vis_tutorial.md)

```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

#read in image
img, path, img_filename = pcv.readbayer("home/user/images/test-image.tiff")
```
