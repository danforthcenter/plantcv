## Invert

Invert a binary image. This is a wrapper for the OpenCV function [bitwise_not](http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#bitwise-not)

<<<<<<< HEAD
**invert**(*img, device, debug=None*)
=======
**invert**(*img, device, debug=False*)
>>>>>>> master

**returns** device, inverted image

- **Parameters:**
    - img = image to be inverted (works best with binary image)
    - device- Counter for image processing steps
<<<<<<< HEAD
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
=======
    - debug- Default value is False, if True, masked intermediate image will be printed
>>>>>>> master
- **Context:**
    - Invert image values. Useful for inverting an image mask.
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md)
    
**Input binary image**

![Screenshot](img/documentation_images/invert/binary_image.jpg)

```python
import plantcv as pcv

# Invert a binary mask.
<<<<<<< HEAD
device, inverted_img = pcv.invert(img, device, debug="print")
=======
device, inverted_img = pcv.invert(img, device, debug=True)
>>>>>>> master
```

**Inverted image**

![Screenshot](img/documentation_images/invert/inverted_image.jpg)
