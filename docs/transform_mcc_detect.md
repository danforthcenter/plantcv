## Automatically Detect a Color Card with cv2.mcc tools

Automatically detects a Macbeth ColorChecker and creates a labeled mask.

**plantcv.transform.mcc_detect**(*rgb_img, color_chip_size=None, roi=None, delta_E=True, \*\*kwargs*)

**returns** color_matrix

- **Parameters**
    - rgb_img          - Input RGB image data containing a color card.
    - roi              - Optional rectangular ROI as returned by [`pcv.roi.rectangle`](roi_rectangle.md) within which to look for the color card. (default = None)
	- delta_E          - Boolean, should Delta E be calculated between the observed and expected color card values? This will add delta E values to `outputs.metadata`. See [`pcv.transform.deltaE`](transform_deltaE.md)
	- **kwargs         - Other keyword arguments passed to `cv2.mcc.CheckerDetector.process`.
	    - chartType    - int, code for type of chart (defaults to `cv2.mcc.MCC24`, which is 0)
		- nc           - int, number of charts to detect (defaults to 1)
		- useNet       - bool, should a neural network be used to detect the chart? (defaults to False)
		- params       - `cv2.mcc.DetectorParameters` object describing parameters for card detection (defaults to `cv2.mcc.DetectorParameters.create()`)

- **Returns**
    - color_matrix     - Detected color values as a matrix, the same format as output from [`pcv.transform.get_color_matrix`](get_color_matrix.md)).

- **Context**
	- In general we advocate for using [`pcv.transform.auto_correct_color`](transform_auto_correct_color.md) for simple color correction rather than `mcc_detect` or [`pcv.transform.detect_color_card`](transform_detect_color_card.md).
	- One setting where this function is a better option is if there are multiple color cards or color card like objects, since `cv2.mcc` detectors will find all matching regions then attempt to pick the best color card from avaiable options. This may be useful for some images where there are multiple color cards or other potentially confounding objects present.
	- If either this function or [`pcv.transform.detect_color_card`](transform_detect_color_card.md) are proving difficult to implement then we suggest at least trying the other function since they will work in slightly different ways to return the same output.
	- Debug images similar to those from [`pcv.transform.detect_color_card`](transform_detect_color_card.md) are generated

!!! note
    Unlike [`pcv.transform.detect_color_card`](transform_detect_color_card.md) this function does not support astrobotany color cards or size scaling based on color chips. `cv2.mcc` does not return the dimensions of color chips so this function does not serve the dual-purpose that other detection methods will allow for.


```python

from plantcv import plantcv as pcv
rgb_img, path, filename = pcv.readimage("target_img.png")

# Detecting a color card
cc_matrix = pcv.transform.mcc_detect(rgb_img=rgb_img)

# When using mcc_detect, as with detect_color_card, you will always set pos=3
tgt_matrix = pcv.transform.std_color_matrix(pos=3)
corrected_img = pcv.transform.affine_color_correction(rgb_img=rgb_img,
                                                      source_matrix=cc_matrix,
                                                      target_matrix=tgt_matrix)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/transform/mcc_detect.py)
