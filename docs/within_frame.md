## Check whether an object is completely within an image

This function tests whether an object falls completely within the bounds of an image or if it touches the edge.

**plantcv.within_frame**(*mask, obj*)

**returns** in_bounds

- **Parameters:**
    - mask = a single channel image (i.e. binary or greyscale) that contains the object
    - obj = a single object from `find_objects()` or `object_composition()`

- **Context:**
    - This function could be used to test whether the plant has grown outside the field of view.
- **Example use:**

```python
from plantcv import plantcv as pcv      

img, path, img_filename = pcv.readimage("home/user/images/test-image.tif")
gray_img = pcv.rgb2gray_lab(img,'a')
mask = pcv.threshold.binary(gray_img, 36, 255, 'light')
id_objects, obj_hierarchy = pcv.find_objects(img, mask)
unified = pcv.object_composition(img, id_objects, obj_hierarchy)
pcv.within_frame(mask,unified)  #True or False?

```
