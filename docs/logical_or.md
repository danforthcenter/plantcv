## Logical Operations - Or

Join two images using the bitwise OR operator. Images must be the same size. 
This is a wrapper for the Opencv Function [bitwise_or](http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#bitwise-or).  

<<<<<<< HEAD
**logical_or**(*img1, img2, device, debug=None*)
=======
**logical_or**(*img1, img2, device, debug=False*)
>>>>>>> master

**returns** device, 'or' image

- **Parameters:**
    - img1 - image object 1.
    - img2 - image object 2.
    - device - Counter for image processing steps
<<<<<<< HEAD
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
=======
    - debug- Default value is False, if True, intermediate image will be printed 
>>>>>>> master
- **Context:**
    - Used to combine to images. Very useful when combining image channels that have been thresholded seperately.
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In NIR Tutorial](nir_tutorial.md)
    
**Input binary image 1**

![Screenshot](img/documentation_images/logical_or/image1.jpg)

**Input binary image 2**

![Screenshot](img/documentation_images/logical_or/image2.jpg)

```python
import plantcv as pcv

# Combine two images that have had different thresholds applied to them.
# For logical 'or' operation object pixel in either image object will be included in 'or' image.
<<<<<<< HEAD
device, ab = pcv.logical_or(maskeda_thresh, maskedb_thresh, device, debug="print")
=======
device, ab = pcv.logical_or(maskeda_thresh, maskedb_thresh, device, args.debug)
>>>>>>> master
```

**Combined image**

![Screenshot](img/documentation_images/logical_or/joined.jpg)
