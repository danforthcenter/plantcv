## Updating PlantCV

The general procedure for updating PlantCV if you are using the `master` branch
cloned from the `danforthcenter/plantcv` repository is to update your local 
repository and reinstall the package.

If you are not sure that you have cloned the `danforthcenter/plantcv` repository
and are on the `master` branch, here is how you can tell:

```
cd plantcv

git remote -v

# You should see something like:
# origin	https://github.com/danforthcenter/plantcv.git (fetch)

git status

# You should see:
# On branch master
# nothing to commit, working directory clean
```

If the above is true, updating can be done simply by:

```
git pull

python setup.py install

# Or with sudo if needed
```

If you have put the cloned plantcv repository folder in your `PYTHONPATH` then
pulling alone is enough to update.

### Updating from v1 to v2

The setuptools installation method was not available in PlantCV v1, so users
put the `plantcv/lib` directory in their custom `PYTHONPATH`. In PlantCV v2, the
plantcv library directory is no longer in the lib directory, now it is in the 
main repository folder (`plantcv/plantcv`). If you want to continue to have
plantcv in your `PYTHONPATH` you will need to update by simply removing `lib`
from the path. You can also remove the lib folder after pulling the new version.
Git will automatically remove the `*.py` files but because we do not track the
`*.pyc` files they will remain behind and can technically be imported, which can
cause confusion.

For Linux/Unix, `PYTHONPATH` can be edited in `~/.bash_profile`, `~/.bashrc`,
`~/.profile`, `~/.cshrc`, `~/.zshrc`, etc. For Windows, right-click on My 
Computer/This PC and select Properties > Advanced system settings >
Environmental Variables... and edit the User variables entry for `PYTHONPATH`.

Also note that the method for parallelizing PlantCV has changed, please see the
new [parallel processing documentation](pipeline_parallel.md) for more details.

### Updating to v3

In addition to new features a major goal ov PlantCV v3 is to make PlantCV functions
a little bit easier to use. We hope you agree the changes detailed below succeed
in that goal, but if you have any questions or concerns please feel free to open
an issue on GitHub or contact us directly.

