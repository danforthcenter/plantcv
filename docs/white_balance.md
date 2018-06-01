## White Balance

Corrects the exposure of an image. A color standard can be specified.

**white_balance**(*device, img, mode='hist', debug=None,roi=None*)

**returns** device, img

- **Parameters:**
    - device - device number. Used to count steps in the pipeline
    - img - image on which to perform the correction
    - mode - either 'hist' or 'max', if 'hist' method is used a histogram for the whole image or the specified ROI is calculated, and the 
    bin with the most pixels is used as a reference point to shift image values. If 'max' is used as a method, then the pixel with the maximum
    value in the whole image or the specified ROI is used as a reference point to shift image values.
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
    - roi - A list of 4 points (x, y, width, height) that form the rectangular ROI of the white color standard.
            If a list of 4 points is not given, the whole image is used.

- **Context:**
    - Used to standardize exposure of images before thresholding

**Original image**

![Screenshot](img/documentation_images/white_balance/original_image.jpg)

```python
from plantcv import plantcv as pcv

# Corrects image based on color standard and stores output as corrected_img
device, corrected_img = pcv.white_balance(device,img,mode='hist', debug="print",roi=(5, 5, 80, 80))
```


**Corrected image**

![Screenshot](img/documentation_images/white_balance/corrected_image.jpg)
