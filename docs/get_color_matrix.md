## Color Matrix

Computes the average *R*, *G*, *B* values for each region in the RGB image denoted by the gray-scale mask and saves them in a matrix of n x 4, where n = the number of color chips represented in the mask.

**plantcv.transform.get_color_matrix**(*rgb_img, mask*)

**returns** headers, color_matrix

- **Parameters**
    - rgb_img - RGB image with color chips visualized
    - mask    - a gray-scale img with unique values for each segmented space, representing unique, discrete color chips.

- **Returns**
    - color_matrix - a *n* x 4 matrix containing the average red value, average green value, and average blue value for each color chip.
    - headers      - a list of 4 headers corresponding to the 4 columns of color_matrix respectively

- **Example use:**
    - [Color Correction Tutorial](tutorials/transform_color_correction_tutorial.md)
    
```python

from plantcv import plantcv as pcv

rgb_img, imgpath, imgname = pcv.readimage(filename="target_img.png")
mask, maskpath, maskname = pcv.readimage(filename="mask_img.png")

headers, color_matrix = pcv.transform.get_color_matrix(rgb_img=rgb_img, mask=mask)

print(headers)
print(color_matrix)


    ['chip_number', 'r_avg', 'g_avg', 'b_avg']
    [[  10.       20.7332   33.672    92.7748]
     [  20.      203.508    79.774    25.77  ]
     [  30.       54.6916   34.0924   26.0352]
     [  40.      193.2972  203.198   199.4544]
     [  50.       40.2052   92.0536   37.222 ]
     [  60.       36.9256   52.4976  123.6224]
     [  70.      177.7984  103.3772   85.1672]
     [  80.      119.4276  128.4068  126.6948]
     [  90.      141.9036   34.0584   22.5056]
     [ 100.      160.9764   50.3872   47.6984]
     [ 110.       51.994    73.584   107.734 ]
     [ 120.       65.9104   69.5172   68.482 ]
     [ 130.      227.1652  183.1696   30.1332]
     [ 140.       35.9472   25.4984   47.3424]
     [ 150.       39.51     52.9624   26.3956]
     [ 160.       32.8148   34.8512   35.5284]
     [ 170.      146.522    55.7016   94.7452]
     [ 180.      114.6672  155.3968   42.5688]
     [ 190.       84.2172   88.8424  134.2356]
     [ 200.       34.5308   90.4592  132.9108]
     [ 210.      207.1596  128.736    28.7744]
     [ 220.       74.632   158.8224  144.3724]]
     
```
