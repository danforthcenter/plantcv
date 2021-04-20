## Visualize label image

This is a plotting method used to visualize label image.

**plantcv.visualize.colorize_label_img**(*label_img*)

**returns** colored_img

- **Parameters:**
    - label_img - A label image, i.e. a 2d image with int values at every pixel, where the values represent for the class the pixel belongs to
- **Context:**
    - Visualize different class labels in one image
- **Example use:**
    - [Use In Machine Learning Tutorial](machine_learning_tutorial.md)

**Original image**

![Screenshot](img/tutorial_images/machine_learning/color_image.jpg) 

```python

from plantcv import plantcv as pcv

colored_img = pcv.visualize.colorize_label_img(label_img=label_img)
                                       
```

**Plot with Colored Masks**

![Screenshot](img/documentation_images/colorize_masks/colored_classes.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/colorize_label_img.py)
