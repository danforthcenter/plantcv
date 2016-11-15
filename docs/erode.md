## Erode

Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if 
conditions set in kernel are true, otherwise removes pixel.

<<<<<<< HEAD
**erode**(*img, kernel, i, device, debug=None*)
=======
**erode**(*img, kernel, i, device, debug=False*)
>>>>>>> master

**returns** device, image after erosion

- **Parameters:**
    - img1 - Input image
<<<<<<< HEAD
    - kernel - An odd integer that is used to build a kernel x kernel matrix using np.ones
    - i - Iterations, i.e. the number of consecutive filtering passes
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
=======
    - kernel - Filtering window, you'll need to make your own using as such:  kernal = np.zeros((x,y), dtype=np.uint8), then fill the kernal with appropriate values
    - i - Iterations, i.e. the number of consecutive filtering passes
    - device - Counter for image processing steps
    - debug- Default value is False, if True, filled intermediate image will be printed
>>>>>>> master
- **Context:**
    - Used to perform morphological erosion filtering. Helps remove isolated noise pixels or remove boundary of objects.
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)
    
**Input grayscale image**

![Screenshot](img/documentation_images/erode/grayscale_image.jpg)

```python
import plantcv as pcv

# Perform erosion filtering
# Results in removal of isolated pixels or boundary of object removal
<<<<<<< HEAD
device, er_img = pcv.erosion(img, kernel, 1 device, debug='print')
=======
device, er_img = pcv.erosion(img, kernel, 1 device, debug=True)
>>>>>>> master
```

**Image after erosion**

![Screenshot](img/documentation_images/erode/erosion.jpg)
