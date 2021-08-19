## Checking a Color Card

We have added a function to help identify problems with color chips. One frequent issue that can happen is a color chip that is fully saturated, and would
be better off excluded from analysis . A quick way to examine this is by plotting the source matrix value against the target matrix value for all color chips
masked in the color card.

To see an example of how to check for problematic color chips see [here](tutorials/transform_color_correction_tutorial.md#checking-the-color-card-chips).

**plantcv.transform.quick_color_check**(*source_matrix, target_matrix, num_chips*)

**returns** none

- **Parameters**
    - source_matrix - a 22x4 matrix containing the average red value, average green value, and
                             average blue value for each color chip of the source image
    - target_matrix - a 22x4 matrix containing the average red value, average green value, and
                             average blue value for each color chip of the target image
    - num_chips     - the number of color card chips included in the matrices (integer)
    
- **Example use:**
    - [Color Correction Tutorial](tutorials/transform_color_correction_tutorial.md)
    

```python

from plantcv import plantcv as pcv

pcv.transform.quick_color_check(source_matrix=s_matrix, target_matrix=t_matrix, num_chips=24)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/transform/color_correction.py)
