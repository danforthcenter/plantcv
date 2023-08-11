## Automatically Find a Color Card

Automatically detects a color card's location and size. Useful in workflows where color card positioning isn't constant in all images.

**plantcv.transform.find_color_card**(*rgb_img, threshold_type='adaptgauss', threshvalue=125, blurry=False, background='dark', record_chip_size='median', label=None*)

**returns** df, start_coord, spacing

- **Parameters**
    - rgb_img          - Input RGB image data containing a color card.
    - threshold_type   - Optional, threshold method, either 'normal', 'otsu', or 'adaptgauss' (default theshold_type='adaptgauss')
    - threshvalue      - Optional, thresholding value (default threshvalue=125)
    - blurry           - Optional boolean, if True then image sharpening is applied (default blurry=False)
    - background       - Optional, type of image background, either 'dark' or 'light' (default background='dark')
    - record_chip_size - Optional, for choosing chip size measurement to be recorded, either "median" (default), "mean", or None
    - label - Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)
- **Returns**
    - df            - Dataframe of all color card chips found.
    - start_coord   - Two-element tuple of the first chip mask starting x and y coordinate. Useful in [create a color card mask](#create-a-labeled-color-card-mask) function.
    - spacing       - Two-element tuple of the horizontal and vertical spacing between chip masks. Useful in [create a color card mask](#create-a-labeled-color-card-mask) function.

**Important Note:** This function isn't entirely robust. There are a few important assumptions that must be met in order to automatically detect color cards:

- There is only one color card in the image.
- Color card should be 4x6 (like an X-Rite ColorChecker Passport Photo). Spacing calculations are based on 4x6 color cards. Although starting coordinates will be
    robust for most color cards, unless an entire row or entire column of chips is missing. Missing chips may also skew spacing and can also skew starting coordinates.
- Color card isn't tilted. The card can be vertical OR horizontal but if it is tilted there will errors in calculating spacing.

```python

from plantcv import plantcv as pcv
rgb_img, path, filename = pcv.readimage("target_img.png")
df, start, space = pcv.transform.find_color_card(rgb_img=rgb_img, label="prefix")

# Use these outputs to create a labeled color card mask
mask = pcv.transform.create_color_card_mask(rgb_img=img, radius=10, start_coord=start, spacing=space, ncols=6, nrows=4)
avg_chip_size = pcv.outputs.observations['prefix']['color_chip_size']['value']

```

**Image automatically detected and masked**

![Screenshot](img/documentation_images/correct_color_imgs/find_color_card.jpg)

#### "Troublesome" Example Images

**Image with multiple color cards**

![Screenshot](img/documentation_images/correct_color_imgs/multiple_color_card.jpg)

**Tilted color card**

![Screenshot](img/documentation_images/correct_color_imgs/tilted_color_card.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/transform/color_correction.py)
