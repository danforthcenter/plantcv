## Check If An Object Is Within Frame

This function tests whether an object (defined as nonzero pixels in a mask) falls completely within the bounds of an 
image, or if it touches the edge.

**plantcv.within_frame**(*mask, border_width=1, label=None*)

**returns** in_bounds

- **Parameters:**
    - mask - a single channel image (i.e. binary or greyscale)
    - border_width - distance from border of image considered out of frame (default = 1)
    - label - Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)

- **Context:**
    - This function could be used to test whether the plant has grown outside the field of view.
    
- **Output data stored:** Data ('in_bounds') automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow. For more detail about data output see 
    [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

- **Example use:**

```python
from plantcv import plantcv as pcv      

img, path, img_filename = pcv.readimage(filename="home/user/images/test-image.tif")
gray_img = pcv.rgb2gray_lab(rgb_img=img, channel='a')
mask = pcv.threshold.binary(gray_img=gray_img, threshold=36, object_type='light')
in_bounds = pcv.within_frame(mask=mask)  #True or False?

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/within_frame.py)
