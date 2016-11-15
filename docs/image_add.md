## Image add

This is a method used to perform pixelwise addition between images. 
The numpy addition function '+' is used. This is a modulo operation rather 
than the cv2.add fxn which is a saturation operation.

<<<<<<< HEAD
**image_add**(*img1, img2, device, debug=None*)
=======
**image_add**(*img1, img2, device, debug=False*)
>>>>>>> master

**returns** device, image of the sum of both images

- **Parameters:**
    - img1 - image to add
    - img2 - image to add
    - device - Counter for image processing steps
<<<<<<< HEAD
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
=======
    - debug- Default value is False, if True, filled intermediate image will be printed
>>>>>>> master
- **Context:**
    - Used to combine/stack the pixelwise intensity found in two images
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)
    
**Image 1 to be added**

![Screenshot](img/documentation_images/image_add/image1.jpg)

**Image 2 to be added**

![Screenshot](img/documentation_images/image_add/image2.jpg)

```python
import plantcv as pcv

# Add two images together
# Results to combine/stack the pixelwise intensity found in two images
<<<<<<< HEAD
device, sum_img = pcv.image_add(img1, img2 device, debug="print")
=======
device, sum_img = pcv.image_add(img1, img2 device, debug=True)
>>>>>>> master
```

**Sum of images 1 and 2**

![Screenshot](img/documentation_images/image_add/added_image.jpg)
