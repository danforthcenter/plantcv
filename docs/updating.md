## Updating PlantCV

### Table of Contents for Contibution
1. [Updating with PyPi](#pypi)
2. [Updating with Conda](#conda)
3. [Updating from source](#source)
4. [Updating to v4](#v4)
    * [An example](#ex)
5. [Changelog](#changelog)

### PyPI <a name="pypi"></a>

To update PlantCV, in a terminal type:

```bash
pip install --upgrade plantcv

```

### Conda <a name="conda"></a>

To update PlantCV, in a terminal type:

```bash
conda update -n plantcv -c conda-forge plantcv

```

If conda does not update your PlantCV installation, you can try installing a specific version. For example if you are on v3.6.1 and you would like to install v4.0 you can use:

```bash
conda install -n plantcv -c conda-forge plantcv=4.0

``` 

You can find the version you have installed with:

```bash
conda list plantcv

```

### Updating from the source code  <a name="source"></a>

The general procedure for updating PlantCV if you are using the `main` branch
cloned from the `danforthcenter/plantcv` repository is to update your local
repository and reinstall the package.

With GitHub Desktop you can [synchronize](https://docs.github.com/en/free-pro-team@latest/desktop/contributing-and-collaborating-using-github-desktop/syncing-your-branch)
to pull updates from GitHub. Or on the command line update using `git pull` while
on top of your cloned `plantcv` directory.

If you are not sure that you have cloned the `danforthcenter/plantcv` repository
and are on the `main` branch, here is how you can tell:

If you installed PlantCV using the "editable" mode `pip install -e .` then your installation should be updated
automatically. Alternatively, you can run `pip install -e .` to reinstall the package from the cloned repository.

### Updating to v4 <a name="v4"></a>

In addition to new features a major goal of PlantCV v4 is to make PlantCV functions
a bit easier to use and combine into a custom workflow for batch processing.
We hope you agree the changes detailed below succeed
in that goal, but if you have any questions or concerns please feel free to open
an issue on GitHub or contact us directly.

Another feature we have rolled out for PlantCV v4 is an update to the existing
package API. The goal is to make each PlantCV function easier to use by reducing
the number of inputs and outputs that need to be configured (without losing
functionality). Part of these updates include making input parameters consistently
named and clearly defined where input types matter (e.g. instead of just `img` it could be `rgb_img`,
`gray_img`, or `bin_img` for RGB, grayscale, or binary image, respectively).

In PlantCV v3.0dev2 onwards, all functions were redesigned to utilize a global
parameters class to inherit values for standard inputs like `debug` and `device`
so that these values will not need to be explicitly input or output to/from each
function. An instance of the class [`Params`](params.md) as `params` is created automatically
when PlantCV is imported and it can be imported to set global defaults. For example,
to change debug from `None` to 'plot' or 'print' you can now just add one line to
the top of your script or notebook to change the behavior of all subsequent function
calls:

```python
from plantcv import plantcv as pcv
pcv.params.debug = "plot"
```

For more information, see the [Params](params.md) documentation. 

### Workflow Updating (an example) <a name="ex"></a>

Below is a simple example of a typical PlantCV v3 workflow of a single plant. 

```python
# Read in image data 
img, path, filename = pcv.readimage(filename="rgb_img.png")

# Covert to grayscale colorspace 
a = pcv.rgb2gray_lab(rgb_img=img, channel='a')

# Threshold/segment plant from background 
bin_mask = pcv.threshold.binary(gray_img=a, threshold=100, max_value=255, object_type="light")

# Define objects & hierarchies (needed for OpenCV)
id_objects, obj_hierarchy = pcv.find_objects(img=img, mask=bin_mask)

# Define ROI 
roi_contour, roi_hierarchy = pcv.roi.rectangle(img=img, x=100, y=100, h=100, w=100)

# Filter binary image to make a clean mask based on ROI
kept_objs, kept_h, kept_mask, obj_area = pcv.roi_objects(img=img,roi_contour=roi_contour,
roi_hierarchy=roi_h,
object_contour=id_objects,
obj_hierarchy=obj_hierarchy,
roi_type="partial")

# Perform object composition (needed for OpenCV)
plant_obj, mask = pcv.object_composition(img=img,
contours=kept_objs, hierarchy=kept_h)        
        
# Finally extract shape traits from plant 
shape_img = pcv.analyze_object(img=img, obj=plant_obj, mask=mask)

# Save out data to file
pcv.outputs.save_results(filename="results.txt", outformat="json")
# In even older versions of PlantCV (pre v3.12) it would have been 
# pcv.print_results(filename="results.txt")
```

And below is how the same workflow steps look for a single plant workflow
in PlantCV v4.0 and future releases. 

```python
# Read in image data (no change)
img, path, filename = pcv.readimage(filename="rgb_img.png")

# Covert to grayscale colorspace (no change)
a = pcv.rgb2gray_lab(rgb_img=img, channel='a')

# Threshold/segment plant from background (removed max_value)
bin_mask = pcv.threshold.binary(gray_img=a, threshold=100, object_type="light")

# Define ROI (reduced outputs)
roi = pcv.roi.rectangle(img=img, x=100, y=100, h=100, w=100)

# Filter binary image to make a clean mask based on ROI 
# (no longer needs `pcv.find_objects` or `pcv.object_composition`)
mask = pcv.roi.filter(mask=bin_mask, roi=roi, roi_type="partial")

# Extract shape traits from plant
shape_img = pcv.analyze.size(img=img,labeled_mask=mask, n_labels=1)

# Save out data to file
pcv.outputs.save_results(filename="results.txt", outformat="json")
```

In the case of a single plant workflow, users will likely create their `labeled_mask`
with the [`pcv.roi.filter`](roi_filter.md) function but multi-object workflows
will want to use the [`pcv.create_labels`](create_labels.md) function. We've updated PlantCV
analysis functions to work iteratively over multiple objects without needed to write a Python 
`for` loop. See the [multi-plant tutorial](https://plantcv.org/tutorials/arabidopsis-tray) to see an 
example workflow for datasets where there are more than one distinct object of interest
per image (e.g. top down tray of plants). 

Also note that the method for parallelizing PlantCV has changed, please see the
new [parallel processing documentation](pipeline_parallel.md) for more details.

### Changelog <a name="changelog"></a>

Below is an overview of all updates that are required to convert a pre-v3.0dev2
function call to the most updated function call.
See the individual function help
pages for more details on the input and output variable types.

#### plantcv.acute

* pre v3.0dev2: device, homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist = **plantcv.acute**(*obj, win, thresh, mask, device, debug=None*)
* post v3.0dev2: homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist = **plantcv.acute**(*obj, win, thresh, mask*)
* post v3.2: homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist = **plantcv.acute**(*obj, mask, win, thresh*)
* post v4.0: DEPRECATED see plantcv.homology.acute

#### plantcv.acute_vertex

* pre v3.0dev2: device, acute = **plantcv.acute_vertex**(*obj, win, thresh, sep, img, device, debug=None*)
* post v3.0dev2: acute = **plantcv.acute_vertex**(*obj, win, thresh, sep, img*)
* post v3.2: acute, analysis_image = **plantcv.acute_vertex**(*img, obj, win, thresh, sep*)
* post v3.11: acute, analysis_image = **plantcv.acute_vertex**(**img, obj, win, thresh, sep, label="default"*)
* post v4.0: DEPRECATED see plantcv.homology.acute

#### plantcv.adaptive_threshold

* pre v3.0dev2: device, bin_img = **plantcv.adaptive_threshold**(*img, maxValue, thres_type, object_type, device, debug=None*)
* post v3.0dev2: Deprecated, see:
    * bin_img = **plantcv.threshold.gaussian**(*gray_img, max_value, object_type="light"*)
    * bin_img = **plantcv.threshold.mean**(*gray_img, max_value, object_type="light"*)

#### plantcv.analyze_bound

* pre v3.0dev2: device, bound_header, bound_data, analysis_images = **plantcv.analyze_bound**(*img, imgname, obj, mask, line_position, device, debug=None, filename=False*)
* post v3.0dev2: Deprecated, see: plantcv.analyze_bound_horizontal

#### plantcv.analyze_bound_horizontal

* pre v3.0dev2: device, bound_header, bound_data, analysis_images = **plantcv.analyze_bound_horizontal**(*img, obj, mask, line_position, device, debug=None, filename=False*)
* post v3.0dev2: bound_header, bound_data, analysis_images = **plantcv.analyze_bound_horizontal**(*img, obj, mask, line_position, filename=False*)
* post v3.0: bound_header, bound_data, analysis_images = **plantcv.analyze_bound_horizontal**(*img, obj, mask, line_position*)
* post v3.3: analysis_image = **plantcv.analyze_bound_horizontal**(*img, obj, mask, line_position*)
* post v3.11: analysis_image = **plantcv.analyze_bound_horizontal**(*img, obj, mask, line_position, label="default"*)
* post v4.0: DEPRECATED see plantcv.analyze.bound_horizontal


#### plantcv.analyze_bound_vertical

* pre v3.0dev2: device, bound_header, bound_data, analysis_images = **plantcv.analyze_bound_vertical**(*img, obj, mask, line_position, device, debug=None, filename=False*)
* post v3.0dev2: bound_header, bound_data, analysis_images = **plantcv.analyze_bound_vertical**(*img, obj, mask, line_position, filename=False*)
* post v3.0.5: bound_header, bound_data, analysis_images = **plantcv.analyze_bound_vertical**(*img, obj, mask, line_position*)
* post v3.3: analysis_image = **plantcv.analyze_bound_vertical**(*img, obj, mask, line_position*)
* post v3.11: analysis_image = **plantcv.analyze_bound_vertical**(*img, obj, mask, line_position, label="default"*)
* post v4.0: DEPRECATED see plantcv.analyze.bound_vertical

#### plantcv.analyze_color

* pre v3.0dev2: device, hist_header, hist_data, analysis_images = **plantcv.analyze_color**(*img, imgname, mask, bins, device, debug=None, hist_plot_type=None, pseudo_channel='v', pseudo_bkg='img', resolution=300, filename=False*)
* post v3.0dev2: hist_header, hist_data, analysis_images = **plantcv.analyze_color**(*rgb_img, mask, bins, hist_plot_type=None, pseudo_channel='v', pseudo_bkg='img', filename=False*)
* post v3.0: hist_header, hist_data, analysis_images = **plantcv.analyze_color**(*rgb_img, mask, bins, hist_plot_type=None*)
* post v3.3: analysis_image = **plantcv.analyze_color**(*rgb_img, mask, hist_plot_type=None*)
* post v3.11: analysis_image = **plantcv.analyze_color**(*rgb_img, mask, hist_plot_type=None, label="default"*)
* post v3.12: analysis_image = **plantcv.analyze_color**(*rgb_img, mask, hist_plot_type=None, colorspaces="all", label="default"*)
* post v4.0: DEPRECATED see plantcv.analyze.color

#### plantcv.analyze_nir_intensity

* pre v3.0dev2: device, hist_header, hist_data, analysis_img = **plantcv.analyze_NIR_intensity**(*img, rgbimg, mask, bins, device, histplot=False, debug=None, filename=False*)
* post v3.0dev2: hist_header, hist_data, analysis_img = **plantcv.analyze_nir_intensity**(*gray_img, mask, bins, histplot=False, filename=False*)
* post v3.0: hist_header, hist_data, nir_hist = **plantcv.analyze_nir_intensity**(*gray_img, mask, bins, histplot=False*)
* post v3.3: nir_hist = **plantcv.analyze_nir_intensity**(*gray_img, mask, bins, histplot=False*)
* post v3.11: nir_hist = **plantcv.analyze_nir_intensity**(*gray_img, mask, bins, histplot=False, label="default"*)
* post v4.0: DEPRECATED: see plantcv.analyze.grayscale


#### plantcv.analyze_object

* pre v3.0dev2: device, shape_header, shape_data, analysis_images = **plantcv.analyze_object**(*img, imgname, obj, mask, device, debug=None, filename=False*)
* post v3.0dev2: shape_header, shape_data, analysis_images = **plantcv.analyze_object**(*img, obj, mask, filename=False*)
* post v3.0: shape_header, shape_data, analysis_images = **plantcv.analyze_object**(*img, obj, mask*)
* post v3.3: analysis_image = **plantcv.analyze_object**(*img, obj, mask*)
* post v3.11: analysis_image = **plantcv.analyze_object**(*img, obj, mask, label="default"*)
* post v4.0: DEPRECATED, see plantcv.analyze.size


#### plantcv.analyze_thermal_values

* pre v3.5: NA
* post v3.5: thermal_histogram = **plantcv.analyze_thermal_values**(*thermal_array, mask, histplot=False*)
* post v3.11: thermal_histogram = **plantcv.analyze_thermal_values**(*thermal_array, mask, histplot=False, label="default"*)
* post v4.0: DEPRECATED, see plantcv.analyze.thermal

#### plantcv.analyze.bound_horizontal

* pre v4.0: (see plantcv.analyze_bound_horizontal)
* post v4.0: analysis_image = **plantcv.analyze.bound_horizontal**(*img, labeled_mask, line_position, n_labels=1, label=None*)


#### plantcv.analyze.bound_vertical

* pre v4.0: (see plantcv.analyze_bound_vertical)
* post v4.0: analysis_image = **plantcv.analyze.bound_vertical**(*img, labeled_mask, line_position, n_labels=1, label=None*)


#### plantcv.analyze.color

* pre v4.0: (see plantcv.analyze_color)
* post v4.0: histogram = **plantcv.analyze.color**(*rgb_img, labeled_mask, n_labels=1, colorspaces="hsv", label=None*)

#### plantcv.analyze.distribution

* pre v4.2.1: NA
* post v4.2.1: dist_chart = **plantcv.analyze.distribution**(*labeled_mask, n_labels=1, direction="down", bin_size=100, hist_range="absolute", label=None*)

#### plantcv.analyze.grayscale

* pre v4.0: (see plantcv.analyze_nir_intensity)
* post v4.0: histogram = **plantcv.analyze.grayscale**(*gray_img, labeled_mask, n_labels=1, bins=100, label=None*)

#### plantcv.analyze.npq

* pre v4.0: NA
* post v4.0: npq, npq_hist = **plantcv.analyze.npq**(*ps_da_light, ps_da_dark, labeled_mask, n_labels=1, auto_fm=False, min_bin=0, max_bin="auto", measurement_labels=None, label=None*)

#### plantcv.analyze.size

* pre v4.0: (see plantcv.analyze_object)
* post v4.0: analysis_image = **plantcv.analyze.size**(*img, labeled_mask, n_labels=1, label=None*)


#### plantcv.analyze.spectral_index

* pre v4.0: (see plantcv.hyperspectral.analyze_index)
* post v4.0: analysis_image = **plantcv.analyze.spectral_index**(*index_img, labeled_mask, n_labels=1, bins=100, min_bin=0, max_bin=1, label=None*)


#### plantcv.analyze.spectral_reflectance

* pre v4.0: (see plantcv.hyperspectral.analyze_spectral)
* post v4.0: analysis_image = **plantcv.analyze.spectral_reflectance**(*hsi, labeled_mask, n_labels=1, label=None*)


#### plantcv.analyze.thermal

* pre v4.0: (see plantcv.analyze_thermal_values)
* post v4.0: analysis_image = **plantcv.analyze.thermal**(*thermal_img, labeled_mask, n_labels=1, bins=100, label=None*)

#### plantcv.analyze.yii

* pre v4.0: NA
* post v4.0: yii, yii_hist = **plantcv.analyze.yii**(*ps_da, labeled_mask, n_labels=1, auto_fm=False, measurement_labels=None, label=None*)

#### plantcv.apply_mask

* pre v3.0dev2: device, masked_img = **plantcv.apply_mask**(*img, mask, mask_color, device, debug=None*)
* post v3.0dev2: masked_img = **plantcv.apply_mask**(*rgb_img, mask, mask_color*)
* post v3.7: masked_img = **plantcv.apply_mask**(*img, mask, mask_color*)

#### plantcv.auto_crop

* pre v3.0dev2: device, cropped = **plantcv.auto_crop**(*device, img, objects, padding_x=0, padding_y=0, color='black', debug=None*)
* post v3.0dev2: cropped = **plantcv.auto_crop**(*img, objects, padding_x=0, padding_y=0, color='black'*)
* post v3.2: cropped = **plantcv.auto_crop**(*img, obj, padding_x=0, padding_y=0, color='black'*)
* post v4.0: cropped = **plantcv.auto_crop**(*img, mask, padding_x=0, padding_y=0, color='black'*)


#### plantcv.background_subtraction

* pre v3.0dev2: device, fgmask = **plantcv.background_subtraction**(*background_image, foreground_image, device, debug=None*)
* post v3.0dev2: fgmask = **plantcv.background_subtraction**(*background_image, foreground_image*)

#### plantcv.binary_threshold

* pre v3.0dev2: device, bin_img = **plantcv.binary_threshold**(*img, threshold, maxValue, object_type, device, debug=None*)
* post v3.0dev2: Deprecated, see:
    * bin_img = **plantcv.threshold.binary**(*gray_img, threshold, max_value, object_type="light"*)

#### plantcv.canny_edge_detect

* pre v3.2: NA
* post v3.2: bin_img = **plantcv.canny_edge_detect**(*img, mask=None, sigma=1.0, low_thresh=None, high_thresh=None, thickness=1, mask_color=None, use_quantiles=False*)

#### plantcv.closing

* pre v3.3: NA
* post v3.3: filtered_img = **plantcv.closing**(*gray_img, kernel=None*)


#### plantcv.cluster_contour_splitimg

* pre v3.0dev2: device, output_path = **plantcv.cluster_contour_splitimg**(*device, img, grouped_contour_indexes, contours, hierarchy, outdir=None, file=None, filenames=None, debug=None*)
* post v3.0dev2: output_path = **plantcv.cluster_contour_splitimg**(*rgb_img, grouped_contour_indexes, contours, hierarchy, outdir=None, file=None, filenames=None*)
* post v3.3: output_path, output_imgs, output_masks = **plantcv.cluster_contour_splitimg**(*rgb_img, grouped_contour_indexes, contours, hierarchy, outdir=None, file=None, filenames=None*)
* post v3.12 output_path, output_imgs, output_masks = **plantcv.cluster_contour_splitimg**(*img, grouped_contour_indexes, contours, hierarchy, outdir=None, file=None, filenames=None*)
* post v4.0: DEPRECATED 


#### plantcv.cluster_contours

* pre v3.0dev2: device, grouped_contour_indexes, contours, roi_obj_hierarchy = **plantcv.cluster_contours**(*device, img, roi_objects,roi_obj_hierarchy, nrow=1, ncol=1, debug=None*)
* post v3.0dev2: grouped_contour_indexes, contours, roi_obj_hierarchy = **plantcv.cluster_contours**(*img, roi_objects, roi_obj_hierarchy, nrow=1, ncol=1*)
* post v3.2: grouped_contour_indexes, contours, roi_obj_hierarchy = **plantcv.cluster_contours**(*img, roi_objects, roi_object_hierarchy, nrow=1, ncol=1, show_grid=False*)
* post v3.12: grouped_contour_indexes, contours, roi_obj_hierarchy = **plantcv.cluster_contours**(*img, roi_objects, roi_object_hierarchy, nrow=1, ncol=1, show_grid=False, bounding=True*)
* post v4.0: DEPRECATED see plantcv.roi.auto_grid


#### plantcv.color_palette

* pre v3.0: NA
* post v3.0: colors = **plantcv.color_palette**(*num*)
* post v3.9: colors = **plantcv.color_palette**(*num, saved=False*)

#### plantcv.create_labels

* pre v4.0: NA
* post v4.0: labeled_masks, num_labels = **plantcv.create_labels**(*mask, rois=None, roi_type="partial"*)


#### plantcv.crop_position_mask

* pre v3.0dev2: device, newmask = **plantcv.crop_position_mask**(*img, mask, device, x, y, v_pos="top", h_pos="right", debug=None*)
* post v3.0dev2: newmask = **plantcv.crop_position_mask**(*img, mask, x, y, v_pos="top", h_pos="right"*)

#### plantcv.define_roi

* pre v3.0dev2: device, contour, hierarchy = **plantcv.define_roi**(*img, shape, device, roi=None, roi_input='default', debug=None, adjust=False, x_adj=0, y_adj=0, w_adj=0, h_adj=0*)
* post v3.0dev2: Deprecated, see:
    * roi_contour, roi_hierarchy = **plantcv.roi.circle**(*img, x, y, r*)
    * roi_contour, roi_hierarchy = **plantcv.roi.ellipse**(*img, x, y, r1, r2, angle*)
    * roi_contour, roi_hierarchy = **plantcv.roi.from_binary_image**(*img, bin_img*)
    * roi_contour, roi_hierarchy = **plantcv.roi.rectangle**(*img, x, y, h, w*)

#### plantcv.dilate

* pre v3.0dev2: device, dil_img = **plantcv.dilate**(*img, kernel, i, device, debug=None*)
* post v3.0dev2: dil_img = **plantcv.dilate**(*gray_img, kernel, i*)
* post v3.2: dil_img = **plantcv.dilate**(*gray_img, ksize, i*)

#### plantcv.distance_transform

* pre v3.0dev2: device, norm_image = **plantcv.distance_transform**(*img, distanceType, maskSize, device, debug=None*)
* post v3.0dev2: norm_image = **plantcv.distance_transform**(*bin_img, distance_type, mask_size*)

#### plantcv.erode

* pre v3.0dev2: device, er_img = **plantcv.erode**(*img, kernel, i, device, debug=None*)
* post v3.0dev2: er_img = **plantcv.erode**(*gray_img, kernel, i*)
* post v3.2: er_img = **plantcv.erode**(*gray_img, ksize, i*)

#### plantcv.fill

* pre v3.0dev2: device, filtered_img = **plantcv.fill**(*img, mask, size, device, debug=None*)
* post v3.0dev2: filtered_img = **plantcv.fill**(*bin_img, size*)

#### plantcv.fill_holes

* pre v3.3: NA
* post v3.3: filtered_img = **plantcv.fill**(*bin_img*)

#### plantcv.filters.eccentricity 

* pre v4.3:  NA 
* post v4.3: filtered_mask = **plantcv.filters.eccentricity**(*bin_img, ecc_thresh=0*)

#### plantcv.filters.obj_props

* pre v4.4:  NA 
* post v4.4: filtered_mask = **plantcv.filters.obj_props**(*bin_img, cut_side = "upper", thresh=0, regprop="area"*)

#### plantcv.find_objects

* pre v3.0dev2: device, objects, hierarchy = **plantcv.find_objects**(*img, mask, device, debug=None*)
* post v3.0dev2: objects, hierarchy = **plantcv.find_objects**(*img, mask*)
* post v4.0: Deprecated


#### plantcv.flip

* pre v3.0dev2: device, vh_img = **plantcv.flip**(*img, direction, device, debug=None*)
* post v3.0dev2: vh_img = **plantcv.flip**(*img, direction*)

#### plantcv.flood_fill

* pre v4.1: NA
* post v4.1: filled_image = **plantcv.flood_fill**(*bin_img, points, value=0*)

#### plantcv.fluor_fvfm

* pre v3.0dev2: device, hist_header, hist_data = **plantcv.fluor_fvfm**(*fdark, fmin, fmax, mask, device, filename, bins=1000, debug=None*)
* post v3.0dev2: hist_header, hist_data, hist_images = **plantcv.fluor_fvfm**(*fdark, fmin, fmax, mask, filename, bins=256*)
* post v3.0: hist_header, hist_data, analysis_images = **plantcv.fluor_fvfm**(*fdark, fmin, fmax, mask, bins=256*)
* post v3.3: analysis_images = **plantcv.fluor_fvfm**(*fdark, fmin, fmax, mask, bins=256*)
* post v3.9: DEPRECATED see plantcv.photosynthesis

#### plantcv.gaussian_blur

* pre v3.0dev2: device, img_gblur = **plantcv.gaussian_blur**(*device, img, ksize, sigmax=0, sigmay=None, debug=None*)
* post v3.0dev2: img_gblur = **plantcv.gaussian_blur**(*img, ksize, sigmax=0, sigmay=None*)
* post v3.2: img_gblur = **plantcv.gaussian_blur**(*img, ksize, sigma_x=0, sigma_y=None*)

#### plantcv.get_nir

* pre v3.0dev2: device, nirpath = **plantcv.get_nir**(*path, filename, device, debug=None*)
* post v3.0dev2: nirpath = **plantcv.get_nir**(*path, filename*)
* post v4.0: DEPRECATED

#### plantcv.hist_equalization

* pre v3.0dev2: device, img_eh = **plantcv.hist_equalization**(*img, device, debug=None*)
* post v3.0dev2: img_eh = **plantcv.hist_equalization**(*gray_img*)

#### plantcv.homology.acute

* pre v4.0: NA, see plantcv.acute
* post v4.0: homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist = **plantcv.homology.acute**(*img, mask, win, threshold*)

#### plantcv.homology.space

* pre v4.0: NA
* post v4.0: cur_plms = **plantcv.homology.space**(*cur_plms, include_bound_dist=False, include_centroid_dist=False, include_orient_angles=False*)

#### plantcv.homology.starscape

* pre v4.0: NA
* post v4.0: final_df, eigenvals, loadings = **plantcv.homology.starscape**(*cur_plms, group_a, group_b, outfile_prefix*)

#### plantcv.homology.constella

* pre v4.0: NA
* post v4.0: cur_plms, group_iter = **plantcv.homology.constella**(*cur_plms, pc_starscape, group_iter, outfile_prefix*)

#### plantcv.homology.constellaqc

* pre v4.0: NA
* post v4.0: **plantcv.homology.constellaqc**(*denovo_groups, annotated_groups*)

#### plantcv.homology.landmark_reference_pt_dist

* pre v4.0: see plantcv.landmark_reference_pt_dist
* post v4.0: **plantcv.homology.landmark_reference_pt_dist**(*points_r, centroid_r, bline_r, label=None*)

#### plantcv.homology.x_axis_pseudolandmarks

* pre v4.0: see plantcv.x_axis_pseudolandmarks
* post v4.0: top, bottom, center_v = **plantcv.homology.x_axis_pseudolandmarks**(*img, mask, label=None*)

#### plantcv.homology.y_axis_pseudolandmarks

* pre v4.0: see plantcv.y_axis_pseudolandmarks
* post v4.0: left, right, center_h = **plantcv.homology.y_axis_pseudolandmarks**(*img, mask, label=None*)

#### plantcv.homology.scale_features

* pre v4.0: see plantcv.scale_features
* post v4.0: rescaled, centroid_scaled, boundary_line_scaled = **plantcv.homology.scale_features**(*mask, points, line_position*)

#### plantcv.hyperspectral.analyze_index

* pre v3.7: NA
* post v3.7: **plantcv.hyperspectral.analyze_index**(*index_array, mask*)
* post v3.8: index_histogram = **plantcv.hyperspectral.analyze_index**(*index_array, mask, histplot=False, bins=100, max_bin=0, min_bin=1*)
* post v3.11: index_histogram = **plantcv.hyperspectral.analyze_index**(*index_array, mask, histplot=False, bins=100, max_bin=0, min_bin=1, label="default"*)
* post v4.0: DEPRECATED, see plantcv.analyze.spectral_index

#### plantcv.hyperspectral.analyze_spectral

* pre v3.7: NA
* post v3.7: spectral_histogram = **plantcv.hyperspectral.analyze_spectral**(*array, mask, histplot=True*)
* post v3.11: spectral_histogram =**plantcv.hyperspectral.analyze_spectral**(*array, mask, histplot=True, label="default"*)
* post v4.0: Deprecated, see: plantcv.analyze.spectral_reflectance

#### plantcv.hyperspectral.extract_index

* pre v3.7: NA
* post v3.7: index_array = **plantcv.hyperspectral.extract_index**(*array, index="NDVI", distance=20*)
* post v3.8: DEPRECATED see plantcv.spectral_index

#### plantcv.hyperspectral.rot90

* pre v4.x: NA
* post v4.x: rot_hsi = **plantcv.hyperspectral.rot90**(*spectral_data, k*)

#### plantcv.hyperspectral.write_data

* pre v4.0: NA
* post v4.0: **plantcv.hyperspectral.write_data**(*filename, spectral_data*)

#### plantcv.image_add

* pre v3.0dev2: device, added_img = **plantcv.image_add**(*img1, img2, device, debug=None*)
* post v3.0dev2: added_img = **plantcv.image_add**(*gray_img1, gray_img2*)

#### plantcv.image_subtract

* pre v3.0: NA
* post v3.0: new_img = **plantcv.image_subtract**(*gray_img1, gray_img2*)

#### plantcv.image_fusion

* pre v3.13.0: NA
* post v3.13.0: fused_img = **plantcv.image_fusion**(*img1, img2, wvs1, wvs2, array_type="multispectral"*)

#### plantcv.invert

* pre v3.0dev2: device, img_inv = **plantcv.invert**(*img, device, debug=None*)
* post v3.0dev2: img_inv = **plantcv.invert**(*gray_img*)

#### plantcv.io.open_url

* pre v4.2.1: NA
* post v4.2.1: img = **plantcv.io.open_url**(*url*)

#### plantcv.io.random_subset

* pre v3.14.0: NA
* post v3.14.0: sub_dataset = **plantcv.io.random_subset**(*dataset, num=100, seed=None*)

#### plantcv.io.read_dataset

* pre v3.14.0: NA
* post v3.14.0:  image_dataset = **plantcv.io.read_dataset**(*source_path, pattern='', sort=True*)

#### plantcv.landmark_reference_pt_dist

* pre v3.0dev2: device, vert_ave_c, hori_ave_c, euc_ave_c, ang_ave_c, vert_ave_b, hori_ave_b, euc_ave_b, ang_ave_b = **plantcv.landmark_reference_pt_dist**(*points_r, centroid_r, bline_r, device, debug=None*)
* post v3.0dev2: vert_ave_c, hori_ave_c, euc_ave_c, ang_ave_c, vert_ave_b, hori_ave_b, euc_ave_b, ang_ave_b = **plantcv.landmark_reference_pt_dist**(*points_r, centroid_r, bline_r*)
* post v3.2: landmark_header, landmark_data = **plantcv.landmark_reference_pt_dist**(*points_r, centroid_r, bline_r*)
* post v3.3: **plantcv.landmark_reference_pt_dist**(*points_r, centroid_r, bline_r*)
* post v3.11: **plantcv.landmark_reference_pt_dist**(*points_r, centroid_r, bline_r, label="default"*)
* post v4.0: DEPRECATED see plantcv.homology.landmark_reference_pt_dist


#### plantcv.laplace_filter

* pre v3.0dev2: device, lp_filtered = **plantcv.laplace_filter**(*img, k, scale, device, debug=None*)
* post v3.0dev2: lp_filtered = **plantcv.laplace_filter**(*gray_img, k, scale*)
* post v3.2: lp_filtered = **plantcv.laplace_filter**(*gray_img, ksize, scale*)

#### plantcv.learn.train_kmeans

* pre v4.3: NA 
* post v4.3: **plantcv.learn.train_kmeans**(*img_dir, k, out_path="./kmeansout.fit", prefix="", patch_size=10, sigma=5, sampling=None, seed=1, num_imgs=0, n_init=10*)

#### plantcv.logical_and

* pre v3.0dev2: device, merged = **plantcv.logical_and**(*img1, img2, device, debug=None*)
* post v3.0dev2: merged = **plantcv.logical_and**(*bin_img1, bin_img2*)

#### plantcv.logical_or

* pre v3.0dev2: device, merged = **plantcv.logical_or**(*img1, img2, device, debug=None*)
* post v3.0dev2: merged = **plantcv.logical_or**(*bin_img1, bin_img2*)

#### plantcv.logical_xor

* pre v3.0dev2: device, merged = **plantcv.logical_xor**(*img1, img2, device, debug=None*)
* post v3.0dev2: merged = **plantcv.logical_xor**(*bin_img1, bin_img2*)

#### plantcv.mask_kmeans

* pre v4.3: NA 
* post v4.3: **plantcv.mask_kmeans**(*labeled_img, k, patch_size, cat_list=None*)

#### plantcv.median_blur

* pre v3.0dev2: device, img_mblur = **plantcv.median_blur**(*img, ksize, device, debug=None*)
* post v3.0dev2: img_mblur = **plantcv.median_blur**(*gray_img, ksize*)
* post v3.2: img_blur = **plantcv.median_blur**(*gray_img, ksize*) OR img_blur = **plantcv.median_blur**(*gray_img, (ksize1, ksize2)*)

#### plantcv.morphology.analyze_stem

* pre v3.8: NA
* post v3.8: labeled_img = **plantcv.morphology.analyze_stem**(*rgb_img, stem_objects*)
* post v3.11: labeled_img = **plantcv.morphology.analyze_stem**(*rgb_img, stem_objects, label="default"*)
* post v4.0: labeled_img = **plantcv.morphology.analyze_stem**(*rgb_img, stem_objects, label=None*)

#### plantcv.morphology.check_cycles

* pre v3.3: NA
* post v3.3: cycle_img = **plantcv.morphology.check_cycles**(*skel_img*)
* post v3.11: cycle_img = **plantcv.morphology.check_cycles**(*skel_img, label="default"*)
* post v4.0: cycle_img = **plantcv.morphology.check_cycles**(*skel_img, label=None*)

#### plantcv.morphology.fill_segments
* pre v3.13: filled_img = **plantcv.morphology.fill_segments**(*mask, objects, stem_objects=None, label="default"*)
* post v3.13: filled_mask = **plantcv.morphology.fill_segments**(*mask, objects, stem_objects=None, label="default"*)
* post v4.0: filled_mask = **plantcv.morphology.fill_segments**(*mask, objects, stem_objects=None, label=None*)

#### plantcv.morphology.find_branch_pts

* pre v3.3: NA
* post v3.3: branch_pts_img = **plantcv.morphology.find_branch_pts**(*skel_img, mask=None*)
* post v3.11: branch_pts_img = **plantcv.morphology.find_branch_pts**(*skel_img, mask=None, label="default"*)
* post v4.0: branch_pts_img = **plantcv.morphology.find_branch_pts**(*skel_img, mask=None, label=None*)

#### plantcv.morphology.find_tips

* pre v3.3: NA
* post v3.3: tip_img = **plantcv.morphology.find_tips**(*skel_img, mask=None*)
* post v3.11: tip_img = **plantcv.morphology.find_tips**(*skel_img, mask=None, label="default"*)
* post v4.0: tip_img = **plantcv.morphology.find_tips**(*skel_img, mask=None, label=None*)

#### plantcv.morphology.prune

* pre v3.3: NA
* post v3.3: pruned_img = **plantcv.morphology.prune**(*skel_img, size*)
* post v3.4: pruned_skeleton, segmented_img, segment_objects = **plantcv.morphology.prune**(*skel_img, size=0, mask=None*)

#### plantcv.morphology.segment_angle

* pre v3.3: NA
* post v3.3: labeled_img = **plantcv.morphology.segment_angle**(*segmented_img, objects*)
* post v3.11: labeled_img = **plantcv.morphology.segment_angle**(*segmented_img, objects, label="default"*)
* post v4.0: labeled_img = **plantcv.morphology.segment_angle**(*segmented_img, objects, label=None*)

#### plantcv.morphology.segment_curvature

* pre v3.3: NA
* post v3.3: labeled_img = **plantcv.morphology.segment_curvature**(*segmented_img, objects*)
* post v3.11: labeled_img = **plantcv.morphology.segment_curvature**(*segmented_img, objects, label="default"*)
* post v4.0: labeled_img = **plantcv.morphology.segment_curvature**(*segmented_img, objects, label=None*)

#### plantcv.morphology.segment_ends 

* pre v4.8: NA
* post v4.8: sorted_obs, branch_pts, tips = **plantcv.morphology.segment_ends**(*skel_img, leaf_objects, mask=None, label=None*)

#### plantcv.morphology.segment_euclidean_length

* pre v3.3: NA
* post v3.3: labeled_img = **plantcv.morphology.segment_euclidean_length**(*segmented_img, objects*)
* post v3.11: labeled_img = **plantcv.morphology.segment_euclidean_length**(*segmented_img, objects, label="default"*)
* post v4.0: labeled_img = **plantcv.morphology.segment_euclidean_length**(*segmented_img, objects, label=None*)

#### plantcv.morphology.segment_id

* pre v3.3: NA
* post v3.3: segmented_img, labeled_img = **plantcv.morphology.segment_id**(*skel_img, objects, mask=None*)

#### plantcv.morphology.segment_path_length

* pre v3.3: NA
* post v3.3: labeled_img = **plantcv.morphology.segment_path_length**(*segmented_img, objects*)
* post v3.11: labeled_img = **plantcv.morphology.segment_path_length**(*segmented_img, objects, label="default"*)
* post v4.0: labeled_img = **plantcv.morphology.segment_path_length**(*segmented_img, objects, label=None*)

#### plantcv.morphology.segment_skeleton

* pre v3.3: NA
* post v3.3: segmented_img, segment_objects = **plantcv.morphology.segment_skeleton**(*skel_img, mask=None*)

#### plantcv.morphology.segment_sort

* pre v3.3: NA
* post v3.3: secondary_objects, primary_objects = **plantcv.morphology.segment_sort**(*skel_img, objects, mask=None*)

#### plantcv.morphology.segment_tangent_angle

* pre v3.3: NA
* post v3.3: labeled_img = **plantcv.morphology.segment_tangent_angle**(*segmented_img, objects, size*)
* post v3.11: labeled_img = **plantcv.morphology.segment_tangent_angle**(*segmented_img, objects, size, label="default"*)
* post v4.0: labeled_img = **plantcv.morphology.segment_tangent_angle**(*segmented_img, objects, size, label=None*)

#### plantcv.morphology.skeletontize

* pre v3.3: NA
* post v3.3: skeleton = **plantcv.morphology.skeletonize**(*mask*)

#### plantcv.naive_bayes_classifier

* pre v3.0dev2: device, masks = **plantcv.naive_bayes_classifier(*img, pdf_file, device, debug=None*)**
* post v3.0dev2: masks = **plantcv.naive_bayes_classifier(*rgb_img, pdf_file*)**

#### plantcv.object_composition

* pre v3.0dev2: device, group, mask = **plantcv.object_composition**(*img, contours, hierarchy, device, debug=None*)
* post v3.0dev2: group, mask = **plantcv.object_composition**(*img, contours, hierarchy*)
* post v4.0: DEPRECATED

#### plantcv.opening

* pre v3.3: NA
* post v3.3: filtered_img = **plantcv.opening**(*gray_img, kernel=None*)

#### plantcv.otsu_auto_threshold

* pre v3.0dev2: device, bin_img = **plantcv.otsu_auto_threshold**(*img, maxValue, object_type, device, debug=None*)
* post v3.0dev2: Deprecated, see:
    * bin_img = **plantcv.threshold.otsu**(*gray_img, max_value, object_type="light"*)

#### plantcv.output_mask

* pre v3.0dev2: device, maskpath, analysis_images = **plantcv.output_mask**(*device, img, mask, filename, outdir=None, mask_only=False, debug=None*)
* post v3.0dev2: imgpath, maskpath, analysis_images = **plantcv.output_mask**(*img, mask, filename, outdir=None, mask_only=False*)

#### plantcv.outputs.add_observation

* pre v3.3: NA
* post v3.3: **plantcv.outputs.add_observation**(*variable, trait, method, scale, datatype, value, label*)
* post v3.11: **plantcv.outputs.add_observation**(*sample, variable, trait, method, scale, datatype, value, label*)

#### plantcv.outputs.add_metadata

* pre v4.1: NA
* post v4.1: **plantcv.outputs.add_metadata**(*term, datatype, value*)

#### plantcv.outputs.clear

* pre v3.2: NA
* post v3.2: **plantcv.outputs.clear**()

#### plantcv.outputs.save_results

* pre v3.12: NA
* post v3.12: **plantcv.outputs.save_results**(*filename, outformat="json"*)

#### plantcv.photosynthesis.analyze_fvfm

* pre v3.10: see plantcv.fluor_fvfm
* post v3.10: analysis_images = **plantcv.photosynthesis.analyze_fvfm**(*fdark, fmin, fmax, mask, bins=256*)
* post v3.11: analysis_images = **plantcv.photosynthesis.analyze_fvfm**(*fdark, fmin, fmax, mask, bins=256, label="default"*)
* post v4.0: Deprecated, see: plantcv.analyze.yii

#### plantcv.photosynthesis.read_cropreporter

* pre v3.10: NA
* post v3.10: fdark, fmin, fmax = **plantcv.photosynthesis.read_cropreporter**(*filename*)
* post v4.0: ps = **plantcv.photosynthesis.read_cropreporter**(*filename*)

#### plantcv.photosynthesis.reassign_frame_labels

* pre v4.0: NA
* post v4.0: ps_da = **plantcv.photosynthesis.reassign_frame_labels(*ps_da, mask*)**

#### plantcv.plot_hist

* pre v3.0dev2: bins, hist = **plantcv.plot_hist**(*img, name=False*)
* post v3.0dev2: bins, hist = **plantcv.plot_hist**(*img, name=False*)
* post v3.2: Deprecated, see:
    * hist_header, hist_data, fig_hist = **plantcv.visualize.histogram**(*gray_img, mask=None, bins=256*)

#### plantcv.plot_image

* pre v3.0dev2: **plantcv.plot_image**(*img, cmap=None*)
* post v3.0dev2: **plantcv.plot_image**(*img, cmap=None*)

#### plantcv.Points

* pre v4.0: NA
* post v4.0: marker = **plantcv.Points**(*img, figsize=(6,12)*)

#### plantcv.predict_kmeans

* pre v4.3: NA
* post v4.3: **plantcv.predict_kmeans**(*img, model_path="./kmeansout.fit", patch_size=10*)

#### plantcv.print_image

* pre v3.0dev2: **plantcv.print_image**(*img, filename*)
* post v3.0dev2: **plantcv.print_image**(*img, filename*)

#### plantcv.print_results

* pre v3.1: NA
* post v3.1: **plantcv.print_results**(*filename*)
* post v4.0: DEPRECATED, see plantcv.outputs.save_results

#### plantcv.pseudocolor

* pre v3.1: NA
* post v3.1: pseudo_img = **plantcv.pseudocolor**(*gray_img, obj=None, mask=None, cmap=None, background="image", min_value=0, max_value=255, dpi=None, axes=True, colorbar=True*)
* post v3.2: Deprecated, see:
    * pseudo_img = **plantcv.visualize.pseudocolor**(*gray_img, obj=None, mask=None, cmap=None, background="image", min_value=0, max_value=255, axes=True, colorbar=True*)

#### plantcv.qc.exposure

* pre v4.3.1: NA
* post v4.3.1: chart = **plantcv.qc.exposure**(*rgb_img, warning_threshold=0.05*)

#### plantcv.readbayer

* pre v3.0: NA
* post v3.0: img, path, img_name = **plantcv.readbayer**(*filename, bayerpattern = 'BG', alg = 'default'*)

#### plantcv.readimage

* pre v3.0dev2: img, path, img_name = **plantcv.readimage**(*filename, debug=None*)
* post v3.0dev2: img, path, img_name = **plantcv.readimage**(*filename, mode="native"*)

#### plantcv.rectangle_mask

* pre v3.0dev2: device, img1, bnk, contour, hierarchy = **plantcv.rectangle_mask**(*img, p1, p2, device, debug=None, color="black"*)
* post v3.0dev2: img1, bnk, contour, hierarchy = **plantcv.rectangle_mask**(*img, p1, p2, color="black"*)
* post v4.0: DEPRECATED

#### plantcv.report_size_marker_area

* pre v3.0dev2: device, marker_header, marker_data, analysis_images = **plantcv.report_size_marker_area**(*img, shape, device, debug, marker='define', x_adj=0, y_adj=0, w_adj=0, h_adj=0, base='white', objcolor='dark', thresh_channel=None, thresh=None, filename=False*)
* post v3.0dev2: marker_header, marker_data, analysis_images = **plantcv.report_size_marker_area**(*img, roi_contour, roi_hierarchy, marker='define', objcolor='dark', thresh_channel=None, thresh=None, filename=False*)
* post v3.1: marker_header, marker_data, analysis_image = **plantcv.report_size_marker_area**(*img, roi_contour, roi_hierarchy, marker='define', objcolor='dark', thresh_channel=None, thresh=None*)
* post v3.3: analysis_image = **plantcv.report_size_marker_area**(*img, roi_contour, roi_hierarchy, marker='define', objcolor='dark', thresh_channel=None, thresh=None*)
* post v3.11: analysis_image = **plantcv.report_size_marker_area**(*img, roi_contour, roi_hierarchy, marker='define', objcolor='dark', thresh_channel=None, thresh=None, label="default"*)
* post v4.0: analysis_image = **plantcv.report_size_marker_area**(*img, roi, marker='define', objcolor='dark', thresh_channel=None, thresh=None, label=None*)

#### plantcv.resize

* pre v3.0dev2: device, reimg = **plantcv.resize**(*img, resize_x, resize_y, device, debug=None*)
* post v3.0dev2: reimg = **plantcv.resize**(*img, resize_x, resize_y*)
* post v3.11: Deprecated, see:
    * **pcv.transform.resize** and **pcv.transform.resize_factor**

#### plantcv.rgb2gray

* pre v3.0dev2: device, gray = **plantcv.rgb2gray**(*img, device, debug=None*)
* post v3.0dev2: gray = **plantcv.rgb2gray**(*rgb_img*)

#### plantcv.rgb2gray_hsv

* pre v3.0dev2: device, gray = **plantcv.rgb2gray_hsv**(*img, channel, device, debug=None*)
* post v3.0dev2: gray = **plantcv.rgb2gray_hsv**(*rgb_img, channel*)

#### plantcv.rgb2gray_lab

* pre v3.0dev2: device, gray = **plantcv.rgb2gray_lab**(*img, channel, device, debug=None*)
* post v3.0dev2: gray = **plantcv.rgb2gray_lab**(*rgb_img, channel*)

#### plantcv.roi.circle

* pre v3.0dev1: NA
* post v3.0dev2: roi_contour, roi_hierarchy = **plantcv.roi.circle**(*x, y, r, img*)
* post v3.2: roi_contour, roi_hierarchy = **plantcv.roi.circle**(*img, x, y, r*)
* post v4.0: roi = **plantcv.roi.circle**(*img, x, y, r*)

#### plantcv.roi.custom

* pre v3.0dev1: NA
* post v3.14: roi_contour, roi_hierarchy = **plantcv.roi.custom**(*img, vertices*)
* post v4.0: roi = **plantcv.roi.custom**(*img, vertices*)

#### plantcv.roi.ellipse

* pre v3.0dev1: NA
* post v3.0dev2: roi_contour, roi_hierarchy = **plantcv.roi.ellipse**(*x, y, r1, r2, angle, img*)
* post v3.2: roi_contour, roi_hierarchy = **plantcv.roi.ellipse**(*img, x, y, r1, r2, angle*)
* post v4.0: roi = **plantcv.roi.ellipse**(*img, x, y, r1, r2, angle*)

#### plantcv.roi.filter

* pre v4.0: NA
* post v4.0: filtered_mask = **pcv.roi.filter**(*mask, roi, roi_type='partial'*)

#### plantcv.roi.from_binary_image

* pre v3.0dev1: NA
* post v3.0dev2: roi_contour, roi_hierarchy = **plantcv.roi.from_binary_image**(*bin_img, img*)
* post v3.2: roi_contour, roi_hierarchy = **plantcv.roi.from_binary**(*img, bin_img*)
* post v4.0: roi = **plantcv.roi.from_binary**(*img, bin_img*)

#### plantcv.roi.rectangle

* pre v3.0dev1: NA
* post v3.0dev2: roi_contour, roi_hierarchy = **plantcv.roi.rectangle**(*x, y, h, w, img*)
* post v3.2: roi_contour, roi_hierarchy = **plantcv.roi.rectangle**(*img, x, y, h, w*)
* post v4.0: roi = **plantcv.roi.rectangle**(*img, x, y, h, w*)

#### plantcv.roi.roi2mask

* pre v3.8: NA
* post v3.8: mask = **pcv.roi.roi2mask**(*img, contour*)
* post v4.0: mask = **pcv.roi.roi2mask**(*img, roi*)

#### plantcv.roi.auto_grid

* pre v4.0: NA
* post v4.0: roi_objects = **pcv.roi.auto_grid**(*mask, nrows, ncols, radius=None, img=None*)

#### plantcv.roi.auto_wells

* pre v4.6: NA
* post v4.6: roi_objects = **pcv.roi.auto_wells**(*gray_img, mindist, candec, accthresh, minradius, maxradius, nrows, ncols, radiusadjust=None*)

#### plantcv.roi.multi

* pre v3.1: NA
* post v3.1: roi_contours, roi_hierarchies = **plantcv.roi.multi**(*img, coord, radius, spacing=None, nrows=None, ncols=None*)
* post v4.0: roi_objects = **plantcv.roi.multi**(*img, coord, radius=None, spacing=None, nrows=None, ncols=None*)

#### plantcv.roi.quick_filter

* pre v4.2.1: NA
* post v4.2.1: filtered_mask = **plantcv.roi.quick_filter**(*mask, roi*)

#### plantcv.roi_objects

* pre v3.0dev2: device, kept_cnt, hierarchy, mask, obj_area = **plantcv.roi_objects**(*img, roi_type, roi_contour, roi_hierarchy, object_contour, obj_hierarchy, device, debug=None*)
* post v3.0dev2: kept_cnt, hierarchy, mask, obj_area = **plantcv.roi_objects**(*img, roi_type, roi_contour, roi_hierarchy, object_contour, obj_hierarchy*)
* post v3.3: kept_cnt, hierarchy, mask, obj_area = **plantcv.roi_objects**(*img, roi_contour, roi_hierarchy, object_contour, obj_hierarchy,roi_type='partial'*)
* post v4.0: Deprecated, see:
    * filtered_mask = **pcv.roi.filter**(*mask, roi, roi_type='partial'*)

#### plantcv.transform.calibrate_camera

* pre v4.2.1: NA
* post v4.2.1: corrected_img = **plantcv.transform.calibrate_camera**(*rgb_img, mtx, dist*)

#### plantcv.transform.checkerboard_calib

* pre v4.2.1: NA
* post v4.2.1: mtx, dist = **plantcv.transform.checkerboard_calib**(*img_path, col_corners, row_corners, out_dir*)

#### plantcv.transform.mask_color_card 

* pre v4.8:  NA 
* post v4.8: color_card_mask = **plantcv.transform.mask_color_card**(*rgb_img, \*\*kwargs*)

#### plantcv.transform.rotate

* post v3.12.0: rotated_img = **plantcv.transform.rotate**(*img, rotation_deg, crop*)

#### plantcv.transform.warp

* pre v3.11.0: NA
* post v3.11.0: warped_img = **plantcv.transform.warp(*img, refimg, pts, refpts, method='default'*)**
* post v3.13.0: warped_img, mat = **plantcv.transform.warp(*img, refimg, pts, refpts, method='default'*)**

#### plantcv.transform.warp_align

* pre v3.13.0: NA
* post v3.13.0: warped_img = **plantcv.transform.warp_align(*img, refimg, mat*)**

#### plantcv.rotate

* pre v3.0dev2: device, rotated_img = **plantcv.rotate**(*img, rotation_deg, crop, device, debug=None*)
* post v3.0dev2: rotated_img = **plantcv.rotate**(*img, rotation_deg, crop*)
* post v4.0: DEPRECATED see plantcv.transform.rotate

#### plantcv.rotate_img

* pre v3.0dev2: device, rotated_img = **plantcv.rotate_img**(*img, rotation_deg, device, debug=None*)
* post v3.0dev2: DEPRECATED see plantcv.transform.rotate

#### plantcv.scale_features

* pre v3.0dev2: device, rescaled, centroid_scaled, boundary_line_scaled = **plantcv.scale_features**(*obj, mask, points, boundary_line, device, debug=None*)
* post v3.0dev2: rescaled, centroid_scaled, boundary_line_scaled = **plantcv.scale_features**(*obj, mask, points, boundary_line*)
* post v3.2: rescaled, centroid_scaled, boundary_line_scaled = **plantcv.scale_features**(*obj, mask, points, line_position*)
* post v4.0: DEPRECATED, see: plantcv.homology.scale_features

#### plantcv.scharr_filter

* pre v3.0dev2: device, sr_img = **plantcv.scharr_filter**(*img, dX, dY, scale, device, debug=None*)
* post v3.0dev2: sr_img = **plantcv.scharr_filter**(*gray_img, dx, dy, scale*)

#### plantcv.shift_img

* pre v3.0dev2: device, adjusted_img = **plantcv.shift_img**(*img, device, number, side="right", debug=None*)
* post v3.0dev2: adjusted_img = **plantcv.shift_img**(*img, number, side="right"*)

#### plantcv.segment_image_series

* pre v4.0: NA
* post v4.0: out_labels = **plantcv.segment_image_series**(*imgs_paths, masks_paths, rois, save_labels=True, ksize=3*)

#### plantcv.sobel_filter

* pre v3.0dev2: device, sb_img = **plantcv.sobel_filter**(*img, dx, dy, k, device, debug=None*)
* post v3.0dev2: sb_img = **plantcv.sobel_filter**(*gray_img, dx, dy, k*)
* post v3.2: sb_img = **plantcv.sobel_filer**(*gray_img, dx, dy, ksize*)

#### plantcv.spectral_index.ari

* post v3.8: array = **plantcv.spectral_index.ari**(*hsi, distance=20*)

#### plantcv.spectral_index.ci_rededge

* post v3.8: array = **plantcv.spectral_index.ci_rededge**(*hsi, distance=20*)

#### plantcv.spectral_index.cri550

* post v3.8: array = **plantcv.spectral_index.cri550**(*hsi, distance=20*)

#### plantcv.spectral_index.cri700

* post v3.8: array = **plantcv.spectral_index.cri700**(*hsi, distance=20*)

#### plantcv.spectral_index.egi

* post v3.8: array = **plantcv.spectral_index.egi**(*rgb_img*)
* post v4.4: array = **plantcv.spectral_index.egi**(*rgb_img, distance=40*)

#### plantcv.spectral_index.evi

* post v3.8: array = **plantcv.spectral_index.evi**(*hsi, distance=20*)

#### plantcv.spectral_index.gdvi

* post v3.8: array = **plantcv.spectral_index.gdvi**(*hsi, distance=20*)

#### plantcv.spectral_index.gli

* post v4.4: array = **plantcv.spectral_index.gli**(*img, distance=20*)

#### plantcv.spectral_index.mari

* post v3.8: array = **plantcv.spectral_index.mari**(*hsi, distance=20*)

#### plantcv.spectral_index.mcari

* post v3.8: array = **plantcv.spectral_index.mcari**(*hsi, distance=20*)

#### plantcv.spectral_index.mtci

* post v3.8: array = **plantcv.spectral_index.mtci**(*hsi, distance=20*)

#### plantcv.spectral_index.ndre

* post v3.8: array = **plantcv.spectral_index.ndre**(*hsi, distance=20*)

#### plantcv.spectral_index.ndvi

* post v3.8: array = **plantcv.spectral_index.ndvi**(*hsi, distance=20*)

#### plantcv.spectral_index.npci

* post v4.4: array = **plantcv.spectral_index.npci**(*hsi, distance=20*)

#### plantcv.spectral_index.pri

* post v3.8: array = **plantcv.spectral_index.pri**(*hsi, distance=20*)

#### plantcv.spectral_index.psnd_car

* post v3.8: array = **plantcv.spectral_index.psnd_car**(*hsi, distance=20*)

#### plantcv.spectral_index.psnd_chla

* post v3.8: array = **plantcv.spectral_index.psnd_chla**(*hsi, distance=20*)

#### plantcv.spectral_index.psnd_chlb

* post v3.8: array = **plantcv.spectral_index.psnd_chlb**(*hsi, distance=20*)

#### plantcv.spectral_index.psri

* post v3.8: array = **plantcv.spectral_index.psri**(*hsi, distance=20*)

#### plantcv.spectral_index.pssr_car

* post v3.8: array = **plantcv.spectral_index.pssr_car**(*hsi, distance=20*)

#### plantcv.spectral_index.pssr_chla

* post v3.8: array = **plantcv.spectral_index.pssr_chla**(*hsi, distance=20*)

#### plantcv.spectral_index.pssr_chlb

* post v3.8: array = **plantcv.spectral_index.pssr_chlb**(*hsi, distance=20*)

#### plantcv.spectral_index.rgri

* post v3.8: array = **plantcv.spectral_index.rgri**(*hsi, distance=20*)

#### plantcv.spectral_index.rvsi

* post v3.8: array = **plantcv.spectral_index.rvsi**(*hsi, distance=20*)

#### plantcv.spectral_index.savi

* post v3.8: array = **plantcv.spectral_index.savi**(*hsi, distance=20*)

#### plantcv.spectral_index.sipi

* post v3.8: array = **plantcv.spectral_index.sipi**(*hsi, distance=20*)

#### plantcv.spectral_index.sr

* post v3.8: array = **plantcv.spectral_index.sr**(*hsi, distance=20*)

#### plantcv.spectral_index.vari

* post v3.8: array = **plantcv.spectral_index.vari**(*hsi, distance=20*)

#### plantcv.spectral_index.vi_green

* post v3.8: array = **plantcv.spectral_index.vi_green**(*hsi, distance=20*)

#### plantcv.spectral_index.wi

* post v3.8: array = **plantcv.spectral_index.wi**(*hsi, distance=20*)

#### plantcv.stdev_filter

* pre v3.9: NA
* post v3.9: filtered_img = **plantcv.stdev_filter**(*img, kszie, borders="nearest"*)

#### plantcv.threshold.dual_channels

* pre v4.0: NA
* post v4.0: bin_img = **plantcv.threshold.dual_channels**(*rgb_img, x_channel, y_channel, points, above=True*)

#### plantcv.threshold.binary

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = **plantcv.threshold.binary**(*gray_img, threshold, max_value, object_type="light"*)
* post v4.0: bin_img = **plantcv.threshold.binary**(*gray_img, threshold, object_type="light"*)

#### plantcv.threshold.custom_range

* pre v3.3: NA
* post v3.3: mask, masked_img = **plantcv.threshold.custom_range**(*rgb_img, lower_thresh, upper_thresh, channel='RGB'*)**
* post v3.8: mask, masked_img = **plantcv.threshold.custom_range**(*img, lower_thresh, upper_thresh, channel='RGB'*)**

#### plantcv.threshold.gaussian

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = **plantcv.threshold.gaussian**(*gray_img, max_value, object_type="light"*)
* post v4.0: bin_img = **plantcv.threshold.gaussian**(*gray_img, ksize, offset, object_type="light"*)

#### plantcv.threshold.mean

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = **plantcv.threshold.mean**(*gray_img, max_value, object_type="light"*)
* post v4.0: bin_img = **plantcv.threshold.mean**(*gray_img, ksize, offset, object_type="light"*)

#### plantcv.threshold.otsu

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = **plantcv.threshold.otsu**(*gray_img, max_value, object_type="light"*)
* post v4.0: bin_img = **plantcv.threshold.otsu**(*gray_img, object_type="light"*)

#### plantcv.threshold.saturation

* pre v3.8: NA
* post v3.8: bin_img = **plantcv.threshold.saturation**(*rgb_img, threshold=255, channel="any"*)

#### plantcv.threshold.texture

* pre v3.0: NA
* post v3.0: bin_img = **plantcv.threshold.texture**(*gray_img, ksize, threshold, offset=3, texture_method='dissimilarity', borders='nearest', max_value=255*)
* post v4.0: bin_img = **plantcv.threshold.texture**(*gray_img, ksize, threshold, offset=3, texture_method='dissimilarity', borders='nearest'*)

#### plantcv.threshold.triangle

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = **plantcv.threshold.triangle**(*gray_img, max_value, object_type="light", xstep=1*)
* post v4.0: bin_img = **plantcv.threshold.triangle**(*gray_img, object_type="light", xstep=1*)

#### plantcv.transform.affine_color_correction

* pre v4.0: NA
* post v4.0: **plantcv.transform.affine_color_correction**(*rgb_img, source_matrix, target_matrix*)

#### plantcv.transform.apply_transformation_matrix

* pre v3.0dev1: NA
* post v3.0dev2: corrected_img = **plantcv.transform.apply_transformation_matrix**(*source_img, target_img, transformation_matrix*)

#### plantcv.transform.calc_transformation_matrix

* pre v3.0dev1: NA
* post v3.0dev2: determinant, transformation_matrix = **plantcv.transform.calc_transformation_matrix**(*matrix_m, matrix_b*)

#### plantcv.transform.auto_correct_color

* pre v4.6: NA
* post v4.6: corrected_img = **plantcv.transform.auto_correct_color**(*rgb_img, label=None, \*\*kwargs*)
* post v4.9: corrected_img = **plantcv.transform.auto_correct_color**(*rgb_img, label=None, color_chip_size=None, \*\*kwargs*)

#### plantcv.transform.correct_color

* pre v3.0dev1: NA
* post v3.0dev2: target_matrix, source_matrix, transformation_matrix, corrected_img = **plantcv.transform.correct_color**(*target_img, target_mask, source_img, source_mask, output_directory*)

#### plantcv.transform.create_color_card_mask

* pre v3.0: NA
* post v3.0: mask = **pcv.transform.create_color_card_mask**(*rgb_img, radius, start_coord, spacing, nrows, ncols, exclude=[]*)

#### plantcv.transform.detect_color_card

* pre v4.0.1: NA
* post v4.0.1: labeled_mask = **plantcv.transform.detect_color_card**(*rgb_img, label=None, \*\*kwargs*)
* post v4.9: labeled_mask = **plantcv.transform.detect_color_card**(*rgb_img, label=None, color_chip_size=None, \*\*kwargs*)

#### plantcv.transform.find_color_card

* pre v3.0: NA
* post v3.0: df, start_coord, spacing = **plantcv.transform.find_color_card**(*rgb_img, threshold='adaptgauss', threshvalue=125, blurry=False, background='dark'*)
* post v3.3: df, start_coord, spacing = **plantcv.transform.find_color_card**(*rgb_img, threshold_type='adaptgauss', threshvalue=125, blurry=False, background='dark'*)
* post v3.9: df, start_coord, spacing = **plantcv.transform.find_color_card**(*rgb_img, threshold_type='adaptgauss', threshvalue=125, blurry=False, background='dark', record_chip_size='median'*)
* post v3.11: df, start_coord, spacing = **plantcv.transform.find_color_card**(*rgb_img, threshold_type='adaptgauss', threshvalue=125, blurry=False, background='dark', record_chip_size='median', label="default"*)
* post v4.0: df, start_coord, spacing = **plantcv.transform.find_color_card**(*rgb_img, threshold_type='adaptgauss', threshvalue=125, blurry=False, background='dark', record_chip_size='median', label=None*)

#### plantcv.transform.gamma_correct

* pre v3.12.1: NA
* post v3.13: corrected_img = **plantcv.transform.gamma_correct**(*img, gamma=1, gain=1*)

#### plantcv.transform.get_color_matrix

* pre v3.0dev1: NA
* post v3.0dev2: headers, color_matrix = **plantcv.transform.get_color_matrix**(*rgb_img, mask*)

#### plantcv.transform.get_matrix_m

* pre v3.0dev1: NA
* post v3.0dev2: matrix_a, matrix_m, matrix_b = **plantcv.transform.get_matrix_m**(*target_matrix, source_matrix*)

#### plantcv.transform.load_matrix

* pre v3.0dev1: NA
* post v3.0dev2: matrix = **plantcv.transform.load_matrix**(*filename*)

#### plantcv.transfor.merge_images

* pre v4.2.1: NA
* post v4.2.1: merged_img = **plantcv.transform.merge_images**(*paths_to_imgs, overlap_percentage, direction = "vertical", method = "stacked"*)

#### plantcv.transform.resize

* pre v3.11: NA
* post v3.11: resized_img = **plantcv.transform.resize**(*img, size, interpolation="auto"*)

#### plantcv.transform.resize_factor

* pre v3.11: NA
* post v3.11: resized_img = **plantcv.transform.resize_factor**(*img, factors, interpolation="auto"*)


#### plantcv.transform.nonuniform_illumination

* pre v3.5: NA
* post v3.5: corrected_img = **plantcv.transform.nonuniform_illumination**(*img, ksize*)

#### plantcv.transform.quick_color_check

* pre v3.0: NA
* post v3.0: **plantcv.transform.quick_color_check**(*target_matrix, source_matrix, num_chips*)
* post v4.0: chart = **plantcv.transform.quick_color_check**(*target_matrix, source_matrix, num_chips*)

#### plantcv.transform.save_matrix

* pre v3.0dev1: NA
* post v3.0dev2: **plantcv.transform.save_matrix**(*matrix, filename*)

#### plantcv.transform.std_color_matrix

* pre v4.0: NA
* post v4.0: **plantcv.transform.std_color_matrix**(*pos=0*)

#### plantcv.triangle_auto_threshold

* pre v3.0dev2: device, bin_img = **plantcv.triangle_auto_threshold**(*device, img, maxvalue, object_type, xstep=1, debug=None*)
* post v3.0dev2: Deprecated, see:
    * bin_img = **plantcv.threshold.triangle**(*gray_img, max_value, object_type="light", xstep=1*)

#### plantcv.visualize.chlorophyll_fluorescence

* pre v4.0: NA
* post v4.0: chart = **plantcv.visualize.chlorophyll_fluorescence**(*ps_da, labeled_mask, n_labels=1, label="object"*)

#### plantcv.visualize.colorize_label_img

* pre v3.13: NA
* post v3.13: colored_img = **plantcv.visualize.colorize_label_img**(*label_img*)

#### plantcv.visualize.colorize_masks

* pre v3.2: NA
* post v3.2: colored_img = pcv.visualize.colorize_masks(classes, colors)

#### plantcv.visualize.colorspaces

* pre v3.8: NA
* post v3.8: plotting_img = pcv.visualize.colorspaces(rgb_img, original_img=True)

#### plantcv.visualize.histogram

* pre v3.2: bins, hist = **plantcv.plot_hist**(*img, name=False*)
* post v3.2: hist_header, hist_data, fig_hist = **plantcv.visualize.histogram**(*gray_img, mask=None, bins=256*)
* post v3.3: hist_header, hist_data, fig_hist = **plantcv.visualize.histogram**(*gray_img, mask=None, bins=256, color='red', title=None*)
* post v3.5: fig_hist = **plantcv.visualize.histogram**(*gray_img, mask=None, bins=256, color='red', title=None*)
* post v3.12: fig_hist, hist_data = **plantcv.visualize.histogram**(*img, mask=None, bins=100, lower_bound=None, upper_bound=None, title=None, hist_data=False*)

#### plantcv.visualize.hyper_histogram

* pre v3.13: NA
* post v3.13: fig_hist = **plantcv.visualize.hyper_histogram**(*hsi, mask=None, bins=100, lower_bound=None, upper_bound=None, title=None, wvlengths=[480, 550, 650]*)

#### plantcv.visualize.obj_size_ecdf

* pre v3.13: NA
* post v3.13: fig_ecdf = **plantcv.visualize.obj_size_ecdf**(*mask, title=None*)
* post v4.0: fig_ecdf = **plantcv.visualize.obj_size_ecdf**(*mask*)

#### plantcv.visualize.obj_sizes

* pre v3.13: NA
* post v3.13: plotting_img = **pcv.visualize.obj_sizes**(*img, mask, num_objects=100*)

#### plantcv.visualize.pseudocolor

* pre v3.2: pseudo_img = **plantcv.pseudocolor**(*gray_img, obj=None, mask=None, cmap=None, background="image", min_value=0, max_value=255, dpi=None, axes=True, colorbar=True*)
* post v3.2: pseudo_img = **plantcv.visualize.pseudocolor**(*gray_img, obj=None, mask=None, cmap=None, background="image", min_value=0, max_value=255, dpi=None, axes=True, colorbar=True*)
* post v3.3: pseudo_img = **plantcv.visualize.pseudocolor**(*gray_img, obj=None, mask=None, cmap=None, background="image", min_value=0, max_value=255, axes=True, colorbar=True*)
* post v3.12: pseudo_img = **plantcv.visualize.pseudocolor**(*gray_img, obj=None, mask=None, cmap=None, background="image", min_value=0, max_value=255, axes=True, colorbar=True, obj_padding="auto", title=None*)
* post v4.0: pseudo_img = **plantcv.visualize.pseudocolor**(*gray_img, mask=None, cmap=None, background="image", min_value=0, max_value=255, axes=True, colorbar=True, title=None*)

#### plantcv.visualize.pixel_scatter_plot

* pre v4.0: NA
* post v4.0: fig, ax = **pcv.visualize.pixel_scatter_plot**(*paths_to_imgs, x_channel, y_channel*)

#### plantcv.visualize.tile

* pre v4.4: NA
* post v4.4: tile_img = **pcv.visualize.tile**(*img_list, ncol*)

#### plantcv.visualize.time_lapse_video

* pre v4.0: NA
* post v4.0: frame_size = **pcv.visualize.time_lapse_video**(*img_list, out_filename='./time_lapse_video.mp4', fps=29.97, display=True*)

#### plantcv.watershed_segmentation

* pre v3.0dev2: device, watershed_header, watershed_data, analysis_images = **plantcv.watershed_segmentation**(*device, img, mask, distance=10, filename=False, debug=None*)
* post v3.0dev2: watershed_header, watershed_data, analysis_images = **plantcv.watershed_segmentation**(*rgb_img, mask, distance=10, filename=False*)
* post v3.1: watershed_header, watershed_data, analysis_images = **plantcv.watershed_segmentation**(*rgb_img, mask, distance=10*)
* post v3.3: analysis_image = **plantcv.watershed_segmentation**(*rgb_img, mask, distance=10*)
* post v3.11: analysis_image = **plantcv.watershed_segmentation**(*rgb_img, mask, distance=10, label="default"*)
* post v4.0: analysis_image = **plantcv.watershed_segmentation**(*rgb_img, mask, distance=10, label=None*)
* post v4.3: labeled_mask = **plantcv.watershed_segmentation**(*rgb_img, mask, distance=10, label=None*)

#### plantcv.white_balance

* pre v3.0dev2: device, finalcorrected = **plantcv.white_balance**(*device, img, mode='hist',debug=None, roi=None*)
* post v3.0dev2: finalcorrected = **plantcv.white_balance**(*img, mode='hist', roi=None*)

#### plantcv.within_frame

* pre v3.3: NA
* post v3.3: in_bounds = **plantcv.within_frame**(*mask*)
* post v3.8: in_bounds = **plantcv.within_frame**(*mask, border_width=1*)
* post v3.11: in_bounds = **plantcv.within_frame**(*mask, border_width=1, label="default"*)
* post v4.0: in_bounds = **plantcv.within_frame**(*mask, border_width=1, label=None*)

#### plantcv.x_axis_pseudolandmarks

* pre v3.0dev2: device, top, bottom, center_v = **plantcv.x_axis_pseudolandmarks**(*obj, mask, img, device, debug=None*)
* post v3.0dev2: top, bottom, center_v = **plantcv.x_axis_pseudolandmarks**(*obj, mask, img*)
* post v3.2: top, bottom, center_v = **plantcv.x_axis_pseudolandmarks**(*img, obj, mask*)
* post v3.11: top, bottom, center_v = **plantcv.x_axis_pseudolandmarks**(*img, obj, mask, label="default"*)
* post v4.0: DEPRECATED, see: plantcv.homology.x_axis_pseudolandmarks


#### plantcv.y_axis_pseudolandmarks

* pre v3.0dev2: device, left, right, center_h = **plantcv.y_axis_pseudolandmarks**(*obj, mask, img, device, debug=None*)
* post v3.0dev2: left, right, center_h = **plantcv.y_axis_pseudolandmarks**(*obj, mask, img*)
* post v3.2: left, right, center_h = **plantcv.y_axis_pseudolandmarks**(*img, obj, mask*)
* post v3.11: left, right, center_h = **plantcv.y_axis_pseudolandmarks**(*img, obj, mask, label="default"*)
* post v4.0: Deprecated, see: plantcv.homology.y_axis_pseudolandmarks
