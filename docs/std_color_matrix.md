## Macbeth ColorChecker Standard Color Matrix

Returns a color matrix with the standard *R*, *G*, *B* values compatible with the x-rite ColorCheker Classic,
ColorChecker Mini, and ColorChecker Passport targets.

X-Rite changed the pigment formulations of these targets in November 2014, so reference values are
provided for both post-November 2014 targets (default) and legacy (pre-November 2014) targets, which
can be useful when standardizing images collected with older color cards.

Sources:

- Post-November 2014 targets: sRGB conversion of the X-Rite reference CIELAB data for targets
manufactured November 2014 and later, converted and distributed by
[BabelColor](https://babelcolor.com/colorchecker-2.htm)
- Pre-November 2014 targets: average of measurements from 30 charts,
[https://en.wikipedia.org/wiki/ColorChecker](https://en.wikipedia.org/wiki/ColorChecker)

**plantcv.transform.std_color_matrix**(*pos=0, xrite_legacy=False*)

**returns** color_matrix

- **Parameters**
    - pos - reference value indicating orientation of the color card. The reference
    is based on the position of the white chip:

        - pos = 0: bottom-left corner  
        - pos = 1: bottom-right corner
        - pos = 2: top-right corner
        - pos = 3: top-left corner

    - xrite_legacy - return the reference matrix for legacy (pre-November 2014) X-Rite
    ColorChecker targets instead of the current (post-November 2014) targets (default = False)

- **Context**
    - A standard matrix can be used most readily while doing [affine](transform_affine_color_correction.md) color correction. 
    Where possible it's recommended to use [`pcv.transform.detect_color_card`](transform_detect_color_card.md) which orders the color card mask as if the white chip were in the top-left corner, or `pos = 3`. 

- **Returns**
    - color_matrix - a *n* x 4 matrix containing the standard red, green, and blue
    values for each color chip

- **Example use below:**

```python

from plantcv import plantcv as pcv

std_color_matrix = pcv.transform.std_color_matrix(pos=0)

# use fixed point notation for printing the matrix
np.set_printoptions(precision=2, suppress=True)

print(std_color_matrix)

        [[ 10.     0.45   0.31   0.25]
         [ 20.     0.78   0.56   0.5 ]
         [ 30.     0.36   0.47   0.61]
         [ 40.     0.36   0.42   0.25]
         [ 50.     0.51   0.5    0.69]
         [ 60.     0.37   0.74   0.67]
         [ 70.     0.88   0.49   0.19]
         [ 80.     0.27   0.35   0.65]
         [ 90.     0.78   0.31   0.37]
         [100.     0.36   0.22   0.41]
         [110.     0.61   0.73   0.23]
         [120.     0.89   0.63   0.15]
         [130.     0.15   0.24   0.57]
         [140.     0.24   0.58   0.27]
         [150.     0.7    0.21   0.22]
         [160.     0.93   0.78   0.05]
         [170.     0.75   0.31   0.58]
         [180.     0.     0.52   0.65]
         [190.     0.95   0.95   0.93]
         [200.     0.79   0.8    0.79]
         [210.     0.63   0.64   0.64]
         [220.     0.47   0.47   0.47]
         [230.     0.33   0.33   0.33]
         [240.     0.19   0.19   0.2 ]]

```
**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/transform/standard_matrices.py)
