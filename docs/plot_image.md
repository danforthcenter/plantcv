## Plot Image

Open the image in a window or plot in a Jupyter notebook using [matplotlib](https://matplotlib.org/).

**plot_image**(*img, cmap=None*)

**returns** none

- **Parameters:**
    - img - image object
    - cmap - matplotlib color map name (e.g. "gray", default: None)
- **Context:**
    - Often used to debug new image processing pipelines
    - Used to view images in Jupyter notebooks (or in a window) 
- **Example use:**
    - [Use In Jupyter](jupyter.md)  

```python

from plantcv import plantcv as pcv      
pcv.plot_image(img)
```
