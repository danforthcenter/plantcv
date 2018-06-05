## Erode

Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if 
conditions set in kernel are true, otherwise removes pixel.

**erode**(*img, kernel, i, device, debug=None*)

**returns** device, image after erosion

- **Parameters:**
    - img1 - Input image
    - kernel - An odd integer that is used to build a kernel x kernel matrix using np.ones
    - i - Iterations, i.e. the number of consecutive filtering passes
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to perform morphological erosion filtering. Helps remove isolated noise pixels or remove boundary of objects.
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)
    
**Input grayscale image**

![Screenshot](img/documentation_images/erode/grayscale_image.jpg)

```python
from plantcv import plantcv as pcv

# Perform erosion filtering
# Results in removal of isolated pixels or boundary of object removal
device, er_img = pcv.erosion(img, kernel, 1 device, debug='print')
```

**Image after erosion**

![Screenshot](img/documentation_images/erode/erosion.jpg)
