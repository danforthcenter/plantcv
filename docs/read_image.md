## Read Image

Reads image into numpy ndarray and splits the path and image filename. This is a wrapper for the OpenCV function [imread](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html).

**readimage**(*filename, debug=None*)

**returns** img, path, image filename

- **Parameters:**
    - filename - image file to be read (possibly including a path)
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Reads in file to be processed
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md) 

```python
from plantcv import base as pcv      
img, path, img_filename=pcv.readimage("home/user/images/test-image.png")
```
