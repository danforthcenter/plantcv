## Visualize composite of image tiles

This is a plotting method used to examine several output versions, such as from different model fits with varying parameters, all at once.

**plantcv.visualize.tile**(*images, nrow, ncol*)

**returns** comp_img

- **Parameters:**
    - images - A list of numpy arrays to tile into a composite.
    - nrow - Number of rows in composite output
    - ncol - Number of columns in composite output

- **Example use:**
    - Below


```python

from plantcv import plantcv as pcv

# Examine all images at once
composite = pcv.visualize.tile(images=images, nrow=3, ncol=3)

```

**Ouput**

![Screenshot](img/documentation_images/visualize_colorspaces/all_colorspaces.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/visualize/colorspaces.py)