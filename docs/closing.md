## Closing

Filters out dark noise from an image.

**plantcv.closing**(*gray_img, kernel=None*)

**returns** filtered_img

- **Parameters:**
    - gray_img - Grayscale or binary image data
    - kernel - Optional neighborhood, expressed as an array of 1's and 0's. See the [kernel making](get_kernel.md) function. If None, 
    use cross-shaped structuring element.
  - **Context:**
    - Used to reduce image noise, specifically small dark spots (i.e. "pepper").
- **Example use:**
    - See below

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Apply closing
filtered_img = pcv.closing(gray_img=gray_img)

```

**Grayscale image**

![Screenshot](img/documentation_images/closing/before_closing.jpg)

**Closing**

![Screenshot](img/documentation_images/closing/after_closing.jpg)


In addition to the [kernel making](get_kernel.md) function users can create custom kernel shapes. 
```python

# Apply closing with an X-shaped kernel 
filtered_img = pcv.closing(gray_img=gray_img, kernel=np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]]))

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/closing.py)
