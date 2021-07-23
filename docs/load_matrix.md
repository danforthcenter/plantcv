## Load Matrix

Load a matrix from an '.npz' file. 

**plantcv.transform.load_matrix**(*filename*)

**returns** matrix

- **Parameters**
    - filename - a .npz filename of a matrix

- **Returns**
    - matrix - an ndarray loaded from a '.npz' file
    
- **Example use:**
    - [Color Correction Tutorial](tutorials/transform_color_correction_tutorial.md)

```python

from plantcv import plantcv as pcv

filename = "test.npz"

matrix = pcv.transform.load_matrix(filename=filename)

```
