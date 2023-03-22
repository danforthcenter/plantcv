## Flip Image

Flips an image in either the horizontal or vertical direction

**plantcv.flip**(*img, direction*)

**returns** flipped_image

- **Parameters:**
    - img - RGB or grayscale image data
    - direction - the direction you want the image flipped, either 'horizontal' or 'vertical'
- **Context:**
    - Used to flip images when necessary
- **Example use:**
    - Below

**Original image**

![Screenshot](img/documentation_images/flip/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Flip Image Horizontal
flipped= pcv.flip(img=img, direction='horizontal')

```

**Flipped Image**

![Screenshot](img/documentation_images/flip/flipped.jpg)

```python


# Flip Image Vertical
flipped= pcv.flip(img=img, direction='vertical')

```

**Flipped Image**

![Screenshot](img/documentation_images/flip/flipped1.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/flip.py)
