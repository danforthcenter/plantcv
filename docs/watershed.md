## Watershed Segmentation

This function is based on code contributed by Suxing Liu, Arkansas State University.
For more information see https://github.com/lsx1980/Leaf_count. 
This function uses the watershed algorithm to detect boundry of objects. 
Needs a mask file which specifies area which is object is white, and background is black

**watershed_segmentation**(*device, img, mask, distance=10, filename=False, debug=None*)**

**returns** device, watershed_header,watershed_data, analysis_images

- **Parameters:**
    - device - Counter for image processing steps
    - img - img object
    - mask - binary image, single channel, object in white and background black
    - distance - min_distance of local maximum (lower values are more sensitive, and segments more objects)
    - filename - if user wants to output analysis images change filenames from false
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to segment image into parts

**Original image**

![Screenshot](img/documentation_images/watershed/543_auto_cropped.jpg)

```python
from plantcv import plantcv as pcv

# Segment image with watershed function
device, watershed_header, watershed_data,analysis_images=pcv.watershed_segmentation(device, crop_img,thresh,10,'./examples',debug='print')

print(watershed_header)
print(watershed_data)
```

**Watershed Segmentation**

![Screenshot](img/documentation_images/watershed/watershed.jpg)

('HEADER_WATERSHED', 'estimated_object_count')  
('WATERSHED_DATA', 10)