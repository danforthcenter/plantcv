## Print Image

Write image to the file specified. This is a wrapper for the OpenCV function [imwrite](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html)
for numpy arrays (like the images that get returned by most PlantCV functions), and can handle matplotlib Figures (like the one returned by [pcv.visualize.pseudocolor](visualize_pseudocolor.md)) 
and plotnine ggplots (like the histograms returned in [pcv.analyze_nir_intensity](analyze_NIR_intensity.md), 
[pcv.analyze_color](analyze_color.md), [pcv.visualize.histogram](visualize_histogram.md),
 and [pcv.photosynthesis.analyze_fvfm](photosynthesis_analyze_fvfm.md)).

**plantcv.print_image**(*img, filename*)

**returns** none

- **Parameters:**
    - img- image object
    - filename- desired name of image file, supported extensions are PNG, JPG, and TIFF
- **Context:**
    - Often used to debug new image processing workflows
    - Used to write out final results images  
- **Example use:**
    - [Use In VIS Tutorial](tutorials/vis_tutorial.md)  

```python

from plantcv import plantcv as pcv

pcv.print_image(img, "home/user/images/test-image.png")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/print_image.py)
