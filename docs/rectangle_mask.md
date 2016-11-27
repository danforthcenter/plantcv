## Mask-Rectangle

Takes an input image and returns a binary image masked by a rectangular area denoted by p1 and p2. 
Note that p1 = (0,0) is the top left hand corner bottom right hand corner is p2 = (max-value(x), max-value(y)).

**rectangle_mask**(*img, point1, point2, device, debug=None*)

**returns** device, masked, binary img, contours, hierarchy 

- **Parameters:**
    - img - Input image
    - p1 - Point is the top left corner of rectangle (0,0) is top left corner
    - p2 - Point is the bottom right corner of rectangle (max-value(x),max-value(y)) is bottom right corner
    - device - Counter for image processing steps
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
    - color - default is "black" this acts to select (mask) area from object capture (need to invert to remove)
- **Context:**
    - Used to mask rectangular regions of an image
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)
    
**Grayscale image**

![Screenshot](img/documentation_images/rectangle_mask/grayscale_image.jpg) 

```python
import plantcv as pcv

# Makes a rectangle area that will be treated as a mask
device, masked, binary, contours, hierarchy = pcv.rectangle_mask(img, (0,0), (75,252), device, debug="print", color="black")
```

**Region of interest**

![Screenshot](img/documentation_images/rectangle_mask/roi.jpg) 

**Masked image**

![Screenshot](img/documentation_images/rectangle_mask/masked.jpg) 
