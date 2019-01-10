## Color Palette

Returns a random list of RGB color values, equally spaced across a rainbow color spectrum.
If one color is requested, a random color is returned. Otherwise, evenly spaced colors are returned.

**plantcv.color_palette(*num*)**

**returns** colors

- **Parameters:**
    - num - an integer number greater than or equal to 1
- **Context:**
    - Used when a random set of colors is needed.

```python

from plantcv import plantcv as pcv

# Get one random color
colors = pcv.color_palette(1)
print(colors)
[(255, 16, 0)]

# Get five random colors
colors = pcv.color_palette(5)
print(colors)
[(0, 0, 255), (0, 255, 205), (100, 255, 0), (255, 106, 0), (255, 0, 199)]
```
