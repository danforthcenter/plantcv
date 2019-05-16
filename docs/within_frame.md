## Check whether an object is completely within an image

This function tests whether an object (defined as any nonzero pixels) falls completely within the bounds of an image or if it touches the edge.

**plantcv.within_frame**(*mask*)

**returns** in_bounds

- **Parameters:**
    - mask = a single channel image (i.e. binary or greyscale)

- **Context:**
    - This function could be used to test whether the plant has grown outside the field of view.
- **Example use:**

```python
from plantcv import plantcv as pcv      

img, path, img_filename = pcv.readimage("home/user/images/test-image.tif")
gray_img = pcv.rgb2gray_lab(img,'a')
mask = pcv.threshold.binary(gray_img, 36, 255, 'light')
pcv.within_frame(mask)  #True or False?

```
