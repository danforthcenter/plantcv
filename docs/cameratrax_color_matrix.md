## CameraTrax 24ColorCard Standard Color Matrix

Returns a color matrix with the standard *R*, *G*, *B* values compatible with the CameraTrax
24ColorCard color cards.

The CameraTrax 24ColorCard has the same chip layout as the X-Rite ColorChecker targets but uses its
own color formulation, so it requires its own reference matrix. The sRGB values are the
print-measured values printed on each card below the color chips.

Source: [https://www.cameratrax.com/color_balance_4x6.php](https://www.cameratrax.com/color_balance_4x6.php)

**plantcv.transform.cameratrax_color_matrix**(*pos=0*)

**returns** color_matrix

- **Parameters**
    - pos - reference value indicating orientation of the color card. The reference
    is based on the position of the white chip:

        - pos = 0: bottom-left corner  
        - pos = 1: bottom-right corner
        - pos = 2: top-right corner
        - pos = 3: top-left corner

- **Context**
    - A standard matrix can be used most readily while doing [affine](transform_affine_color_correction.md) color correction. 
    Where possible it's recommended to use [`pcv.transform.detect_color_card`](transform_detect_color_card.md) which orders the color card mask as if the white chip were in the top-left corner, or `pos = 3`. 

- **Returns**
    - color_matrix - a *n* x 4 matrix containing the standard red, green, and blue
    values for each color chip

- **Example use below:**

```python

from plantcv import plantcv as pcv

cameratrax_color_matrix = pcv.transform.cameratrax_color_matrix(pos=0)

# use fixed point notation for printing the matrix
np.set_printoptions(precision=2, suppress=True)

print(cameratrax_color_matrix)

        [[ 10.     0.45   0.35   0.3 ]
         [ 20.     0.76   0.59   0.53]
         [ 30.     0.35   0.49   0.63]
         [ 40.     0.36   0.44   0.28]
         [ 50.     0.5    0.51   0.7 ]
         [ 60.     0.36   0.76   0.69]
         [ 70.     0.88   0.5    0.24]
         [ 80.     0.27   0.37   0.7 ]
         [ 90.     0.77   0.33   0.4 ]
         [100.     0.36   0.25   0.43]
         [110.     0.63   0.75   0.3 ]
         [120.     0.91   0.64   0.24]
         [130.     0.19   0.27   0.6 ]
         [140.     0.28   0.61   0.32]
         [150.     0.69   0.25   0.25]
         [160.     0.95   0.8    0.25]
         [170.     0.75   0.35   0.61]
         [180.     0.     0.54   0.67]
         [190.     0.96   0.96   0.97]
         [200.     0.8    0.81   0.82]
         [210.     0.63   0.65   0.66]
         [220.     0.47   0.48   0.5 ]
         [230.     0.33   0.35   0.36]
         [240.     0.21   0.21   0.21]]

```
**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/transform/standard_matrices.py)
