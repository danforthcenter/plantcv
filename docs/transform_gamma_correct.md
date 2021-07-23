## Gamma Correction

Wrapper for scikit-image gamma correction function. Performs Gamma Correction on the input image. Also known as 
    Power Law Transform. This function transforms the input image pixelwise according to the equation O = I**gamma 
    after scaling each pixel to the range 0 to 1.

**plantcv.transform.gamma_correct**(*img, gamma=1, gain=1*)

**returns** corrected_img

- **Parameters**
    - img - RGB or grayscale image on which to perform the correction.
    - gamma - non-negative real number. Default value is 1.
    - gain - the constant multiplier. Default value is 1.

**Original Image**

![Screenshot](img/documentation_images/gamma_correct/original_image.png)

```python
from plantcv import plantcv as pcv

corrected_img = pcv.transform.gamma_correct(img=img, gamma=1, gain=1)

```

**Corrected Image**

![Screenshot](img/documentation_images/gamma_correct/corrected_image.png)

**Source Code**: [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/transform/gamma_correct.py)