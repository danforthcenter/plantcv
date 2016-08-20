## White Balance

Corrects the exposure of an image. A color standard can be specified.

**white_balance**(*img, device, roi=None, debug=None*)

**returns** img

- **Parameters:**
    - img - A gray scale image on which to perform the correction
    - device - device number. Used to count steps in the pipeline
    - roi - A list of 4 points (x, y, width, height) that form the
    rectangular ROI of the white color standard.
          If a list of 4 points is not given, the whole image is used.
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None

- **Context:**
    - Used to standardize exposure of images before thresholding

**Original image**

![Screenshot](img/documentation_images/white_balance/original_image.jpg)

```python
import plantcv as pcv

# Corrects image based on color standard and stores output as corrected_img
corrected_img = pcv.white_balance(img, device, [5, 5, 80, 80], debug="print")
```


**Corrected image**

![Screenshot](img/documentation_images/white_balance/corrected_image.jpg)
