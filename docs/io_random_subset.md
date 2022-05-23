## Random subset

This function returns a random subset of the elements in an input list.

**plantcv.io.random_subset**(*dataset, num=100, seed=None*)

**returns** sub_dataset

- **Parameters:**
    - dataset - List source of the samples
    - num     - Number of elements in the resulting subset
    - seed    - Optional seed for the random number generator

- **Context:**
    - This function is useful when a random portion of the elements in a list are required.

- **Example use:**

```python
from plantcv import plantcv as pcv

imgs_sub_set = pcv.io.random_subset(dataset=paths_to_imgs, num=5)
```
