## Image add

This is a method used to perform pixelwise addition between images. 
The numpy addition function '+' is used. This is a modulo operation rather 
than the cv2.add fxn which is a saturation operation.

**plantcv.image_add**(*gray_img1, gray_img2*)

**returns** image of the sum of both images

- **Parameters:**
    - gray_img1 - Grayscale image data to be added to image 2
    - gray_img2 - Grayscale image data to be added to image 1
- **Context:**
    - Used to combine/stack the pixelwise intensity found in two images
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)
    
**Image 1 to be added**

![Screenshot](img/documentation_images/image_add/image1.jpg)

**Image 2 to be added**

![Screenshot](img/documentation_images/image_add/image2.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Add two images together
# Results to combine/stack the pixelwise intensity found in two images
sum_img = pcv.image_add(img1, img2)
```

**Sum of images 1 and 2**

![Screenshot](img/documentation_images/image_add/added_image.jpg)
