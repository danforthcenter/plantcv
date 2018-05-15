## Create a Region of Interest (ROI) from a binary image

**plantcv.roi.from_binary_image**(*bin_img, img*)

**returns** roi_contour, roi_hierarchy

- **Parameters:**
    - bin_img - Binary image. The ROI contour will be identified from this image.
    - img - An RGB or grayscale image to plot the ROI on in debug mode.
- **Context:**
    - Used to define a region of interest in the image.

**Binary Image**

![Screenshot](img/documentation_images/from_binary_image/binary_image.png)

```python
import plantcv.roi

roi_contour, roi_hierarchy = plantcv.roi.from_binary_image(bin_img=bin_img, img=rgb_img)
```

![Screenshot](img/documentation_images/from_binary_image/image_with_roi.png)
