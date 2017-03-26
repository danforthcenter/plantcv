## Triangle Auto Threshold

Creates a binary image from a gray image using adaptive thresholding.

**triangle_auto_threshold(*device, img, maxvalue, object_type, xstep=1, debug=None*)**

**returns** device, thresholded image

- **Parameters:**
    - device- Counter for image processing steps
    - img - grayscale img object
    - maxValue - value to apply above threshold (255 = white)
    - objecttype - 'light' or 'dark', is target image light or dark?
    - xstep - value to move along x-axis to determine the points from which to calculate distance
              recommended to start at 1 and change if needed)
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to help differentiate plant and background
    

**Grayscale image (green-magenta channel)**

![Screenshot](img/documentation_images/triangle_threshold/input_gray_img.jpg)


```python
import plantcv as pcv

# Create binary image from a gray image based
device, thresholded= pcv.triangle_auto_threshold(device,img, 255,'light', xstep=10, debug="print")
```

**Triangle Auto-Thresholded image (xstep=10)**

![Screenshot](img/documentation_images/triangle_threshold/4_triangle_thresh_hist_30.0.jpg)
![Screenshot](img/documentation_images/triangle_threshold/4_triangle_thresh_img_30.0.jpg)

```python
import plantcv as pcv

# Create binary image from a gray image based 
device, thresholded= pcv.triangle_auto_threshold(device,img, 255,'light', xstep=1, debug="print")
```

**Triangle Auto-Thresholded image (xstep=1)**

![Screenshot](img/documentation_images/triangle_threshold/11_triangle_thresh_hist_3.0.jpg)
![Screenshot](img/documentation_images/triangle_threshold/11_triangle_thresh_img_3.0.jpg)
