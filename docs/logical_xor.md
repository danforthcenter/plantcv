## Logical Operations - XOR

Join two images using the bitwise XOR operator (difference between the two images). Images must be the same size. 
This is a wrapper for the Opencv Function [bitwise_xor](https://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#bitwise-xor).  

**logical_xor**(*bin_img1, bin_img2*)

**returns** ='xor' image

- **Parameters:**
    - bin_img1 - Binary image data to be compared to bin_img2.
    - bin_img2 - Binary image data to be compared to bin_img1.
- **Context:**
    - Used to combine to images. Very useful when combining image channels that have been thresholded seperately.
- **Example use:**
    - Below

**Input binary image 1**

![Screenshot](img/documentation_images/logical_xor/19_binary_threshold120_inv.png)

**Input binary image 2**

![Screenshot](img/documentation_images/logical_xor/20_binary_threshold50.png)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"

# Combine two images that have had different thresholds applied to them.
# For logical 'xor' operation object pixel must be in either images 
# but not both to be included in 'xor' image.
xor_image = pcv.logical_xor(s_threshold, b_threshold)

```

**Combined image**

![Screenshot](img/documentation_images/logical_xor/21_xor_joined.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/logical_xor.py)
