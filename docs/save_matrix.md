## Save Matrix

Save a matrix from to '.npz' file. 

**plantcv.transform.save_matrix**(*matrix, 'filename'*)

**returns** none

- **Parameters**
    - matrix   = a numpy.matrix or numpy.ndarray
    - filename = name of file to which matrix will be saved. Must end in .npz
    
```python

from plantcv import plantcv as pcv
import numpy as np


filename = "test.npz"
matrix = np.matrix('1 2; 3 4')

pcv.transform.save_matrix(matrix, filename)

```

