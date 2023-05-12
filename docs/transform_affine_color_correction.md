## Correct Color using an affine transformation

Corrects the color of the input image based on the target color matrix using an affine transformation
in the RGB space. The vector containing the regression coefficients is calculated as the one that minimizes the
Euclidean distance between the transformed source color values and the target color values.

**plantcv.transform.affine_color_correction**(*rgb_img, source_matrix, target_matrix*)

**returns** corrected_img

**Important Note:** Each image must contain a reference from which color values are sampled.
 The following example uses a 24-color Colorchecker passport.

 - **Parameters:**
    - rgb_img       - an RGB image with color chips visualized
    - source_matrix - array of RGB color values (intensity in the range [0-1]) from the image to be corrected where each row is one color reference and the columns are organized as index,R,G,B
    - target_matrix - array of target RGB color values (intensity in the range [0-1]) where each row is one color reference and the columns are organized as index,R,G,B


**Reference Images**

 RGB image

![Screenshot](img/documentation_images/transform_affine_color_corr/tobacco_leaves.jpg)


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = 'plot'

# the source matrix needs to be computed form the RGB image, see the functions
# plantcv.transform.create_color_card_mask and plantcv.transform.get_color_matrix

# using standard color values for the color card
tgt_matrix = pcv.transform.std_color_matrix(pos=2)

corrected_img = pcv.transform.correct_color(rgb_img=img,
                                            source_matrix=src_matrix,
                                            target_matrix=tgt_matrix)

```

Corrected image

![Screenshot](img/documentation_images/transform_affine_color_corr/tobacco_leaves_corrected.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/transform/color_correction.py)
