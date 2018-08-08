## class Params

A global PlantCV parameters class.

*class* plantcv.**Params**

`Params` is a class that stores global PlantCV attributes. An instance of `Params` is created on import automatically
as `plantcv.params`. Updated PlantCV functions import the `plantcv.params` instance to access globally
configured attributes.

### Attributes

Attributes are accessed as plantcv.*attribute*.

**device**: A counter for image processing steps that is autoincremented by functions that use `params`. Default = 0.

**debug**: Debugging mode. Values are `None`, "print", or "plot". Default = `None`.

**debug_outdir**: The directory to output debug images to when `plantcv.debug` = "print".

### Example

Updated PlantCV functions use `params` implicitly, so overriding the `params` defaults will alter the behavior of
updated functions. In the meantime, it can also be used with older-style functions.

```python
from plantcv import plantcv as pcv

# Set debug to plot instead of None
pcv.params.debug = "plot"

# Use a pre-v3 function to open an image
# Note that pcv.params.debug is passed to the debug argument
img, imgpath, imgname = pcv.readimage(filename="test.png")

# Use a v3 function to create a region of interest
# Note that debug is not explicitly provided but is used implicitly by the function
roi_contour, roi_hierarchy = pcv.roi.rectangle(x=0, y=0, h=100, w=100, img=img)
```
