## Auto Crop

Crops image to an object and allows user to specify image padding (if desired)

**auto_crop**(*device, img, objects, padding_x=0, padding_y=0, color='black',debug=None*)

**returns** device, image after resizing

- **Parameters:**
    - img1 - Input image
    - object - contour of target object 
    - padding_x - padding in the x direction
    - padding_y - padding in the y direction
    - color - either 'black' or 'white'
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Crops image to object
    
**Input image**

![Screenshot](img/documentation_images/auto_crop/2016-05-25_1031.chamber129-camera-01.jpg)

```python
import plantcv as pcv

# Resize image
device, crop_img=pcv.auto_crop(device, img, id_objects[0],20,20,'black',debug)
```

**Debug Auto Crop Images**

![Screenshot](img/documentation_images/auto_crop/155_crop_area.jpg)
-------------------------------------------------------------------
![Screenshot](img/documentation_images/auto_crop/155_auto_cropped.jpg)
