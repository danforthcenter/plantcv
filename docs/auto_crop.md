## Auto Crop

Crops image to an object and allows user to specify image padding (if desired)

**plantcv.auto_crop**(*img, obj, padding_x=0, padding_y=0, color='black'*)

**returns** image after resizing

- **Parameters:**
    - img - RGB or grayscale image data
    - obj - contour of target object 
    - padding_x - padding in the x direction (default padding_x=0)
    - padding_y - padding in the y direction (default padding_x=0)
    - color - either 'black' (default), 'white', or 'image'
- **Context:**
    - Crops image to object
    
**Input image**

![Screenshot](img/documentation_images/auto_crop/2016-05-25_1031.chamber129-camera-01.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Crop image
crop_img = pcv.auto_crop(rgb_img, id_objects[0], 20, 20, 'black')

crop_img2 = pcv.auto_crop(rgb_img, id_objects[0], 20, 20, 'image')

```

**Debug Auto Crop Images**

![Screenshot](img/documentation_images/auto_crop/155_crop_area.jpg)

![Screenshot](img/documentation_images/auto_crop/155_auto_cropped.jpg)

![Screenshot](img/documentation_images/auto_crop/155_auto_image.jpg)

