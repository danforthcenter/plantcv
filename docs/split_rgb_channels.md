## Split RGB Channels

Split a `Spectral_data.pseudo_rgb` image into red, green, and blue grayscale channel images.

**plantcv.split_rgb_channels**(*img*)

**returns** tuple of split images `(r, g, b)`

- **Parameters:**
    - img - `Spectral_data` object (uses `pseudo_rgb`)

- **Context:**
    - Useful for one-off RGB channel math (for example, `R/G`, `R-G`, or normalized ratios)

- **Example use below:**

```python
from plantcv import plantcv as pcv

# Split channels from hyperspectral pseudo_rgb
r, g, b = pcv.split_rgb_channels(img=hsi_obj)

# One-off ratio
rg_ratio = r / (g + 1e-6)
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/split_rgb_channels.py)
