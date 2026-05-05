## Astrobotany Calibration Sticker Color Matrix

Returns a color matrix with the standard *R*, *G*, *B* values compatible with Astrobotany Calibration Stickers.

Source: [https://astrobotany.com/product/airi-bio-imaging-spectrum-5cm/](https://astrobotany.com/product/airi-bio-imaging-spectrum-5cm/)

**plantcv.transform.astro_color_matrix**()

**returns** color_matrix

- **Context**
    - A standard matrix can be used most readily while doing [affine](transform_affine_color_correction.md) color correction. 

- **Returns**
    - color_matrix - a *n* x 4 matrix containing the standard red, green, and blue
    values for each color chip

- **Example use below:**

```python

from plantcv import plantcv as pcv

astro_color_matrix = pcv.transform.astro_color_matrix()

# use fixed point notation for printing the matrix
np.set_printoptions(precision=2, suppress=True)

print(astro_color_matrix)

        [[ 10.,    0.18,   0.23,   0.5 ],
         [ 20.,    0.34,   0.62,   0.25],
         [ 30.,    0.71,   0.25,   0.21],
         [ 40.,    0.89,   0.81,   0.2 ],
         [ 50.,    0.21,   0.22,   0.22],
         [ 60.,    0.91,   0.95,   0.93],
         [ 70.,    0.82,   0.86,   0.86],
         [ 80.,    0.72,   0.75,   0.73],
         [ 90.,    0.64,   0.67,   0.64],
         [100.,    0.57,   0.58,   0.56],
         [110.,    0.48,   0.49,   0.48],
         [120.,    0.39,   0.4 ,   0.39],
         [130.,    0.33,   0.32,   0.32],
         [140.,    0.27,   0.28,   0.27],
         [150.,    0.22,   0.23,   0.23]]

```
**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/transform/color_correction.py)
