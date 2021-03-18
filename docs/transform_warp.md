## Warp to Align

Find the transformation matrix that best describes the projective transform from reference image to target image, based on pairs of corresponding points on reference image and target image, respectively;
performs the projective transform on the target image to align it to the reference image. 

In general, any geometric transformation between 4 pairs of corresponding points is considered as projective transform. 
- Projective Transform: preservs lines but not necessarily parallelism. There are several special cases of projective transform. 
  - Euclidean Transform (righd transform): preserves the Euclidean distance between pairs of points. It can be described as a rotation about the origin followed by a translation.
    - Similarity Transform: preserves the shape of objects. It combines scaling, translation and rotation. 
  - Affine Transform: preserves lines (hence the alignment of objects), as well as parallelism between lines. It can be decomposed into a similarity transform and a shear transformation. 

Projective transformation describs most cases when images are taken from a slight different point of view, or even taken with different cameras. 

Read about different transformations at [Image Processing in OpenCV](https://docs.opencv.org/3.4/da/d6e/tutorial_py_geometric_transformations.html) and the [transform module of scikit-image](https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.estimate_transform). 

### warp_align 
**plantcv.transform.warp_align**(*img, refimg, pts, refpts, method="default"*)

**returns** image after warping and a 3x3 matrix of the perspective transformation.

- **Parameters:**
    - img - image to warp (np.ndarray)
    - refimg - image used as a reference for the warp (np.ndarray)
    - pts - coordinate points on `img`. At least 4 pairs should be given as a list of tuples
    - refpts - corresponding coordinate points on `refimg`. At least 4 pairs should be given as a list of tuples
    - method - robust estimation algorithm when calculating projective transformation. Available options are 'default', 'ransac', 'lmeds', 'rho' which correspond to the opencv methods and [vary based on how they handle outlier points](https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html#ga4abc2ece9fab9398f2e560d53c8c9780)
      - Any 4 pairs of corresponding points can define a projective transform. More than 4 pairs given means there are outliers. 
      - Robust estimation algorithms can be used to estimate the model based only on inliers to find a robust model.
      - Using 'default' means that a regular method using all the points without robustness i.e., the least squares method, is adopted.
- **Context:**
    - Warps an image without preserving parallel lines. 
- **Example use:**

1. A mask derived from an RGB image can be used to segment an NIR image which is difficult to segment otherwise.

**Input image**

A mask derived from a RGB image 2056x2454

![mask](img/documentation_images/transform_warp/mask.png)

An image from a SWIR camera is used as the reference image to define the transformation is 7000x5000

![reference image](img/documentation_images/transform_warp/refimg.png)

In this case we know the field of view of the two images is the same, so we can use the image corners to define the transformation. In other cases you might need to establish corresponding control points in each image.

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot" (Jupyter Notebooks or X11)
mrow, mcol = mask.shape
vrow, vcol, vdepth = grayimg.shape

mat, img_warped = pcv.transform.warp_align(img=mask,
                                refimg=grayimg,
                                pts = [(0,0),(mcol-1,0),(mcol-1,mrow-1),(0,mrow-1)],
                                refpts = [(0,0),(vcol-1,0),(vcol-1,vrow-1),(0,vrow-1)],
                                method='default')


```
2. Register the RGB image to the corresponding thermal image based on landmark points so that the mask derived from it can be used to pull out plant pixels from the corresponding thermal image.

**Input Image**
A thermal image (reference image) and its corresponding RGB image (target image).
![ref_target_img](img/documentation_images/transform_warp/ref_tar.png)
Overlay the thermal image on corresponding RGB image before image registration:
![overlay_orig](img/documentation_images/transform_warp/overlayed_orig.jpg)
Pairs of corresponding landmard points on both images:
![ref_target_img_pts](img/documentation_images/transform_warp/ref_tar_pts.png)
Check back later for information of getting landmark coordinates to registrate two images in a user-friendly interactive way!

```python

from plantcv import plantcv as pcv
pcv.params.marker_size=12
mat, img_warped = pcv.transform.warp_align(img=im_RGB,
                                refimg=im_therm,
                                pts=pts_RGB,
                                refpts=pts_therm)
```

Warped RGB image:
![warped_RGB](img/documentation_images/transform_warp/RGB_aligned.jpg)

Overlay the thermal image on warped RGB image:
![overlay_warped](img/documentation_images/transform_warp/overlayed_aligned.jpg)

Reference image with markers:
![ref_marked](img/documentation_images/transform_warp/ref_pts.png)

Target image with markers:
![ref_marked](img/documentation_images/transform_warp/tar_pts.png)

A pair of correaponding inlier points are represented with the same color with the "+" marker; the outliers are represented using upper triangles. 

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/transform/warp.py)
