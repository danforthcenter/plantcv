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
is a set of data blocks of observational data or measurements. Observations contain samples. Each sample has the same 
set of information, roughly following the [MIAPPE](https://www.miappe.org/) guidelines: `trait` is the name of the 
observation, `method` is generally the PlantCV function name used (but it could be another method), `scale` is the 
observation units, `datatype` is the Python data type the data are stored as, `value` is the observation output 
value(s), and `label` is the data/category label. 

Example (abbreviated) JSON data:

```json
{
    "variables": {
        "camera": {
            "category": "metadata",
            "datatype": "<class 'str'>"
        },
        "imgtype": {
            "category": "metadata",
            "datatype": "<class 'str'>"
        },
        "timestamp": {
            "category": "metadata",
            "datatype": "<class 'str'>"
        },
        "plantbarcode": {
            "category": "metadata",
            "datatype": "<class 'str'>"
        },
        "treatment": {
            "category": "metadata",
            "datatype": "<class 'str'>"
        },
        "image": {
            "category": "metadata",
            "datatype": "<class 'str'>"
        },
        "area": {
            "category": "observations",
            "datatype": "<class 'int'>"
        },
        "convex_hull_area": {
            "category": "observations",
            "datatype": "<class 'list'>"
        }
    },
    "entities": [
        {
            "metadata": {
                "camera": {
                    "label": "camera identifier",
                    "datatype": "<class 'str'>",
                    "value": "SV"
                },
                "imgtype": {
                    "label": "image type",
                    "datatype": "<class 'str'>",
                    "value": "VIS"
                },
                "timestamp": {
                    "label": "datetime of image",
                    "datatype": "<class 'datetime.datetime'>",
                    "value": "2014-10-22 17:59:23.046"
                },
                "plantbarcode": {
                    "label": "plant barcode identifier",
                    "datatype": "<class 'str'>",
                    "value": "Ca002AA010557"
                },
                "treatment": {
                    "label": "treatment identifier",
                    "datatype": "<class 'str'>",
                    "value": "none"
                },
                "image": {
                    "label": "image file",
                    "datatype": "<class 'str'>",
                    "value": "./images/snapshot57393/VIS_SV_0_z1_h1_g0_e65_117881.png"
                }
            },
            "observations": {
                "sample1": {
                    "pixel_area": {
                        "trait": "area",
                        "method": "plantcv.plantcv.analyze.size",
                        "scale": "pixels",
                        "datatype": "<class 'int'>",
                        "value": 10000,
                        "label": "pixels"
                    },
                    "hull_area": {
                        "trait": "convex hull area",
                        "method": "plantcv.plantcv.analyze.size",
                        "scale": "pixels",
                        "datatype": "<class 'int'>",
                        "value": 100000,
                        "label": "pixels"
                    }
                }
            }
        }
    ]
}
```

Data in this structure can be converted to tables for downstream analysis using the provided script 
`plantcv-utils json2csv`, see [Accessory Tools](tools.md) for more details.

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


## Output Observations

Functions that automatically store data to the [`Outputs` class](outputs.md) are
[analyze.bound_horizontal](analyze_bound_horizontal2.md), 
[analyze.bound_vertical](analyze_bound_vertical2.md),
[analyze.color](analyze_color2.md),
[analyze.grayscale](analyze_grayscale.md),
[analyze.size](analyze_size.md),
[analyze.spectral_index](analyze_spectral_index.md),
[analyze.spectral_reflectance](analyze_spectral_reflectance.md),
[analyze.thermal](analyze_thermal.md),
[analyze.yii](analyze_yii.md), 
[analyze.npq](analyze_npq.md),
[homology.landmark_reference_pt_dist](homology_landmark_reference_pt_dist.md),
[homology.x_axis_pseudolandmarks](homology_x_axis_pseudolandmarks.md), 
[homology.y_axis_pseudolandmarks](homology_y_axis_pseudolandmarks.md),
[morphology.check_cycles](check_cycles.md),
[morphology.fill_segments](fill_segments.md), 
[morphology.find_tips](find_tips.md),
[morphology.find_branch_pts](find_branch_pts.md), 
[morphology.segment_angle](segment_angle.md),
[morphology.segment_curvature](segment_curvature.md), 
[morphology.segment_euclidean_length](segment_euclidean_length.md),
[morphology.segment_insertion_angle](segment_insertion_angle.md), 
[morphology.segment_path_length](segment_pathlength.md),
[morphology.segment_tangent_angle](segment_tangent_angle.md),
[report_size_marker_area](report_size_marker.md),
[transform.find_color_card](find_color_card.md),
[watershed_segmentation](watershed.md), and
[within_frame](within_frame.md)

All of these functions include an optional `label` parameter 
that allows users to append custom prefixes to the unique variable identifier. 

For more detail about the traits measured by each function see the
[Observation Traits Summary Table](https://docs.google.com/spreadsheets/d/1gk5VocBA-63gyF_vA6yPNvWreZ1R7-_z4vOfm37YBl8/edit?usp=sharing).
