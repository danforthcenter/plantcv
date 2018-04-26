## Create a Region of Interest (ROI) from a binary image

**from_binary_image**(*bin_img, rgb_img=None*)

**returns** roi_contour, roi_hierarchy

- **Parameters:**
    - bin_img  - Binary image. The ROI contour will be identified from this image.
    - rgb_img  - An RGB image to plot the ROI on. Default is None, only needed in conjunction with debugging.
- **Context:**
    - Used to define a region of interest in the image.

**Binary Image**

![Screenshot](img/documentation_images/from_binary_image/binary_image.png)

```python
import plantcv.roi

roi_contour, roi_hierarchy = plantcv.roi.from_binary_image(bin_img=bin_img, rgb_img=rgb_img)
```

![Screenshot](img/documentation_images/from_binary_image/image_with_roi.png)
