## Organization of PlantCV Outputs

During [parallel processing](pipeline_parallel.md), outputs from PlantCV analysis functions are collected into a 
hierarchical JSON output file. The JSON file is used to collect image metadata and PlantCV output observations for the
entire image set. The hierarchical data structure is more flexible than the previous tabular structure: entities 
(typically individual images) do not need to have a rigid set of observations, and users can easily record custom 
observations without the need to update a database schema.

### Data Structure

The JSON output file has two top-level sections: `variables` is a collection of all observation names found in the
dataset, and `entities` is a list of data blocks for each unit of analysis (typically an image, or a sub-region of an
image) in the dataset. For each entity there are two data blocks: `metadata` is a set of key-value pairs of metadata
keywords and their values (e.g. image or experimental metadata such as timestamp, treatment, etc.), and `observations`
is a set of data blocks of observational data or measurements. Each observation has the same set of information,
roughly following the MIAPPE guidelines: `trait` is the name of the observation, `method` is generally the PlantCV
function name used (but it could be another method), `scale` is the observation units, `datatype` is the Python data
type the data are stored as, `value` is the observation output value(s), and `label` is the data/category label. 

Example (abbreviated) JSON data:

```json
{
    "variables": {
        "image": 1,
        "camera": 1,
        "imgtype": 1,
        "zoom": 1,
        "exposure": 1,
        "gain": 1,
        "frame": 1,
        "lifter": 1,
        "timestamp": 1,
        "id": 1,
        "plantbarcode": 1,
        "treatment": 1,
        "cartag": 1,
        "measurementlabel": 1,
        "other": 1,
        "pixel_area": 1
    },
    "entities": [
        {
            "metadata": {
                "image": "./images/snapshot57393/VIS_SV_90_z1_h1_g0_e82_117872.png",
                "camera": "SV",
                "imgtype": "VIS",
                "zoom": "z1",
                "exposure": "e82",
                "gain": "g0",
                "frame": "90",
                "lifter": "h1",
                "timestamp": "2014-10-22 17:59:23.046",
                "id": "117872",
                "plantbarcode": "Ca002AA010557",
                "treatment": "none",
                "cartag": "1663",
                "measurementlabel": "C002ch_092214_biomass",
                "other": "none"
            },
            "observations": {
                "pixel_area": {
                    "trait": "area",
                    "method": "plantcv.plantcv.analyze_object",
                    "scale": "pixels",
                    "datatype": "<class 'int'>",
                    "value": 10000,
                    "label": "pixels"
                },
                "hull_area": {
                    "trait": "convex hull area",
                    "method": "plantcv.plantcv.analyze_object",
                    "scale": "pixels",
                    "datatype": "<class 'int'>",
                    "value": 100000,
                    "label": "pixels"
                }
            }
        }
    ]
}
```

## Summary of Output Metadata

