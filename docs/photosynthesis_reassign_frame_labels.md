## Reassign Frame Labels

Relabel Fm and Fm' in PSII CropReporter datasets. The photosynthesis subpackage is dependent on a PSII_Data instance
file structure as created by `photosynthesis.read_cropreporter`.
Some systems (e.g. CropReporter) output a timeseries of fluorescence images that can be used to calculate a fluorescence
induction curve following a saturating light pulse. This function calculates the frame where maximum fluorescence is
observed and relabels the Fm or Fm' frame, if needed. This can only be done globally, not on a per-plant basis in a
multi-plant image. However, `pcv.analyze.yii` and `pcv.analyze.npq` can use this function to identify the optimal frame
for each plant in a multi-plant image.

**plantcv.photosynthesis.reassign_frame_labels**(*ps_da, mask*)

**returns** xarray DataArray with updated frame labels

- **Parameters:**
    - ps_da - photosynthesis xarray DataArray containing multiple post-saturating light pulse fluorescence images
    - mask - binary mask of plant
- **Context:**
    - Used to assign Fm or Fm' based on observed plant fluorescence.
- **Example use:**
    - [Use In PSII Tutorial](tutorials/psII_tutorial.md)

**Assign Fm**

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

psd = pcv.photosynthesis.reassign_frame_labels(ps_da=ps.ojip_dark, mask=mask)

```

**Assign Fm'**

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

psl = pcv.photosynthesis.reassign_frame_labels(ps_da=ps.ojip_light, mask=mask)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/photosynthesis/reassign_frame_labels.py)
