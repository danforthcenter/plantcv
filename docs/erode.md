## Erode

Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if 
conditions set in kernel are true, otherwise removes pixel.

**plantcv.erode**(*gray_img, ksize, i*)

**returns** image after erosion

- **Parameters:**
    - gray_img - Grayscale (usually binary) image data
    - ksize - Kernel size, an odd integer that is used to build a ksize x ksize matrix using np.ones. Must be greater than 1 to have an effect
    - i - An integer for number of iterations, i.e. the number of consecutive filtering passes
   
- **Context:**
    - Used to perform morphological erosion filtering. Helps remove isolated noise pixels or remove boundary of objects.
- **Example use:**
    - [Use In NIR Tutorial](tutorials/nir_tutorial.md)
    
**Input grayscale image**

![Screenshot](img/documentation_images/erode/grayscale_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Perform erosion filtering
# Results in removal of isolated pixels or boundary of object removal
er_img = pcv.erode(gray_img=gray_img, ksize=3, i=1)

```

**Image after erosion**

![Screenshot](img/documentation_images/erode/erosion.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/erode.py)
