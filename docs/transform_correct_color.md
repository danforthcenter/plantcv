## Correct Color

Corrects the color profile of a source RGB image to the color profile of a target RGB image. This function outputs target_matrix, source_matrix, and transformation_matrix and saves them to the output directory as .npz files.
It also outputs, corrected_img, but storage (print or plot) is determined by debug mode. 

**plantcv.transform.correct_color**(*target_img, target_mask, source_img, source_mask, output_directory*)

**returns** target_matrix, source_matrix, transformation_matrix, corrected_img

**Important Note:** Each image must contain a reference from which color values are sampled.
 The following example uses a 24-color Colorchecker passport.

 - **Parameters:**
    - target_img       - an RGB image with color chips visualized
    - target_mask      - a grayscale image with color chips and background each represented with unique values
    - source_img       - an RGB image with color chips visualized
    - source_mask      - a grayscale image with color chips and background each represented as unique values
    - output_directory - a file path to which the target_matrix, source_matrix, and transformation_matrix will be save as .npz files


To see an example of how to create a grayscale mask of color chips see [here](tutorials/transform_color_correction_tutorial.md#creating-masks).


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

outdir = "."

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = 'plot'

target_matrix, source_matrix, transformation_matrix, corrected_img = pcv.transform.correct_color(target_img=target_img, 
                                                                                                 target_mask=t_mask, 
                                                                                                 source_img=img, 
                                                                                                 source_mask=mask, 
                                                                                                 output_directory=outdir)

```

![Screenshot](img/documentation_images/correct_color_imgs/hstack.jpg)

