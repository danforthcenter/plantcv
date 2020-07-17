## Color Palette

Returns a list of RGB color values, equally spaced across a color map. The color map used is configurable and colors
can either be returned in sequential or randomized order.

**plantcv.color_palette(*num*)**

**returns** colors

- **Parameters:**
    - num - an integer number greater than or equal to 1
- **Context:**
    - Used when a set of colors is needed.
    - See: [Multi-plant tutorial](multi-plant_tutorial.md), [Morphology tutorial](morphology_tutorial.md),
    [Spatial clustering](spatial_clustering.md), and [Watershed segmentation](watershed.md).
    - Visit the [Matplotlib](https://matplotlib.org/tutorials/colors/colormaps.html#sphx-glr-tutorials-colors-colormaps-py) website for a list of available colormaps.

```python

from plantcv import plantcv as pcv

# Get one color
colors = pcv.color_palette(1)
print(colors)
# [[255, 0, 40]]

# The color scale is saved for use by other functions
print(pcv.params.saved_color_scale)
# [[255, 0, 40]]

# To remove the saved scale, set it to None
pcv.params.saved_color_scale = None

# The color scale can be changed and the order can be changed from "sequential" to "random"
pcv.params.color_scale = "viridis"
pcv.params.color_sequence = "random"

# Get five colors
colors = pcv.color_palette(5)
print(colors)
# [[68, 1, 84], [94, 201, 97], [58, 82, 139], [253, 231, 36], [32, 144, 140]]

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/color_palette.py)
