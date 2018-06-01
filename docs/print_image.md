## Print Image

Write image to the file specified. This is a wrapper for the OpenCV function [imwrite](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html).

**print_image**(*img, filename*)

**returns** none

- **Parameters:**
    - img- image object
    - filename- desired name of image file, supported extensions are PNG, JPG, and TIFF
- **Context:**
    - Often used to debug new image processing pipelines
    - Used to write out final results images  
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)  

```python
from plantcv import plantcv as pcv      
pcv.print_image(img, "home/user/images/test-image.png")
```
