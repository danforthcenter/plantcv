## Load Matrix

Load a matrix from an '.npz' file. 

**plantcv.transform.load_matrix**(*filename*)

**returns** matrix

- **Parameters**
    - matrix = an ndarray loaded from a '.npz' file
    
```python

from plantcv import plantcv as pcv

filename = "test.npz"

matrix = pcv.transform.load_matrix(filename)

```
