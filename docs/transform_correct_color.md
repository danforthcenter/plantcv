## Correct Color

Corrects the color profile of a source RGB image to the color profile of a target RGB image. This function outputs target_matrix, source_matrix, and transformation_matrix and saves them to the output directory as .npz files.
It also outputs, corrected_img, but storage (print or plot) is determined by debug mode. 

**plantcv.transform.correct_color**(*target_img, target_mask, source_img, source_mask, output_directory*)

**returns** target_matrix, source_matrix, transformation_matrix, corrected_img

**Important Note:** Each image must contain a reference from which color values are sampled.
 The following example uses a 24-color Colorchecker passport.

 - **Parameters:**
    - target_img       = an RGB image with color chips visualized
    - target_mask      = a grayscale image with color chips and background each represented with unique values
    - source_img       = an RGB image with color chips visualized
    - source_mask      = a grayscale image with color chips and background each represented as unique values
    - output_directory = a file path to which the target_matrix, source_matrix, and transformation_matrix will be save as .npz files


To see an example of how to create a grayscale mask of color chips see [here](transform_color_correction_tutorial.md#creating-masks).


**Reference Images**

 Target Image

![Screenshot](img/documentation_images/correct_color_imgs/target_img_plant_resize.jpg)

 Source Image
 
![Screenshot](img/documentation_images/correct_color_imgs/source_img_plant.jpg)


```python

from plantcv import plantcv as pcv
import cv2

target_img = cv2.imread("target_img.png")
source_img = cv2.imread("source1_img.png")

target_mask = cv2.imread("mask_img.png", -1) # mask must be read in "as-is" include -1
source_mask = cv2.imread("mask_img.png", -1) # in this case, as our images share a zoom level and colorchecker placement, the same mask is used for both the target and the source.

output_directory = "."

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = 'plot'

target_matrix, source_matrix, transformation_matrix, corrected_img = pcv.transform.correct_color(target_img, target_mask, source_img, source_mask, output_directory)

```

![Screenshot](img/documentation_images/correct_color_imgs/hstack.jpg)




## Transformation Matrix

Computes the transformation matrix for application to a source image to transform it to the target color profile.

**plantcv.transform.calc_transformation_matrix**(*matrix_m, matrix_b*)

**returns** deviance, transformation_matrix 

- **Parameters**
    - matrix_m = a 9 x *n* Moore-Penrose inverse matrix
    - matrix_b = a *n* x 9 matrix of linear, quadratic, and cubic RGB values from target_img

- **Returns**
    - 1-t_det               = "deviance" the measure of how greatly the source image deviates from the target image's color space. Two images of the same color space should have a deviance of ~0.
    - transformation_matrix = a 9x9 matrix of linear, square, and cubic transformation coefficients


```python

from plantcv import plantcv as pcv

deviance, transformation_matrix = pcv.transform.calc_transformation_matrix(matrix_m, matrix_b)

```


## Apply Transformation Matrix

Applies the transformation matrix to an image. 

**plantcv.transformation.apply_transformation_matrix**(*source_img, target_img, transformation_matrix*)

**returns** corrected_img

- **Parameters**
    - source_img            = an RGB image to be corrected to the target color space
    - target_img            = an RGB image with the target color space
    - transformation_matrix = a 9x9 matrix of transformation coefficients

- **Returns**
    - corrected_img = an RGB image in correct color space
    
**Reference Images**

  Target Image
  
![Screenshot](img/documentation_images/correct_color_imgs/target_img_plant_resize.jpg)
    
  Source Image
  
![Screenshot](img/documentation_images/correct_color_imgs/source_img_plant.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

corrected_img = pcv.transform.apply_transformation_matrix(source_img=source_img, target_img=target_img, transformation_matrix=transformation_matrix)

```

![Screenshot](img/documentation_images/correct_color_imgs/hstack.jpg)


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


## Load Matrix

Load a matrix from an '.npz' file. 

**plantcv.transform.load_matrix**(*'filename'*)

**returns** matrix

- **Parameters**
    - matrix = an ndarray loaded from a '.npz' file
    
```python

from plantcv import plantcv as pcv

filename = "test.npz"

matrix = pcv.transform.load_matrix(filename)

```

## Checking a Color Card

We have added a function to help identify problems with color chips. One frequent issue that can happen is a color chip that is fully saturated, and would
be better off excluded from analysis . A quick way to examine this is by plotting the source matrix value against the target matrix value for all color chips
masked in the color card.

To see an example of how to check for problematic color chips see [here](transform_color_correction_tutorial.md#checking-the-color-card-chips).

**plantcv.transform.quick_color_check**(*source_matrix, target_matrix, num_chips*)

**returns** none

- **Parameters**
    - source_matrix = a 22x4 matrix containing the average red value, average green value, and
                             average blue value for each color chip of the source image
    - target_matrix = a 22x4 matrix containing the average red value, average green value, and
                             average blue value for each color chip of the target image
    - num_chips     = the number of color card chips included in the matrices (integer)

```python

from plantcv import plantcv as pcv
from plotnine import *

pcv.transform.quick_color_check(source_matrix = s_matrix, target_matrix = t_matrix, num_chips = 24)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/transform/color_correction.py)
