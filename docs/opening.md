## Opening

Filters out bright noise from an image.

**plantcv.opening**(*gray_img, kernel=None*)

**returns** filtered_img

- **Parameters:**
    - gray_img - Grayscale or binary image data
    - kernel - Optional neighborhood, expressed as an array of 1's and 0's. If None, 
    use cross-shaped structuring element.
  - **Context:**
    - Used to reduce image noise, specifically small bright spots (i.e. "salt").
- **Example use:**
    - See below

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Apply opening

filtered_img = pcv.opening(gray_img)

```

**Grayscale image**

![Screenshot](img/documentation_images/opening/before_opening.jpg)

**Opening**

![Screenshot](img/documentation_images/opening/after_opening.jpg)
