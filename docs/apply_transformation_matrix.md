## Apply Transformation Matrix

Applies the transformation matrix to an image. 

**plantcv.transformation.apply_transformation_matrix**(*source_img, target_img, transformation_matrix*)

**returns** corrected_img

- **Parameters**
    - source_img            - an RGB image to be corrected to the target color space
    - target_img            - an RGB image with the target color space
    - transformation_matrix - a 9x9 matrix of transformation coefficients

- **Returns**
    - corrected_img - an RGB image in correct color space
    
- **Example use:**
    - [Color Correction Tutorial](tutorials/transform_color_correction_tutorial.md)
    
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

