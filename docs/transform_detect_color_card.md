## Automatically Detect a Color Card

Automatically detects a color card and creates a mask. 

**plantcv.transform.detect_color_card**(*rgb_img, label=None*)

**returns** labeled_mask

- **Parameters**
    - rgb_img          - Input RGB image data containing a color card.
    - label - Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)
- **Returns**
    - labeled_mask     - Labeled color card mask (useful in `pcv.transform.get_color_matrix` and `pcv.transform.affine_color_correction`)

**Important Note:** This function isn't entirely robust. There are a few important assumptions that must be met in order to automatically detect color cards:

- There is only one color card in the image.
- Color card should be 4x6 (like an X-Rite ColorChecker Passport Photo). 

```python

from plantcv import plantcv as pcv
rgb_img, path, filename = pcv.readimage("target_img.png")
cc_mask = pcv.transform.detect_color_card(rgb_img=rgb_img)

avg_chip_size = pcv.outputs.observations['prefix']['median_color_chip_size']['value']

```

**Image automatically detected and masked**

![Screenshot](img/documentation_images/correct_color_imgs/detect_color_card.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/transform/color_correction.py)
