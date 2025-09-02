## Open an image from a URL

Opens an image file stored at a URL.

**plantcv.io.open_url**(*url*)

**returns** img

- **Parameters:**
    - url - URL of the image file to be opened
- **Context:**
    - Used to open an image file stored at a URL
- **Example use:**

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Open image from URL
img = pcv.io.open_url(url="https://plantcv.org/s/plantcv-hyperspectral.png")

```

**Image**

<img title="PlantCV logo" alt="PlantCV logo" src="https://plantcv.org/s/plantcv-hyperspectral.png" width="300px">

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/io/open_url.py)
