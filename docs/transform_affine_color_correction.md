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

 Target Image

![Screenshot](img/documentation_images/correct_color_imgs/target_img_plant_resize.jpg)

 Source Image

![Screenshot](img/documentation_images/correct_color_imgs/source_img_plant.jpg)


```python

from plantcv import plantcv as pcv
import cv2

target_img, targetpath, targetname = pcv.readimage(filename="target_img.png")
source_img, sourcepath, sourcename = pcv.readimage(filename="source1_img.png")

target_mask, tmaskpath, tmaskname = pcv.readimage(filename="mask_img.png")
source_mask, smaskpath, smaskname = pcv.readimage(filename="mask_img.png") # in this case, as our images share a zoom level and colorchecker placement, the same mask is used for both the target and the source.

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = 'plot'

target_matrix, source_matrix, transformation_matrix, corrected_img = pcv.transform.correct_color(target_img=target_img,
                                                                                                 target_mask=t_mask,
                                                                                                 source_img=img,
                                                                                                 source_mask=mask,
                                                                                                 output_directory=outdir)

```

![Screenshot](img/documentation_images/correct_color_imgs/hstack.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/transform/color_correction.py)
