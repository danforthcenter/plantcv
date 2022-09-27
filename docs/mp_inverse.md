## Moore-Penrose Inverse

Computes the Moore-Penrose Inverse Matrix, an important step in computing the homography for color correction.

**plantcv.transform.get_matrix_m**(*target_matrix, source_matrix*)

**returns** matrix_a, matrix_m, matrix_b

- **Parameters**
    - target_matrix - a *n* x 4 matrix containing the average red value, average green value, and average blue value for each color chip.
    - source_matrix - a *n* x 4 matrix containing the average red value, average green value, and average blue value for each color chip.

- **Returns**
    - matrix_a - a concatenated *n* x 9 matrix of source_matrix red, green, and blue values to the powers 1, 2, 3
    - matrix_m - a 9 x *n* Moore-Penrose inverse matrix
    - matrix_b - a *n* x 9 matrix of linear, quadratic, and cubic RGB values from `target_img`

```python

from plantcv import plantcv as pcv

matrix_a, matrix_m, matrix_b = pcv.transform.get_matrix_m(target_matrix=target_matrix, source_matrix=s_matrix)

print("Moore-Penrose Inverse Matrix: ")
print(matrix_m)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/transform/color_correction.py)
