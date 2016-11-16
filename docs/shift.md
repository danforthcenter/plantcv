## Shift Image

Shifts image, but keeps dimensions the same

**shift_img**(*img, device, number, side='right', debug=None*)

**returns** device, image after shift

- **Parameters:**
    - img1 - Input image
    - device - Counter for image processing steps
    - number - number of rows or columns to add
    - side - "top", "bottom", "right", "left" where to add the rows or columns
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Shifts image from the specified direction.
- **Example use:**
    - [Use In Multi-Plant Tutorial](multi-plant_tutorial.md)
    
**Input image**

![Screenshot](img/documentation_images/shift/36_whitebalance.jpg)

```python
import plantcv as pcv

# Shift image
device, shifted_img = pcv.shift_img(img, device,300,"top", debug='print')
```

**Image after shift**

![Screenshot](img/documentation_images/shift/37_shifted.jpg)
