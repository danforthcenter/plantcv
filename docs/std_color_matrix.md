## Color Matrix

Returns a color matrix with the standard *R*, *G*, *B* values compatible with the x-rite ColorCheker Classic,
ColorChecker Mini, and ColorChecker Passport targets.

Source: [https://en.wikipedia.org/wiki/ColorChecker](https://en.wikipedia.org/wiki/ColorChecker)

**plantcv.transform.std_color_matrix**(*pos=0*)

**returns** color_matrix

- **Parameters**
    - pos - reference value indicating orientation of the color card. The reference
    is based on the position of the white chip:

        - pos = 0: bottom-left corner  
        - pos = 1: bottom-right corner
        - pos = 2: top-right corner
        - pos = 3: top-left corner

- **Returns**
    - color_matrix - a *n* x 4 matrix containing the standard red, green, and blue
    values for each color chip



- **Example use:**
    - Tutorial in progress

```python

from plantcv import plantcv as pcv

std_color_matrix = pcv.transform.std_color_matrix(pos=0)

# use fixed point notation for printing the matrix
np.set_printoptions(precision=2, suppress=True)

print(std_color_matrix)

        [[ 10.     0.45   0.32   0.27]
         [ 20.     0.76   0.59   0.51]
         [ 30.     0.38   0.48   0.62]
         [ 40.     0.34   0.42   0.26]
         [ 50.     0.52   0.5    0.69]
         [ 60.     0.4    0.74   0.67]
         [ 70.     0.84   0.49   0.17]
         [ 80.     0.31   0.36   0.65]
         [ 90.     0.76   0.35   0.39]
         [100.     0.37   0.24   0.42]
         [110.     0.62   0.74   0.25]
         [120.     0.88   0.64   0.18]
         [130.     0.22   0.24   0.59]
         [140.     0.27   0.58   0.29]
         [150.     0.69   0.21   0.24]
         [160.     0.91   0.78   0.12]
         [170.     0.73   0.34   0.58]
         [180.     0.03   0.52   0.63]
         [190.     0.95   0.95   0.95]
         [200.     0.78   0.78   0.78]
         [210.     0.63   0.63   0.63]
         [220.     0.48   0.48   0.47]
         [230.     0.33   0.33   0.33]
         [240.     0.2    0.2    0.2 ]]

```
**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/transform/color_correction.py)
