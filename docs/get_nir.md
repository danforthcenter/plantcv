## Get NIR Images

Gets NIR image that matches VIS image 

**get_nir**(*path, filename, device, debug*)

**returns** device, nir_path

- **Parameters:**
    - path - path to base image (vis image) to match
    - filename - filename of base image (vis image) to match
    - device - Counter for image processing steps
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - This is a function that is likely only useful for those with multiple camera types. We use this function to find the matching NIR image to a VIS image,
that is found in the same directory but which contains multiple images (regex). Would need to be modified for different file naming structure / image types / file structures.  

- **Example use:**
 - [Use in VIS/NIR Tutorial]()

**Original image**

![Screenshot](img/documentation_images/analyze_color/original_image.jpg)

```python
import plantcv as pcv

# Get NIR image

device, nir_path= pcv.get_nir(/home/images/rice_photos/, VIS_ , device, debug="print")

```

**Flipped Image**

![Screenshot](img/documentation_images/analyze_color/color_histogram.jpg)
