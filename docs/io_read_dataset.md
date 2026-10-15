## Read dataset

This function reads a dataset of images as a list of paths.

**plantcv.io.read_dataset**(*img_dir, pattern='', sort=True*)

**returns** image_dataset

- **Parameters:**
    - img_dir - Path to the directory of images
    - pattern     - Optional, the function returns only the paths where the filename contains the pattern.
    - sort        - True by default, sorts the paths alphabetically


- **Context:**
    - This function is useful when it is required to read a set of images containing a given pattern.


- **Example use:**

```python
from plantcv import plantcv as pcv

image_dataset = pcv.io.read_dataset(img_dir='./data/', pattern='color')

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/io/read_dataset.py)
