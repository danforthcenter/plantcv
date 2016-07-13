## Analyze FLU Signal

Extract Fv/Fm data of objects and produce pseudocolored images.

**fluor_fvfm**(*fdark, fmin, fmax, mask, device, filename, bins=1000, debug=False*)

**returns** device, FLU channel histogram headers, FLU channel histogram data, normalized color slice data

- **Parameters:**
    - fdark - image object, grayscale
    - fmin - image object  grayscale
    - fmax - image object, grayscale
    - mask - binary mask of selected contours
    - device - Counter for image processing steps
    - filename - False or image name. If defined print image
    - bins - number of grayscale bins (0-256 for 8-bit images and 0 to 65,536), if you would like to bin data, you would alter this number
    - debug - Default value is False, if True, intermediate image with boundary line will be printed
- **Context:**
    - Used to extract fv/fm per identified plant pixel.
    - Generates histogram of fv/fm data.
    - Generaes pseudocolored output image with fv/fm values per plant pixel.
- **Example use:**
    - [Use In Tutorial](flu_tutorial.md)

**Fdark image**

![Screenshot](img/documentation_images/fluor_fvfm/fdark.jpg)

**Fmin image**

![Screenshot](img/documentation_images/fluor_fvfm/fmin.jpg)

**Fmax image**

![Screenshot](img/documentation_images/fluor_fvfm/fmax.jpg)

```python
import plantcv as pcv

# Analyze Fv/Fm    
 device, fvfm_header, fvfm_data = pcv.fluor_fvfm(fdark, fmin, fmax, kept_mask, device, filename, 1000, debug=True)
```

**Histogram of Fv/Fm values**

![Screenshot](img/documentation_images/fluor_fvfm/fvfm_histogram.jpg)

**Pseudocolored output image based on Fv/Fm values**

![Screenshot](img/documentation_images/fluor_fvfm/fvfm_pseudocolored.jpg)
