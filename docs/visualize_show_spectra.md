## Show Spectra for Selected Pixels (Developing)

`ShowSpectra` is a class that is capable of handling user's selecting and clicking behavior by showing spectra of user selected pixels and storing selected coordinates as well as spectra.

*class* **plantcv.visualize.ShowSpectra(spectral_data, figsize=(12,6))**
- To initialize the ShowSpectra class, the only required parameter is `spectral_data`, which is of type `__main__.Spectral_data`.
- Another optional parameter is the desired figure size `figsize`, by default `figsize=(12,6)`.

### Attributes
**spectral_data** (`__main__.Spectral_data`, required): input hyperspectral image.

**spectra** (`list`): spectra for all selected pixels.

**points** (`list`): list of coordinates of selected pixels.

```python

from plantcv import plantcv as pcv

show_spectra = pcv.visualize.ShowSpectra(spectral_data=array)

```

Check out this video for a sample usage:
<iframe src="https://player.vimeo.com/video/522535625" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/show_spectra.py)
