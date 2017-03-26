## Output Mask and Original Image

Write image and mask with the same name to the path specified (creates two folders within the path if they do not exist).

**output_mask**(*device,img,mask, filename,outdir=None, mask_only=False,debug=None*)

**returns** device, imgpath, maskpath

- **Parameters:**
    - device - pipeline step counter
    - img - original image, read in with plantcv function read_image
    - mask - binary mask image created in previous steps (single chanel)
    - filename - vis image file name (output of plantcv read_image function)
    - outdir - output directory
    - mask_only - If True, only outputs mask
    - debug - None, print, or plot. Print = save to file, Plot = print to screen.
- **Context:**
    - This function was written to more easily create training sets for machine learning (eg. Naive Bayes Classifier)

```python

import plantcv as pcv      

device, imgpath,maskpath=pcv.output_mask(device, img, mask, 'test.png', '/home/user/images', mask_only=False, debug='print')

```
