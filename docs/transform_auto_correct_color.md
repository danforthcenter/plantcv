# Automatically detect a color card and color correct in one step

Corrects the color of the input image based on the target color matrix using an affine transformation
in the RGB space after automatic detection of a color card within the image. A one-step wrapper of
[plantcv.transform.detect_color_card](transform_detect_color_card.md), [plantcv.transform.std_color_matrix](std_color_matrix.md),
[plantcv.transform.get_color_matrix](get_color_matrix.md), and [plantcv.transform.affine_color_correction](transform_affine_color_correction.md).

**plantcv.transform.auto_correct_color**(*rgb_img, label=None, \*\*kwargs*)

**returns** corrected_img

- **Parameters**
    - rgb_img          - Input RGB image data containing a color card.
    - label            - Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)
    - **kwargs         - Other keyword arguments passed to `cv2.adaptiveThreshold` and `cv2.circle`.
        - adaptive_method  - Adaptive threhold method. 0 (mean) or 1 (Gaussian) (default = 1).
        - block_size       - Size of a pixel neighborhood that is used to calculate a threshold value (default = 51). We suggest using 127 if using `adaptive_method=0`.
        - radius           - Radius of circle to make the color card labeled mask (default = 20).
        - min_size         - Minimum chip size for filtering objects after edge detection (default = 1000)
- **Returns**
    - corrected_img    - Color corrected image

- **Example Use**
    - Below

```python

from plantcv import plantcv as pcv

rgb_img, imgpath, imgname = pcv.readimage(filename="top_view_plant.png")

corrected_rgb = pcv.transform.auto_correct_color(rgb_img=old_card)

# Scale length & area Outputs collected downstream
# by updating size scaling parameters
pcv.params.unit = "mm"
# E.G. Given a square color card chips, (11mm x 11mm) in size
pcv.params.px_width = 11 /  pcv.outputs.metadata['median_color_chip_width']['value'][0]
pcv.params.px_height = 11 /  pcv.outputs.metadata['median_color_chip_height']['value'][0]
```

**Debug Image: automatically detected and masked the color card**

![Screenshot](img/documentation_images/correct_color_imgs/detect_color_card.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/transform/auto_correct_color.py)
