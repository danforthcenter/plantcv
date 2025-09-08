## Color Chip Comparison

This function makes a plot comparing observed versus expected values from 1 or more color cards against a standard color card matrix via a "greenness rank". The greenness rank is useful in checking color card quality. The ninth (red) color chip is known to fade most quickly and the proportion of green light that it reflects can vary dramatically as the color card ages. The color of each bar is determined by the standard color matrix on the left side of the bar and by the observed color matrix on the right side of the bar. The order along the x axis is conserved from the order of `*args`.

**plantcv.visualize.color_chip_comparison**(*std_matrix, \*args*)

**returns** plot, a altair.vegalite.v5.api.VConcatChart object

- **Parameters:**
    - std_matrix       - A numpy.ndarray as returned from [`pcv.transform.std_color_matrix`](std_color_matrix.md).
	- \*args       - Any number of numpy.ndarrays as returned from [`pcv.transform.get_color_matrix`](get_color_matrix.md)

- **Context:**
    - The aim of this visualization is to help evaluate the condition of a color card or set of color cards.


- **Example use:**
    - Below

**Dataset images:**

![Screenshot](img/documentation_images/visualize_color_chip_comparison/input.png)

```python

from plantcv import plantcv as pcv

tgt_matrix = pcv.transform.std_color_matrix(pos=3)
_, cc1_matrix = pcv.transform.get_color_matrix(rgb_img=img, mask=cc_mask)
# ... masking more color cards for example
_, cc6_matrix = pcv.transform.get_color_matrix(rgb_img=img, mask=cc_mask6)

plot = pcv.visualize.color_chip_comparison(tgt_matrix, cc1_matrix,
                                           cc2_matrix, cc3_matrix,
                                           cc4_matrix, cc5_matrix,
                                           cc6_matrix)

```

**Color chip comparison visualizations:**

![Screenshot](img/documentation_images/visualize_color_chip_comparison/output.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/color_chip_comparison.py)
