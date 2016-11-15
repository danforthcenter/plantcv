## Binary Threshold

Creates a binary image from a gray image based on the threshold values. 
The object target can be specified as dark or light.

<<<<<<< HEAD
**binary_threshold(*img, threshold, maxValue, object_type, device, debug=None*)**
=======
**binary_threshold(*img, threshold, maxValue, object_type, device, debug=False*)**
>>>>>>> master

**returns** device, thresholded image

- **Parameters:**
    - img - grayscale img object
    - threshold - threshold value (0-255)
    - maxValue - value to apply above threshold (255 = white)
    - objecttype - 'light' or 'dark', is target image light or dark?
    - device- Counter for image processing steps
<<<<<<< HEAD
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
=======
    - debug- Default value is False, if True, thresholded intermediate image will be printed
>>>>>>> master
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In NIR Tutorial](nir_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md)
    
**Original image**

![Screenshot](img/documentation_images/binary_threshold/original_image.jpg)

**Grayscale image (saturation channel)**

![Screenshot](img/documentation_images/binary_threshold/saturation_image.jpg)

```python
import plantcv as pcv

# Create binary image from a gray image based on threshold values. Targeting light objects in the image.
<<<<<<< HEAD
device, threshold_light = pcv.binary_threshold(img, 36, 255, 'light', device, debug="print")
=======
device, threshold_light = pcv.binary_threshold(img, 36, 255, 'light', device, debug=True)
>>>>>>> master
```

**Thresholded image**

![Screenshot](img/documentation_images/binary_threshold/thresholded_image.jpg)

```python
import plantcv as pcv

# Create binary image from a gray image based on threshold values. Targeting dark objects in the image.
<<<<<<< HEAD
device, threshold_dark = pcv.binary_threshold(img, 36, 255, 'dark', device, debug="print")
=======
device, threshold_dark = pcv.binary_threshold(img, 36, 255, 'dark', device, debug=True)
>>>>>>> master
```

**Thresholded image (inverse)**

![Screenshot](img/documentation_images/binary_threshold/thresholded_inverse_image.jpg)
