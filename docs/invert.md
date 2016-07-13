## Invert

Invert a binary image. This is a wrapper for the OpenCV function [bitwise_not](http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#bitwise-not)

**invert**(*img, device, debug=False*)

**returns** device, inverted image

- **Parameters:**
    - img = image to be inverted (works best with binary image)
    - device- Counter for image processing steps
    - debug- Default value is False, if True, masked intermediate image will be printed
- **Context:**
    - Invert image values. Useful for inverting an image mask.

**Input binary image**

![Screenshot](img/documentation_images/invert/binary_image.jpg)

```python
import plantcv as pcv

# Invert a binary mask.
device, inverted_img = pcv.invert(img, device, debug=True)
```

**Inverted image**

![Screenshot](img/documentation_images/invert/inverted_image.jpg)
