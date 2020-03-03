## Check whether an object is completely within an image

This function tests whether an object (defined as nonzero pixels in a mask) falls completely within the bounds of an image or if it touches the edge.

**plantcv.within_frame**(*mask*)

**returns** in_bounds

- **Parameters:**
    - mask = a single channel image (i.e. binary or greyscale)

- **Context:**
    - This function could be used to test whether the plant has grown outside the field of view.
- **Output data stored:** Data ('in_bounds') automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

- **Example use:**

```python
from plantcv import plantcv as pcv      

img, path, img_filename = pcv.readimage("home/user/images/test-image.tif")
gray_img = pcv.rgb2gray_lab(img,'a')
mask = pcv.threshold.binary(gray_img, 36, 255, 'light')
in_bounds = pcv.within_frame(mask)  #True or False?

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/within_frame.py)