Below is a list of currently tracked metadata types in PlantCV. None of these are strictly required. If you have 
suggestions for additional metadata we should track that would be useful to you, please submit an 
[issue](https://github.com/danforthcenter/plantcv/issues) or contact us. Ideally, we will be able to handle the full
[MIAPPE](https://www.miappe.org/) specification at some point.

| Name             | Description                                           |
| ---------------- | ----------------------------------------------------- |
| plantbarcode     | plant (specimin) identifier, name, or code            |
| timestamp        | date and time the image was acquired                  |
| treatment        | treatment name or ID                                  |
| camera           | camera name or ID                                     |
| imgtype          | type of image (e.g. RGB, VIS, NIR, etc.)              |
| zoom             | camera optical or digital zoom setting                |
| exposure         | camera exposure setting                               |
| gain             | camera gain setting                                   |
| frame            | frame name or ID in a multi-frame series              |
| lifter           | position if a variable height lifting system was used |
| id               | image ID or other arbitrary ID                        |
| cartag           | carrier or pot ID                                     |
| measurementlabel | experiment name or ID                                 |
| other            | other information                                     |

## Summary of Output Observations

| Variable                      | Trait                                             | Method                                                             | Scale     | Data Type | Description                                                                                                                                             |
| ----------------------------- | ------------------------------------------------- | ------------------------------------------------------------------ | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tip_coordinates               | tip coordinates                                   | [acute_vertex](acute_vertex.md)                                    | none      | list      | list of positions ([PATO:0000140](http://purl.obolibrary.org/obo/PATO_0000140)) of tip points                                                           |
| red_frequencies               | red frequencies                                   | [analyze_color](analyze_color.md)                                  | frequency | list      | red ([PATO:0000322](http://purl.obolibrary.org/obo/PATO_0000322)) intensity frequency distribution (values of 0-255 in RGB colorspace)                  |
| green_frequencies             | green frequencies                                 | [analyze_color](analyze_color.md)                                  | frequency | list      | green ([PATO:0000320](http://purl.obolibrary.org/obo/PATO_0000320)) intensity frequency distribution (values of 0-255 in RGB colorspace)                |
| blue_frequencies              | blue frequencies                                  | [analyze_color](analyze_color.md)                                  | frequency | list      | blue ([PATO:0000318](http://purl.obolibrary.org/obo/PATO_0000318)) intensity frequency distribution (values of 0-255 in RGB colorspace)                 |
| lightness_frequencies         | lightness frequencies                             | [analyze_color](analyze_color.md)                                  | frequency | list      | lightness ([PATO:0000016](http://purl.obolibrary.org/obo/PATO_0000016)) frequency distribution (values of 0-100% in LAB colorspace)                     |
| green-magenta_frequencies     | green-magenta frequencies                         | [analyze_color](analyze_color.md)                                  | frequency | list      | green-magenta component frequency distribution (values of -127 to 128 in LAB colorspace)                                                                |
| blue-yellow_frequencies       | blue-yellow frequencies                           | [analyze_color](analyze_color.md)                                  | frequency | list      | blue-yellow component frequency distribution (values of -127 to 128 in LAB colorspace)                                                                  |
| hue_frequencies               | hue frequencies                                   | [analyze_color](analyze_color.md)                                  | frequency | list      | hue ([PATO:0000015](http://purl.obolibrary.org/obo/PATO_0000015)) frequency distribution (values of 0-359 degrees in HSV colorspace)                    |
| saturation_frequencies        | saturation frequencies                            | [analyze_color](analyze_color.md)                                  | frequency | list      | saturation ([PATO:0000017](http://purl.obolibrary.org/obo/PATO_0000017)) frequency distribution (values of 0-100% in HSV colorspace)                    |
| value_frequencies             | value frequencies                                 | [analyze_color](analyze_color.md)                                  | frequency | list      | value ([PATO:0000016](http://purl.obolibrary.org/obo/PATO_0000016)) frequency distribution (values of 0-100% in HSV colorspace)                         |
| hue_circular_mean             | hue circular mean                                 | [analyze_color](analyze_color.md)                                  | degrees   | float     | [circular mean](https://en.wikipedia.org/wiki/Mean_of_circular_quantities) of hue values                                                                |
| hue_circular_std              | hue circular standard deviation                   | [analyze_color](analyze_color.md)                                  | degrees   | float     | [circular standard deviation](https://en.wikipedia.org/wiki/Directional_statistics) of hue values                                                       |
| hue_median                    | hue median                                        | [analyze_color](analyze_color.md)                                  | degrees   | float     | median ([NCIT:C28007](http://purl.obolibrary.org/obo/NCIT_C28007)) of hue values                                                                        |
| horizontal_reference_position | horizontal reference position                     | [analyze_bound_horizontal](analyze_bound_horizontal.md)            | none      | int       | position ([PATO:0000140](http://purl.obolibrary.org/obo/PATO_0000140)) of horizontal reference point                                                    |
| height_above_reference        | height above reference                            | [analyze_bound_horizontal](analyze_bound_horizontal.md)            | pixels    | int       | height ([PATO:0000119](http://purl.obolibrary.org/obo/PATO_0000119)) of object above reference position                                                 |
| height_below_reference        | height below reference                            | [analyze_bound_horizontal](analyze_bound_horizontal.md)            | pixels    | int       | height ([PATO:0000119](http://purl.obolibrary.org/obo/PATO_0000119)) of object below reference position                                                 |
| area_above_reference          | area above reference                              | [analyze_bound_horizontal](analyze_bound_horizontal.md)            | pixels    | int       | area ([PATO:0001323](http://purl.obolibrary.org/obo/PATO_0001323)) of object above reference position                                                   |
| area_below_reference          | area below reference                              | [analyze_bound_horizontal](analyze_bound_horizontal.md)            | pixels    | int       | area ([PATO:0001323](http://purl.obolibrary.org/obo/PATO_0001323)) of object below reference position                                                   |
| percent_area_above_reference  | percent area above reference                      | [analyze_bound_horizontal](analyze_bound_horizontal.md)            | percent   | float     | proportion ([PATO:0001470](http://purl.obolibrary.org/obo/PATO_0001470)) of object area above reference position                                        |
| percent_area_below_reference  | percent area below reference                      | [analyze_bound_horizontal](analyze_bound_horizontal.md)            | percent   | float     | proportion ([PATO:0001470](http://purl.obolibrary.org/obo/PATO_0001470)) of object area below reference position                                        |
| vertical_reference_position   | vertical reference position                       | [analyze_bound_vertical](analyze_bound_vertical.md)                | none      | int       | position ([PATO:0000140](http://purl.obolibrary.org/obo/PATO_0000140)) of vertical reference point                                                      |
| width_left_reference          | width left of reference                           | [analyze_bound_vertical](analyze_bound_vertical.md)                | pixels    | int       | width ([PATO:0000921](http://purl.obolibrary.org/obo/PATO_0000921)) of object left of reference position                                                |
| width_right_reference         | height below of reference                         | [analyze_bound_vertical](analyze_bound_vertical.md)                | pixels    | int       | width ([PATO:0000921](http://purl.obolibrary.org/obo/PATO_0000921)) of object right of reference position                                               |
| area_left_reference           | area left of reference                            | [analyze_bound_vertical](analyze_bound_vertical.md)                | pixels    | int       | area ([PATO:0001323](http://purl.obolibrary.org/obo/PATO_0001323)) of object left of reference position                                                 |
| area_right_reference          | area right of reference                           | [analyze_bound_vertical](analyze_bound_vertical.md)                | pixels    | int       | area ([PATO:0001323](http://purl.obolibrary.org/obo/PATO_0001323)) of object right of reference position                                                |
| percent_area_left_reference   | percent area left of reference                    | [analyze_bound_vertical](analyze_bound_vertical.md)                | percent   | float     | proportion ([PATO:0001470](http://purl.obolibrary.org/obo/PATO_0001470)) of object area left of reference position                                      |
| percent_area_right_reference  | percent area right of reference                   | [analyze_bound_vertical](analyze_bound_vertical.md)                | percent   | float     | proportion ([PATO:0001470](http://purl.obolibrary.org/obo/PATO_0001470)) of object area right of reference position                                     |
| nir_frequencies               | near-infrared frequencies                         | [analyze_nir_intensity](analyze_NIR_intensity)                     | frequency | list      | near-infrared intensity frequency distribution (values in 8- or 16-bit sensor detection range)                                                          |
| area                          | area                                              | [analyze_object](analyze_shape.md)                                 | pixels    | int       | area ([PATO:0001323](http://purl.obolibrary.org/obo/PATO_0001323)) of object                                                                            | 
| convex_hull_area              | convex hull area                                  | [analyze_object](analyze_shape.md)                                 | pixels    | int       | area ([PATO:0001323](http://purl.obolibrary.org/obo/PATO_0001323)) of convex hull                                                                       |
| solidity                      | solidity                                          | [analyze_object](analyze_shape.md)                                 | none      | float     | ratio ([PATO:0001470](http://purl.obolibrary.org/obo/PATO_0001470)): area / convex hull area                                                            |
| perimeter                     | perimeter                                         | [analyze_object](analyze_shape.md)                                 | pixels    | int       | perimeter ([PATO:0001711](http://purl.obolibrary.org/obo/PATO_0001711)) around object                                                                   |
| width                         | width                                             | [analyze_object](analyze_shape.md)                                 | pixels    | int       | width ([PATO:0000921](http://purl.obolibrary.org/obo/PATO_0000921)) of object                                                                           | 
| height                        | height                                            | [analyze_object](analyze_shape.md)                                 | pixels    | int       | height ([PATO:0000119](http://purl.obolibrary.org/obo/PATO_0000119)) of object                                                                          |
| longest_path                  | longest path                                      | [analyze_object](analyze_shape.md)                                 | pixels    | int       | length ([PATO:0000122](http://purl.obolibrary.org/obo/PATO_0000122)) of longest path between convex hull vertices through the center of mass            |
| center_of_mass                | center of mass                                    | [analyze_object](analyze_shape.md)                                 | none      | tuple     | position ([PATO:0000140](http://purl.obolibrary.org/obo/PATO_0000140)) of center of mass                                                                |
| convex_hull_vertices          | convex hull vertices                              | [analyze_object](analyze_shape.md)                                 | none      | int       | number ([PATO:0001555](http://purl.obolibrary.org/obo/PATO_0001555)) of convex hull vertices                                                            |
| object_in_frame               | object in frame                                   | [analyze_object](analyze_shape.md)                                 | none      | bool      | true of false (false if the object is touching the border of the image)                                                                                 |
| ellipse_center                | ellipse center                                    | [analyze_object](analyze_shape.md)                                 | none      | tuple     | position ([PATO:0000140](http://purl.obolibrary.org/obo/PATO_0000140)) of the center of the minimum bounding ellipse                                    |
| ellipse_major_axis            | ellipse major axis length                         | [analyze_object](analyze_shape.md)                                 | pixels    | int       | length ([PATO:0000122](http://purl.obolibrary.org/obo/PATO_0000122)) of the major axis of the minimum bounding ellipse                                  |
| ellipse_minor_axis            | ellipse minor axis length                         | [analyze_object](analyze_shape.md)                                 | pixels    | int       | length ([PATO:0000122](http://purl.obolibrary.org/obo/PATO_0000122)) of the minor axis of the minimum bounding ellipse                                  |
| ellipse_angle                 | ellipse major axis angle                          | [analyze_object](analyze_shape.md)                                 | degrees   | float     | angle ([PATO:0002326](http://purl.obolibrary.org/obo/PATO_0002326)) of rotation of the bounding ellipse major axis                                      |
| ellipse_eccentricity          | ellipse eccentricity                              | [analyze_object](analyze_shape.md)                                 | none      | float     | [eccentricity](https://en.wikipedia.org/wiki/Eccentricity_(mathematics)#Ellipses) of the bounding ellipse                                               |
| vert_ave_c                    | average vertical distance from centroid           | [landmark_reference_pt_dist](landmark_reference_pt_dist.md)        | pixels    | float     | average vertical distance from centroid                                                                                                                 |
| hori_ave_c                    | average horizontal distance from centeroid        | [landmark_reference_pt_dist](landmark_reference_pt_dist.md)        | pixels    | float     | average horizontal distance from centeroid                                                                                                              |
| euc_ave_c                     | average euclidean distance from centroid          | [landmark_reference_pt_dist](landmark_reference_pt_dist.md)        | pixels    | float     | average euclidean distance from centroid                                                                                                                |
| ang_ave_c                     | average angle between landmark point and centroid | [landmark_reference_pt_dist](landmark_reference_pt_dist.md)        | degrees   | float     | average angle between landmark point and centroid                                                                                                       |
| vert_ave_b                    | average vertical distance from baseline           | [landmark_reference_pt_dist](landmark_reference_pt_dist.md)        | pixels    | float     | average vertical distance from baseline                                                                                                                 |
| hori_ave_b                    | average horizontal distance from baseline         | [landmark_reference_pt_dist](landmark_reference_pt_dist.md)        | pixels    | float     | average horizontal distance from baseline                                                                                                               |
| euc_ave_b                     | average euclidean distance from baseline          | [landmark_reference_pt_dist](landmark_reference_pt_dist.md)        | pixels    | float     | average euclidean distance from baseline                                                                                                                |
| ang_ave_b                     | average angle between landmark point and baseline | [landmark_reference_pt_dist](landmark_reference_pt_dist.md)        | degrees   | float     | average angle between landmark point and baseline                                                                                                       |
| num_cycles                    | number of cycles                                  | [morphology.check_cycles](check_cycles.md)                         | none      | int       | number ([PATO:0001555](http://purl.obolibrary.org/obo/PATO_0001555)) of closed loops (cycles) in a skeletonized object                                  |
| segment_angle                 | segment angle                                     | [morphology.segment_angle](segment_angle.md)                       | degrees   | list      | list of angles ([PATO:0002326](http://purl.obolibrary.org/obo/PATO_0002326)) of segment paths found by fitting a linear regression line to each segment |
| segment_curvature             | segment curvature                                 | [morphology.segment_curvature](segment_curvature.md)               | none      | list      | list of curvatures (the ratio between geodesic and euclidean distance) of segment paths                                                                 |
| segment_eu_length             | segment euclidean length                          | [morphology.segment_euclidean_length](segment_euclidean_length.md) | pixels    | list      | list of Euclidean Distance Measurements ([NCIT:C65170](http://purl.obolibrary.org/obo/NCIT_C65170)) between segment endpoints                           |
| segment_insertion_angle       | segment insertion angle                           | [morphology.segment_insertion_angle](segment_insertion_angle.md)   | degrees   | list      | list of angles ([PATO:0002326](http://purl.obolibrary.org/obo/PATO_0002326)) between "leaf" and "stem" segments                                         |
| segment_path_length           | segment path length                               | [morphology.segment_path_length](segment_pathlength.md)            | pixels    | list      | list of lengths ([PATO:0000122](http://purl.obolibrary.org/obo/PATO_0000122)) along each segment path                                                   |
| segment_tangent_angle         | segment tangent angle                             | [morphology.segment_tangent_angle](segment_tangent_angle.md)       | degrees   | list      | list of angles ([PATO:0002326](http://purl.obolibrary.org/obo/PATO_0002326)) between the tangents to the ends of each segment                           |
| marker_area                   | marker area                                       | [report_size_marker_area](report_size_marker.md)                   | pixels    | int       | area ([PATO:0001323](http://purl.obolibrary.org/obo/PATO_0001323)) of a size marker object                                                              |
| marker_ellipse_major_axis     | marker ellipse major axis length                  | [report_size_marker_area](report_size_marker.md)                   | pixels    | int       | length ([PATO:0000122](http://purl.obolibrary.org/obo/PATO_0000122)) of the major axis of the minimum bounding ellipse of a size marker                 |
| marker_ellipse_minor_axis     | marker ellipse minor axis length                  | [report_size_marker_area](report_size_marker.md)                   | pixels    | int       | length ([PATO:0000122](http://purl.obolibrary.org/obo/PATO_0000122)) of the minor axis of the minimum bounding ellipse of a size marker                 |
| marker_ellipse_eccentricity   | marker ellipse eccentricity                       | [report_size_marker_area](report_size_marker.md)                   | none      | float     | [eccentricity](https://en.wikipedia.org/wiki/Eccentricity_(mathematics)#Ellipses) of the bounding ellipse of a size marker                              |
| estimated_object_count        | estimated object count                            | [watershed_segmentation](watershed.md)                             | none      | int       | number ([PATO:0001555](http://purl.obolibrary.org/obo/PATO_0001555)) of segmented objects (e.g. leaves)                                                 |
| top_lmk                       | top landmark coordinates                          | [x_axis_pseudolandmarks](x_axis_pseudolandmarks.md)                | none      | list      | list of landmark points within 'top' portion                                                                                                            |
| bottom_lmk                    | bottom landmark coordinates                       | [x_axis_pseudolandmarks](x_axis_pseudolandmarks.md)                | none      | list      | list of landmark points within 'bottom' portion                                                                                                         |
| center_v_lmk                  | center vertical landmark coordinates              | [x_axis_pseudolandmarks](x_axis_pseudolandmarks.md)                | none      | list      | list of landmark points within 'center-vertical' portion                                                                                                |
| left_lmk                      | left landmark coordinates                         | [y_axis_pseudolandmarks](y_axis_pseudolandmarks.md)                | none      | list      | list of landmark points within 'left' portion                                                                                                           |
| right_lmk                     | right landmark coordinates                        | [y_axis_pseudolandmarks](y_axis_pseudolandmarks.md)                | none      | list      | list of landmark points within 'right' portion                                                                                                          |
| center_h_lmk                  | center horizontal landmark coordinates            | [y_axis_pseudolandmarks](y_axis_pseudolandmarks.md)                | none      | list      | list of landmark points within 'center-horizontal' portion                                                                                              |
