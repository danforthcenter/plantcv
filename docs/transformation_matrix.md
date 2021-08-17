## Transformation Matrix

Computes the transformation matrix for application to a source image to transform it to the target color profile.

**plantcv.transform.calc_transformation_matrix**(*matrix_m, matrix_b*)

**returns** deviance, transformation_matrix 

- **Parameters**
    - matrix_m - a 9 x *n* Moore-Penrose inverse matrix
    - matrix_b - a *n* x 9 matrix of linear, quadratic, and cubic RGB values from target_img

- **Returns**
    - 1-t_det               - "deviance" the measure of how greatly the source image deviates from the target image's color space. Two images of the same color space should have a deviance of ~0.
    - transformation_matrix - a 9x9 matrix of linear, square, and cubic transformation coefficients

- **Example use:**
    - [Color Correction Tutorial](tutorials/transform_color_correction_tutorial.md)
    
```python

from plantcv import plantcv as pcv

deviance, transformation_matrix = pcv.transform.calc_transformation_matrix(matrix_m=matrix_m, matrix_b=matrix_b)

```

