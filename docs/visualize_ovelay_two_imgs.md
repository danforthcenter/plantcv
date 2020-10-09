## Overlay Two Images

This function overlays one input image on top of the other one, with a desired alpha value indicating the opacity of the 1st image. It is able to handle both RGB  and gray scale images.

**plantcv.visualize.overlay_two_imgs**(*img1, img2, alpha=0.5, size_img=None*)

**returns** blended image (that can be saved with `pcv.print_image`)

- **Parameters:**
    - img1        - 1st input image (ndarray).
    - img2        - 2nd input image (ndarray).
    - alpha       - Opacity of the 1st image (a value in the range of (0,1), default `alpha=0.5`).
    - size_img    - Desired output image size (optional, default: None). Both input images would be resized to a same size. If the desired size is not given, the larger width and height of the two input images is used as the common size.

- **Context:**
    - Used to overlay two images. 
- **Example use:**
    - Below

**First image: RGB image**

![Screenshot](img/documentation_images/visualize_overlay_two_imgs/overlay_rgb.png)

**Second image: a gray scale mask**

![Screenshot](img/documentation_images/visualize_overlay_two_imgs/overlay_bin.png)


```python

from plantcv import plantcv as pcv

pcv.params.debug='plot'

blended_im = pcv.overlay_two_imgs(img1=img1, img2=img2, alpha=0.5, size_img=None)

```

**Blended Image**

![Screenshot](img/documentation_images/visualize_overlay_two_imgs/overlay_result.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/overlay_two_imgs.py)
