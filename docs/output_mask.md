## Output Mask and Original Image

Write image and mask with the same name to the path specified (creates two folders within the path if they do not exist).

**plantcv.output_mask**(*img,mask, filename,outdir=None, mask_only=False*)

**returns** imgpath, maskpath, analysis_images

**plantcv.output_mask**(*img,mask, filename,outdir=None, mask_only=True*)

**returns** maskpath, analysis_images

- **Parameters:**
    - img - original image, read in with plantcv function read_image
    - mask - binary mask image created in previous steps (single chanel)
    - filename - vis image file name (output of plantcv read_image function)
    - outdir - output directory
    - mask_only - If True, only outputs mask
    
- **Context:**
    - This function was written to more easily create training sets for machine learning (eg. Naive Bayes Classifier)

```python

from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

imgpath,maskpath=pcv.output_mask(img, mask, 'test.png', '/home/user/images', mask_only=True)

```
