## Get Kernel

Create a kernel structuring element

**plantcv.get_kernel**(*size, shape*)

**returns** filtered_img

- **Parameters:**
    - size - Kernel size (n,m). A (n x m) kernel will be built. Must be greater than 1 to have an effect.
    - shape - Element shape, either "rectangle", "cross", or "ellipse".
  - **Context:**
    - Create a kernel structuring element to be used in various filter functions i.e. [closing](closing.md) and [opening](opening.md)
- **Example use:**
    - See below

```python

from plantcv import plantcv as pcv

# get a rectangular kernel
rectangle_kernel = pcv.get_kernel(size=(3,4), shape="rectangle")
print(rectangle_kernel)
[[1 1 1]
 [1 1 1]
 [1 1 1]
 [1 1 1]]
 
 # get an elliptical kernel
ellipse_kernel = pcv.get_kernel(size=(7,7), shape="ellipse")
print(ellipse_kernel)
[[0 0 0 1 0 0 0]
 [0 1 1 1 1 1 0]
 [1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1]
 [0 1 1 1 1 1 0]
 [0 0 0 1 0 0 0]]
 
 # get a cross shaped kernel
cross_kernel = pcv.get_kernel(size=(5,3), shape="cross")
print(cross_kernel)
[[0 0 1 0 0]
 [1 1 1 1 1]
 [0 0 1 0 0]]

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/get_kernel.py)

