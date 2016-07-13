## Erode

Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if 
conditions set in kernel are true, otherwise removes pixel.

**erode**(*img, kernel, i, device, debug=False*)

**returns** device, image after erosion

- **Parameters:**
    - img1 - Input image
    - kernel - Filtering window, you'll need to make your own using as such:  kernal = np.zeros((x,y), dtype=np.uint8), then fill the kernal with appropriate values
    - i - Iterations, i.e. the number of consecutive filtering passes
    - device - Counter for image processing steps
    - debug- Default value is False, if True, filled intermediate image will be printed
- **Context:**
    - Used to perform morphological erosion filtering. Helps remove isolated noise pixels or remove boundary of objects.

**Input grayscale image**

![Screenshot](img/documentation_images/erode/grayscale_image.jpg)

```python
import plantcv as pcv

# Perform erosion filtering
# Results in removal of isolated pixels or boundary of object removal
device, er_img = pcv.erosion(img, kernel, 1 device, debug=True)
```

**Image after erosion**

![Screenshot](img/documentation_images/erode/erosion.jpg)
