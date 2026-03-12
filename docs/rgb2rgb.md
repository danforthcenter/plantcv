## RGB Channel to Gray

Return a single channel from an RGB image as a grayscale image.

**plantcv.rgb2gray_rgb**(*rgb_img, channel*)

**returns** split image (r, g, or b channel)

- **Parameters:**
    - rgb_img - RGB image data
    - channel - Split 'r' (red), 'g' (green), or 'b' (blue) channel

- **Context:**
    - Used to help differentiate plant and background in raw RGB channels
- **Example use below:**

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Green ('g') channel is output
g_channel = pcv.rgb2gray_rgb(rgb_img=rgb_img, channel='g')
```

```python
# Red ('r') channel is output
r_channel = pcv.rgb2gray_rgb(rgb_img=rgb_img, channel='r')
```

```python
# Blue ('b') channel is output
b_channel = pcv.rgb2gray_rgb(rgb_img=rgb_img, channel='b')
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/rgb2gray_rgb.py)
