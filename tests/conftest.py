import pytest
import os
import numpy as np
import matplotlib

# Disable plotting
matplotlib.use('Template')


@pytest.fixture(scope="session")
def test_data():
    # Test input data directory
    datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    # WorkflowConfig saved template dictionary
    workflowconfig_template = {
        "input_dir": "",
        "json": "",
        "filename_metadata": [],
        "workflow": "",
        "img_outdir": "./output_images",
        "tmp_dir": None,
        "start_date": None,
        "end_date": None,
        "imgformat": "png",
        "delimiter": "_",
        "metadata_filters": {},
        "timestampformat": "%Y-%m-%d %H:%M:%S.%f",
        "writeimg": False,
        "other_args": [],
        "coprocess": None,
        "cleanup": True,
        "append": True,
        "cluster": "LocalCluster",
        "cluster_config": {
            "n_workers": 1,
            "cores": 1,
            "memory": "1GB",
            "disk": "1GB",
            "log_directory": None,
            "local_directory": None,
            "job_extra": None
        },
        "metadata_terms": {
            "camera": {
                "label": "camera identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "imgtype": {
                "label": "image type",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "zoom": {
                "label": "camera zoom setting",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "exposure": {
                "label": "camera exposure setting",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "gain": {
                "label": "camera gain setting",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "frame": {
                "label": "image series frame identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "lifter": {
                "label": "imaging platform height setting",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "timestamp": {
                "label": "datetime of image",
                "datatype": "<class 'datetime.datetime'>",
                "value": None
            },
            "id": {
                "label": "image identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "plantbarcode": {
                "label": "plant barcode identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "treatment": {
                "label": "treatment identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "cartag": {
                "label": "plant carrier identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "measurementlabel": {
                "label": "experiment identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "other": {
                "label": "other identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            }
        }
    }
    # Metadata result for VIS only data
    metadata_vis_only = {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(datadir, 'snapshots', 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
            'camera': 'SV',
            'imgtype': 'VIS',
            'zoom': 'z1',
            'exposure': 'e82',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117770',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none'
        }
    }
    # Metadata result for NIR only data
    metadata_nir_only = {
        'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
            'path': os.path.join(datadir, 'snapshots', 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
            'camera': 'SV',
            'imgtype': 'NIR',
            'zoom': 'z1',
            'exposure': 'e65',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117779',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none'
        }
    }
    # Metadata result for VIS and NIR coprocessed data
    metadata_coprocess = {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(datadir, 'snapshots', 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
            'camera': 'SV',
            'imgtype': 'VIS',
            'zoom': 'z1',
            'exposure': 'e82',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117770',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none',
            'coimg': 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'
        },
        'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
            'path': os.path.join(datadir, 'snapshots', 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
            'camera': 'SV',
            'imgtype': 'NIR',
            'zoom': 'z1',
            'exposure': 'e65',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117779',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none'
        }
    }
    # Read contours from saved NumPy array
    setaria_small_mask_contours_npz = np.load(os.path.join(datadir, "setaria_composed_contours.npz"), encoding="latin1")
    setaria_small_mask_contours = setaria_small_mask_contours_npz['arr_0']
    input_contours_npz = np.load(os.path.join(datadir, "input_contours.npz"), encoding="latin1")
    input_object_contours = input_contours_npz['arr_0']
    setaria_small_plant_composed_contours_npz = np.load(os.path.join(datadir,
                                                                     "setaria_small_plant_composed_contours.npz"),
                                                        encoding="latin1")
    setaria_small_plant_composed_contours = setaria_small_plant_composed_contours_npz["arr_0"]
    return {
        "color_img": os.path.join(datadir, "input_color_img.jpg"),
        "workflowconfig_template": workflowconfig_template,
        "workflowconfig_template_file": os.path.join(datadir, "workflow_config_template.json"),
        "img_flatdir": os.path.join(datadir, "images"),
        "img_flatdir_wdates": os.path.join(datadir, "images_w_date"),
        "img_snapshotdir": os.path.join(datadir, "snapshots"),
        "workflow_script": os.path.join(datadir, "plantcv-script.py"),
        "metadata_vis_only": metadata_vis_only,
        "metadata_nir_only": metadata_nir_only,
        "metadata_coprocess": metadata_coprocess,
        "parallel_results_dir": os.path.join(datadir, "results"),
        "parallel_bad_results_dir": os.path.join(datadir, "bad_results"),
        "appended_results_file": os.path.join(datadir, "appended_results.json"),
        "new_results_file": os.path.join(datadir, "new_result.json"),
        "valid_json_file": os.path.join(datadir, "valid.json"),
        "setaria_small_vis": os.path.join(datadir, "setaria_small_vis.png"),
        "setaria_small_mask": os.path.join(datadir, "setaria_small_mask.png"),
        "setaria_small_mask_contours": setaria_small_mask_contours,
        "acute_vertex_result": np.asarray([[[119, 285]], [[151, 280]], [[168, 267]], [[168, 262]], [[171, 261]],
                                           [[224, 269]], [[246, 271]], [[260, 277]], [[141, 248]], [[183, 194]],
                                           [[188, 237]], [[173, 240]], [[186, 260]], [[147, 244]], [[163, 246]],
                                           [[173, 268]], [[170, 272]], [[151, 320]], [[195, 289]], [[228, 272]],
                                           [[210, 272]], [[209, 247]], [[210, 232]]]),
        "input_color_img": os.path.join(datadir, "input_color_img.jpg"),
        "input_binary_img": os.path.join(datadir, "input_binary_img.png"),
        "input_object_contours": input_object_contours,
        "input_gray_img": os.path.join(datadir, "input_gray_img.jpg"),
        "setaria_small_plant_vis": os.path.join(datadir, "setaria_small_plant_vis.png"),
        "setaria_small_plant_mask": os.path.join(datadir, "setaria_small_plant_mask.png"),
        "setaria_small_plant_composed_contours": setaria_small_plant_composed_contours
    }
