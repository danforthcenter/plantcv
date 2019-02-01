## Output Mask and Original Image

Write image and mask with the same name to the path specified (creates two folders within the path if they do not exist).

**plantcv.output_mask**(*img, mask, filename, outdir=None, mask_only=False*)

**returns** imgpath, maskpath, analysis_images

- **Parameters:**
    - img - RGB or grayscale image data, original image, read in with plantcv function read_image
    - mask - binary mask image created in previous steps (single chanel)
    - filename - vis image file name (output of plantcv read_image function)
    - outdir - output directory (default: None)
    - mask_only - If True, only outputs mask (default: False, also prints imgpath )
    
- **Context:**
    - This function was written to more easily create training sets for machine learning (eg. [Naive Bayes Classifier](naive_bayes_classifier.md)

```python

from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

maskpath, analysis_images = pcv.output_mask(img, mask, 'test.png', '/home/user/images', mask_only=True)

```