In order to support the installation of optional add-on subpackages, we converted
PlantCV to a [namespace package](https://packaging.python.org/guides/packaging-namespace-packages/).
To achieve this new functionality, existing functions had to be moved into a 
subpackage to maintain easy importing. To maintain previous behavior, PlantCV
analysis scripts simply need to have updated PlantCV import syntax. So if you were
previously doing something like:

```python
import plantcv as pcv
```

You would now do this instead:

```python
from plantcv import plantcv as pcv
```

Another feature we will be rolling out for PlantCV v3 an update to the existing
package API. The goal is to make each PlantCV function easier to use by reducing
the number of inputs and outputs that need to be configured (without losing
functionality) and by making input parameters more consistently named and clearly
defined where input types matter (e.g. instead of just `img` it could be `rgb_img`,
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

Therefore, all function calls need to be updated to remove the `device` input and
output variables and the `debug` input variable. For example:

```python
from plantcv import plantcv as pcv
pcv.params.debug = "plot"

img, img_path, img_filename = pcv.readimage("image.png")

gray_img = pcv.rgb2gray_hsv(img, "s")

bin_img = pcv.threshold.binary(gray_img, 100, 255)
```

For more information, see the [Params](params.md) documentation.

Below is an overview of all updates that are required to convert a pre-v3.0dev2
function call to a post-v3.0dev2 function call and all updates following the v3.0 release.
See the individual function help
pages for more details on the input and output variable types.

#### plantcv.acute

* pre v3.0dev2: device, homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist = **plantcv.acute**(*obj, win, thresh, mask, device, debug=None*)
* post v3.0dev2: homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist = **plantcv.acute**(*obj, win, thresh, mask*)

#### plantcv.acute_vertex

* pre v3.0dev2: device, acute = **plantcv.acute_vertex**(*obj, win, thresh, sep, img, device, debug=None*)
* post v3.0dev2: acute = **plantcv.acute_vertex**(*obj, win, thresh, sep, img*)

#### plantcv.adaptive_threshold

* pre v3.0dev2: device, bin_img = **plantcv.adaptive_threshold**(*img, maxValue, thres_type, object_type, device, debug=None*)
* post v3.0dev2: Deprecated, see:
    * bin_img = **plantcv.threshold.gaussian**(*gray_img, max_value, object_type="light"*)
    * bin_img = **plantcv.threshold.mean**(*gray_img, max_value, object_type="light"*)

#### plantcv.analyze_bound

* pre v3.0dev2: device, bound_header, bound_data, analysis_images = **plantcv.analyze_bound**(*img, imgname, obj, mask, line_position, device, debug=None, filename=False*)
* post v3.0dev2: Deprecated, see:
    * bound_header, bound_data, analysis_images = **plantcv.analyze_bound_horizontal**(*img, obj, mask, line_position, filename=False*)

#### plantcv.analyze_bound_horizontal

* pre v3.0dev2: device, bound_header, bound_data, analysis_images = **plantcv.analyze_bound_horizontal**(*img, obj, mask, line_position, device, debug=None, filename=False*)
* post v3.0dev2: bound_header, bound_data, analysis_images = **plantcv.analyze_bound_horizontal**(*img, obj, mask, line_position, filename=False*)
* post v3.0.5: bound_header, bound_data, analysis_images = **plantcv.analyze_bound_horizontal**(*img, obj, mask, line_position*)

#### plantcv.analyze_bound_vertical

* pre v3.0dev2: device, bound_header, bound_data, analysis_images = **plantcv.analyze_bound_vertical**(*img, obj, mask, line_position, device, debug=None, filename=False*)
* post v3.0dev2: bound_header, bound_data, analysis_images = **plantcv.analyze_bound_vertical**(*img, obj, mask, line_position, filename=False*)
* post v3.0.5: bound_header, bound_data, analysis_images = **plantcv.analyze_bound_vertical**(*img, obj, mask, line_position*)


#### plantcv.analyze_color

* pre v3.0dev2: device, hist_header, hist_data, analysis_images = **plantcv.analyze_color**(*img, imgname, mask, bins, device, debug=None, hist_plot_type=None, pseudo_channel='v', pseudo_bkg='img', resolution=300, filename=False*)
* post v3.0dev2: hist_header, hist_data, analysis_images = **plantcv.analyze_color**(*rgb_img, mask, bins, hist_plot_type=None, pseudo_channel='v', pseudo_bkg='img', filename=False*)
* post v3.0.5: hist_header, hist_data, analysis_images = **plantcv.analyze_color**(*rgb_img, mask, bins, hist_plot_type=None*)

#### plantcv.apply_mask

* pre v3.0dev2: device, masked_img = **plantcv.apply_mask**(*img, mask, mask_color, device, debug=None*)
* post v3.0dev2: masked_img = **plantcv.apply_mask**(*rgb_img, mask, mask_color*)

#### plantcv.analyze_nir_intensity

* pre v3.0dev2: device, hist_header, hist_data, analysis_img = **plantcv.analyze_NIR_intensity**(*img, rgbimg, mask, bins, device, histplot=False, debug=None, filename=False*)
* post v3.0dev2: hist_header, hist_data, analysis_img = **plantcv.analyze_nir_intensity**(*gray_img, mask, bins, histplot=False, filename=False*)
* post v3.0.5: hist_header, hist_data, nir_hist = **plantcv.analyze_nir_intensity**(*gray_img, mask, bins, histplot=False*)

#### plantcv.analyze_object

* pre v3.0dev2: device, shape_header, shape_data, analysis_images = **plantcv.analyze_object**(*img, imgname, obj, mask, device, debug=None, filename=False*)
* post v3.0dev2: shape_header, shape_data, analysis_images = **plantcv.analyze_object**(*img, obj, mask, filename=False*)
* post v3.0.5: shape_header, shape_data, analysis_images = **plantcv.analyze_object**(*img, obj, mask*)

#### plantcv.auto_crop

* pre v3.0dev2: device, cropped = **plantcv.auto_crop**(*device, img, objects, padding_x=0, padding_y=0, color='black', debug=None*)
* post v3.0dev2: cropped = **plantcv.auto_crop**(*img, objects, padding_x=0, padding_y=0, color='black'*)

#### plantcv.background_subtraction

* pre v3.0dev2: device, fgmask = **plantcv.background_subtraction**(*background_image, foreground_image, device, debug=None*)
* post v3.0dev2: fgmask = **plantcv.background_subtraction**(*background_image, foreground_image*)

#### plantcv.binary_threshold

* pre v3.0dev2: device, bin_img = **plantcv.binary_threshold**(*img, threshold, maxValue, object_type, device, debug=None*)
* post v3.0dev2: Deprecated, see:
    * bin_img = **plantcv.threshold.binary**(*gray_img, threshold, max_value, object_type="light"*)

#### plantcv.cluster_contour_splitimg

* pre v3.0dev2: device, output_path = **plantcv.cluster_contour_splitimg**(*device, img, grouped_contour_indexes, contours, hierarchy, outdir=None, file=None, filenames=None, debug=None*)
* post v3.0dev2: output_path = **plantcv.cluster_contour_splitimg**(*rgb_img, grouped_contour_indexes, contours, hierarchy, outdir=None, file=None, filenames=None*)

#### plantcv.cluster_contours

* pre v3.0dev2: device, grouped_contour_indexes, contours, roi_obj_hierarchy = **plantcv.cluster_contours**(*device, img, roi_objects,roi_obj_hierarchy, nrow=1, ncol=1, debug=None*)
* post v3.0dev2: grouped_contour_indexes, contours, roi_obj_hierarchy = **plantcv.cluster_contours**(*img, roi_objects, roi_obj_hierarchy, nrow=1, ncol=1*)

#### plantcv.color_palette

* pre v3.0: NA
* post v3.0: colors = **plantcv.color_palette**(*num*)

#### plantcv.crop_position_mask

* pre v3.0dev2: device, newmask = **plantcv.crop_position_mask**(*img, mask, device, x, y, v_pos="top", h_pos="right", debug=None*)
* post v3.0dev2: newmask = **plantcv.crop_position_mask**(*img, mask, x, y, v_pos="top", h_pos="right"*)

#### plantcv.define_roi

* pre v3.0dev2: device, contour, hierarchy = **plantcv.define_roi**(*img, shape, device, roi=None, roi_input='default', debug=None, adjust=False, x_adj=0, y_adj=0, w_adj=0, h_adj=0*)
* post v3.0dev2: Deprecated, see:
    * roi_contour, roi_hierarchy = **plantcv.roi.circle**(*x, y, r, img*)
    * roi_contour, roi_hierarchy = **plantcv.roi.ellipse**(*x, y, r1, r2, angle, img*)
    * roi_contour, roi_hierarchy = **plantcv.roi.from_binary_image**(*bin_img, img*)
    * roi_contour, roi_hierarchy = **plantcv.roi.rectangle**(*x, y, h, w, img*)

#### plantcv.dilate

* pre v3.0dev2: device, dil_img = **plantcv.dilate**(*img, kernel, i, device, debug=None*)
* post v3.0dev2: dil_img = **plantcv.dilate**(*gray_img, kernel, i*)

#### plantcv.distance_transform

* pre v3.0dev2: device, norm_image = **plantcv.distance_transform**(*img, distanceType, maskSize, device, debug=None*)
* post v3.0dev2: norm_image = **plantcv.distance_transform**(*bin_img, distance_type, mask_size*)

#### plantcv.erode

* pre v3.0dev2: device, er_img = **plantcv.erode**(*img, kernel, i, device, debug=None*)
* post v3.0dev2: er_img = **plantcv.erode**(*gray_img, kernel, i*)

#### plantcv.fill

* pre v3.0dev2: device, filtered_img = **plantcv.fill**(*img, mask, size, device, debug=None*)
* post v3.0dev2: filtered_img = **plantcv.fill**(*bin_img, size*)

#### plantcv.find_objects

* pre v3.0dev2: device, objects, hierarchy = **plantcv.find_objects**(*img, mask, device, debug=None*)
* post v3.0dev2: objects, hierarchy = **plantcv.find_objects**(*img, mask*)

#### plantcv.flip

* pre v3.0dev2: device, vh_img = **plantcv.flip**(*img, direction, device, debug=None*)
* post v3.0dev2: vh_img = **plantcv.flip**(*img, direction*)

#### plantcv.fluor_fvfm

* pre v3.0dev2: device, hist_header, hist_data = **plantcv.fluor_fvfm**(*fdark, fmin, fmax, mask, device, filename, bins=1000, debug=None*)
* post v3.0dev2: hist_header, hist_data, hist_images = **plantcv.fluor_fvfm**(*fdark, fmin, fmax, mask, filename, bins=256*)
* post v3.0.5: hist_header, hist_data, analysis_images = **plantcv.fluor_fvfm**(*fdark, fmin, fmax, mask, bins=256*)

#### plantcv.gaussian_blur

* pre v3.0dev2: device, img_gblur = **plantcv.gaussian_blur**(*device, img, ksize, sigmax=0, sigmay=None, debug=None*)
* post v3.0dev2: img_gblur = **plantcv.gaussian_blur**(*img, ksize, sigmax=0, sigmay=None*)

#### plantcv.get_nir

* pre v3.0dev2: device, nirpath = **plantcv.get_nir**(*path, filename, device, debug=None*)
* post v3.0dev2: nirpath = **plantcv.get_nir**(*path, filename*)

#### plantcv.hist_equalization

* pre v3.0dev2: device, img_eh = **plantcv.hist_equalization**(*img, device, debug=None*)
* post v3.0dev2: img_eh = **plantcv.hist_equalization**(*gray_img*)

#### plantcv.image_add

* pre v3.0dev2: device, added_img = **plantcv.image_add**(*img1, img2, device, debug=None*)
* post v3.0dev2: added_img = **plantcv.image_add**(*gray_img1, gray_img2*)

#### plantcv.image_subtract

pre v3.0: NA
post v3.0: new_img = **plantcv.image_subtract**(*gray_img1, gray_img2*)

#### plantcv.invert

* pre v3.0dev2: device, img_inv = **plantcv.invert**(*img, device, debug=None*)
* post v3.0dev2: img_inv = **plantcv.invert**(*gray_img*)

#### plantcv.landmark_reference_pt_dist

* pre v3.0dev2: device, vert_ave_c, hori_ave_c, euc_ave_c, ang_ave_c, vert_ave_b, hori_ave_b, euc_ave_b, ang_ave_b = **plantcv.landmark_reference_pt_dist**(*points_r, centroid_r, bline_r, device, debug=None*)
* post v3.0dev2: vert_ave_c, hori_ave_c, euc_ave_c, ang_ave_c, vert_ave_b, hori_ave_b, euc_ave_b, ang_ave_b = **plantcv.landmark_reference_pt_dist**(*points_r, centroid_r, bline_r*)

#### plantcv.laplace_filter

* pre v3.0dev2: device, lp_filtered = **plantcv.laplace_filter**(*img, k, scale, device, debug=None*)
* post v3.0dev2: lp_filtered = **plantcv.laplace_filter**(*gray_img, k, scale*)

#### plantcv.logical_and

* pre v3.0dev2: device, merged = **plantcv.logical_and**(*img1, img2, device, debug=None*)
* post v3.0dev2: merged = **plantcv.logical_and**(*bin_img1, bin_img2*)

#### plantcv.logical_or

* pre v3.0dev2: device, merged = **plantcv.logical_or**(*img1, img2, device, debug=None*)
* post v3.0dev2: merged = **plantcv.logical_or**(*bin_img1, bin_img2*)

#### plantcv.logical_xor

* pre v3.0dev2: device, merged = **plantcv.logical_xor**(*img1, img2, device, debug=None*)
* post v3.0dev2: merged = **plantcv.logical_xor**(*bin_img1, bin_img2*)

#### plantcv.median_blur

* pre v3.0dev2: device, img_mblur = **plantcv.median_blur**(*img, ksize, device, debug=None*)
* post v3.0dev2: img_mblur = **plantcv.median_blur**(*gray_img, ksize*)
* post v3.0: img_blur = **plantcv.median_blur**(*gray_img, ksize*) OR img_blur = **plantcv.median_blur**(*gray_img, (ksize1, ksize2)*)

#### plantcv.naive_bayes_classifier

* pre v3.0dev2: device, masks = **plantcv.naive_bayes_classifier(*img, pdf_file, device, debug=None*)**
* post v3.0dev2: masks = **plantcv.naive_bayes_classifier(*rgb_img, pdf_file*)**

#### plantcv.object_composition

* pre v3.0dev2: device, group, mask = **plantcv.object_composition**(*img, contours, hierarchy, device, debug=None*)
* post v3.0dev2: group, mask = **plantcv.object_composition**(*img, contours, hierarchy*)

#### plantcv.otsu_auto_threshold

* pre v3.0dev2: device, bin_img = **plantcv.otsu_auto_threshold**(*img, maxValue, object_type, device, debug=None*)
* post v3.0dev2: Deprecated, see:
    * bin_img = **plantcv.threshold.otsu**(*gray_img, max_value, object_type="light"*)

#### plantcv.output_mask

* pre v3.0dev2: device, maskpath, analysis_images = **plantcv.output_mask**(*device, img, mask, filename, outdir=None, mask_only=False, debug=None*)
* post v3.0dev2: imgpath, maskpath, analysis_images = **plantcv.output_mask**(*img, mask, filename, outdir=None, mask_only=False*)

#### plantcv.plot_hist

* pre v3.0dev2: bins, hist = **plantcv.plot_hist**(*img, name=False*)
* post v3.0dev2: bins, hist = **plantcv.plot_hist**(*img, name=False*)

#### plantcv.plot_image

* pre v3.0dev2: **plantcv.plot_image**(*img, cmap=None*)
* post v3.0dev2: **plantcv.plot_image**(*img, cmap=None*)

#### plantcv.print_image

* pre v3.0dev2: **plantcv.print_image**(*img, filename*)
* post v3.0dev2: **plantcv.print_image**(*img, filename*)

#### plantcv.readbayer

* pre v3.0: NA
* post v3.0: img, path, img_name = **plantcv.readbayer**(*filename, bayerpattern = 'BG', alg = 'default'*)

#### plantcv.readimage

* pre v3.0dev2: img, path, img_name = **plantcv.readimage**(*filename, debug=None*)
* post v3.0dev2: img, path, img_name = **plantcv.readimage**(*filename, mode="native"*)

#### plantcv.rectangle_mask

* pre v3.0dev2: device, img1, bnk, contour, hierarchy = **plantcv.rectangle_mask**(*img, p1, p2, device, debug=None, color="black"*)
* post v3.0dev2: img1, bnk, contour, hierarchy = **plantcv.rectangle_mask**(*img, p1, p2, color="black"*)

#### plantcv.report_size_marker_area

* pre v3.0dev2: device, marker_header, marker_data, analysis_images = **plantcv.report_size_marker_area**(*img, shape, device, debug, marker='define', x_adj=0, y_adj=0, w_adj=0, h_adj=0, base='white', objcolor='dark', thresh_channel=None, thresh=None, filename=False*)
* post v3.0dev2: marker_header, marker_data, analysis_images = **plantcv.report_size_marker_area**(*img, roi_contour, roi_hierarchy, marker='define', objcolor='dark', thresh_channel=None, thresh=None, filename=False*)

#### plantcv.resize

* pre v3.0dev2: device, reimg = **plantcv.resize**(*img, resize_x, resize_y, device, debug=None*)
* post v3.0dev2: reimg = **plantcv.resize**(*img, resize_x, resize_y*)

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

#### plantcv.roi.ellipse

* pre v3.0dev1: NA
* post v3.0dev2: roi_contour, roi_hierarchy = **plantcv.roi.ellipse**(*x, y, r1, r2, angle, img*)

#### plantcv.roi.from_binary_image

* pre v3.0dev1: NA
* post v3.0dev2: roi_contour, roi_hierarchy = **plantcv.roi.from_binary_image**(*bin_img, img*)

#### plantcv.roi.rectangle

* pre v3.0dev1: NA
* post v3.0dev2: roi_contour, roi_hierarchy = **plantcv.roi.rectangle**(*x, y, h, w, img*)

#### plantcv.roi_objects

* pre v3.0dev2: device, kept_cnt, hierarchy, mask, obj_area = **plantcv.roi_objects**(*img, roi_type, roi_contour, roi_hierarchy, object_contour, obj_hierarchy, device, debug=None*)
* post v3.0dev2: kept_cnt, hierarchy, mask, obj_area = **plantcv.roi_objects**(*img, roi_type, roi_contour, roi_hierarchy, object_contour, obj_hierarchy*)

#### plantcv.rotate

* pre v3.0dev2: device, rotated_img = **plantcv.rotate**(*img, rotation_deg, crop, device, debug=None*)
* post v3.0dev2: rotated_img = **plantcv.rotate**(*img, rotation_deg, crop*)

#### plantcv.rotate_img

* pre v3.0dev2: device, rotated_img = **plantcv.rotate_img**(*img, rotation_deg, device, debug=None*)
* post v3.0dev2: Deprecated, see:
    * rotated_img = **plantcv.rotate**(*img, rotation_deg, crop*)

#### plantcv.scale_features

* pre v3.0dev2: device, rescaled, centroid_scaled, boundary_line_scaled = **plantcv.scale_features**(*obj, mask, points, boundary_line, device, debug=None*)
* post v3.0dev2: rescaled, centroid_scaled, boundary_line_scaled = **plantcv.scale_features**(*obj, mask, points, boundary_line*)

#### plantcv.scharr_filter

* pre v3.0dev2: device, sr_img = **plantcv.scharr_filter**(*img, dX, dY, scale, device, debug=None*)
* post v3.0dev2: sr_img = **plantcv.scharr_filter**(*gray_img, dx, dy, scale*)

#### plantcv.shift_img

* pre v3.0dev2: device, adjusted_img = **plantcv.shift_img**(*img, device, number, side="right", debug=None*)
* post v3.0dev2: adjusted_img = **plantcv.shift_img**(*img, number, side="right"*)

#### plantcv.sobel_filter

* pre v3.0dev2: device, sb_img = **plantcv.sobel_filter**(*img, dx, dy, k, device, debug=None*)
* post v3.0dev2: sb_img = **plantcv.sobel_filter**(*gray_img, dx, dy, k*)

#### plantcv.threshold.binary

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = plantcv.threshold.binary**(*gray_img, threshold, max_value, object_type="light"*)

#### plantcv.threshold.gaussian

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = **plantcv.threshold.gaussian**(*gray_img, max_value, object_type="light"*)

#### plantcv.threshold.mean

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = **plantcv.threshold.mean**(*gray_img, max_value, object_type="light"*)

#### plantcv.threshold.otsu

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = **plantcv.threshold.otsu**(*gray_img, max_value, object_type="light"*)

#### plantcv.threshold.texture_filter

* pre v3.0: NA
* post v3.0: bin_img = **plantcv.threshold.texture_filter**(*gray_img, kernel, threshold, offset=3, texture_method='dissimilarity', borders='nearest', max_value=255*)

#### plantcv.threshold.triangle

* pre v3.0dev2: NA
* post v3.0dev2: bin_img = **plantcv.threshold.triangle**(*gray_img, max_value, object_type="light", xstep=1*)

#### plantcv.transform.apply_transformation_matrix

* pre v3.0dev1: NA
* post v3.0dev2: corrected_img = **plantcv.transform.apply_transformation_matrix**(*source_img, target_img, transformation_matrix*)

#### plantcv.transform.calc_transformation_matrix

* pre v3.0dev1: NA
* post v3.0dev2: determinant, transformation_matrix = **plantcv.transform.calc_transformation_matrix**(*matrix_m, matrix_b*)

#### plantcv.transform.correct_color

* pre v3.0dev1: NA
* post v3.0dev2: target_matrix, source_matrix, transformation_matrix, corrected_img = **plantcv.transform.correct_color**(*target_img, target_mask, source_img, source_mask, output_directory*)

#### plantcv.transform.create_color_card_mask

* pre v3.0: NA
* post v3.0: mask = **pcv.transform.create_color_card_mask**(*rgb_img, radius, start_coord, spacing, nrows, ncols, exclude=[]*)

#### plantcv.transform.find_color_card

* pre v3.0: NA
* post v3.0: df, start_coord, spacing = **plantcv.transofrm.find_color_card**(*rgb_img, threshold='adaptgauss', threshvalue=125, blurry=False, background='dark'*)

#### plantcv.transform.get_color_matrix

* pre v3.0dev1: NA
* post v3.0dev2: headers, color_matrix = **plantcv.transform.get_color_matrix**(*rgb_img, mask*)

#### plantcv.transform.get_matrix_m

* pre v3.0dev1: NA
* post v3.0dev2: matrix_a, matrix_m, matrix_b = **plantcv.transform.get_matrix_m**(*target_matrix, source_matrix*)

#### plantcv.transform.load_matrix

* pre v3.0dev1: NA
* post v3.0dev2: matrix = **plantcv.transform.load_matrix**(*filename*)

#### plantcv.transform.quick_color_check

* pre v3.0: NA
* post v3.0: **plantcv.transform.quick_color_check**(*target_matrix, source_matrix, num_chips*)

#### plantcv.transform.save_matrix

* pre v3.0dev1: NA
* post v3.0dev2: **plantcv.transform.save_matrix**(*matrix, filename*)

#### plantcv.triangle_auto_threshold

* pre v3.0dev2: device, bin_img = **plantcv.triangle_auto_threshold**(*device, img, maxvalue, object_type, xstep=1, debug=None*)
* post v3.0dev2: Deprecated, see:
    * bin_img = **plantcv.threshold.triangle**(*gray_img, max_value, object_type="light", xstep=1*)

#### plantcv.watershed_segmentation

* pre v3.0dev2: device, watershed_header, watershed_data, analysis_images = **plantcv.watershed_segmentation**(*device, img, mask, distance=10, filename=False, debug=None*)
* post v3.0dev2: watershed_header, watershed_data, analysis_images = **plantcv.watershed_segmentation**(*rgb_img, mask, distance=10, filename=False*)

#### plantcv.white_balance

* pre v3.0dev2: device, finalcorrected = **plantcv.white_balance**(*device, img, mode='hist',debug=None, roi=None*)
* post v3.0dev2: finalcorrected = **plantcv.white_balance**(*img, mode='hist', roi=None*)

#### plantcv.x_axis_pseudolandmarks

* pre v3.0dev2: device, top, bottom, center_v = **plantcv.x_axis_pseudolandmarks**(*obj, mask, img, device, debug=None*)
* post v3.0dev2: top, bottom, center_v = **plantcv.x_axis_pseudolandmarks**(*obj, mask, img*)

#### plantcv.y_axis_pseudolandmarks

* pre v3.0dev2: device, left, right, center_h = **plantcv.y_axis_pseudolandmarks**(*obj, mask, img, device, debug=None*)
* post v3.0dev2: left, right, center_h = **plantcv.y_axis_pseudolandmarks**(*obj, mask, img*)
