## Analyze Shape Characteristics of Object

Shape analysis outputs numeric properties for an input object (contour or grouped contours), works best on grouped contours.
 
<<<<<<< HEAD
**analyze_object**(*img, imgname, obj, mask, device, debug=None, filename=False*)
=======
**analyze_object**(*img, imgname, obj, mask, device, debug=False, filename=False*)
>>>>>>> master

**returns** device, shape data headers, shape data, image with shape data

- **Parameters:**
    - img - image object (most likely the original), color(RGB)
    - imgname - name of image
    - obj - single or grouped contour object
    - device - Counter for image processing steps
<<<<<<< HEAD
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None 
=======
    - debug - Default value is False, if True, intermediate image with ROI will be printed 
>>>>>>> master
    - filename - False or image name. If defined print image
- **Context:**
    - Used to output shape characteristics of an image, including height, object area, convex hull, convex hull area, perimeter, extent x, extent y, longest axis, centroid x coordinate, centroid y coordinate, in bounds QC (if object touches edge of image, image is flagged). 
- **Example use:**
    - [Use In VIS Tutorial](../vis_tutorial.html)
    - [Use In NIR Tutorial](nir_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md) 
    
**Original image**

![Screenshot](img/documentation_images/analyze_shape/original_image.jpg)

```python
import plantcv as pcv

# Characterize object shapes
    
<<<<<<< HEAD
device, shape_header, shape_data, shape_img = pcv.analyze_object(img, imgname, objects, mask, device, debug="print", /home/malia/setaria_shape_img.png)
=======
device, shape_header,shape_data,shape_img = pcv.analyze_object(img, imgname, objects, mask, device, debug=True, /home/malia/setaria_shape_img.png)
>>>>>>> master
```

**Image with identified objects**

![Screenshot](img/documentation_images/analyze_shape/objects_on_image.jpg)

**Image with shape characteristics**

![Screenshot](img/documentation_images/analyze_shape/shapes_on_image.jpg)
