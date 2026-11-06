# PlantCV test data

Most test inputs are generated at test time by `tests/synthetic.py` and exposed through the fixtures in
`tests/conftest.py`. Generated data is small, has expected values that can be derived by hand, and does
not need to be stored in the repository. Use it for new tests.

This directory holds only the files that cannot reasonably be generated. Each one is listed below with
the reason it is kept. Add a file here only when the test depends on something a generator cannot
produce, such as a real container or vendor format, and add it to this list in the same pull request.

## Real file formats

Readers are tested against files written by the real software or device.

| File | Used by | Why it is kept |
|---|---|---|
| `test_nd2_img.nd2` | `test_readimage.py` | Nikon ND2 container. |
| `FLIR_test.jpg` | `test_readimage.py` | FLIR radiometric JPEG read with `flyr`; the thermal data sits in FLIR-specific metadata segments inside the JPEG. |

## Templates for generated data

Generators in `tests/synthetic.py` copy these headers and write small synthetic data alongside them.

| File | Used by | Why it is kept |
|---|---|---|
| `cropreporter_v441/PSII_HDR_020321_WT_TOP_1.INF` | `synthetic.write_cropreporter` | Real CropReporter header for PSD, PSL, NPQ, CHL, CLR and SPC. Also referenced by `docs/photosynthesis_read_cropreporter.md`. |
| `cropreporter_v653/HDR_dark_light.INF` | `synthetic.write_cropreporter` | Real CropReporter header for PMD and PML. |
| `cropreporter_gfp/HDR_DYSeed_20251222191634684.INF` | `synthetic.write_cropreporter` | Real CropReporter header for GFP and RFP. |
| `cropreporter_aph/HDR_2025-12-12_tob1_20251212205712029.INF` | `synthetic.write_cropreporter` | Real CropReporter header for APH. |
| `cropreporter_pmt/HDR_E0001P0007N0001_GCU24100090_20260226.INF` | `synthetic.write_cropreporter` | Real CropReporter header for PMT. |
| `SnapshotInfo.csv` | `synthetic.write_image_dir("snapshot")` | LemnaTec snapshot metadata table read by the `parallel` snapshot parser. |
| `phenodata_metadata.json` | `synthetic.write_image_dir("phenodata")` | Written as `metadata.json`, the file that marks a `parallel` phenodata dataset. |

## Results and configuration specimens

Small text files that pin the on-disk formats PlantCV reads and writes.

| File | Used by | Why it is kept |
|---|---|---|
| `outputs_results.json`, `outputs_results.csv` | `test_outputs.py` | Expected `Outputs` JSON input and CSV output. |
| `plantcv_results.json` | `test_json2csv.py` | Multi-sample results file converted by `json2csv`. |
| `invalid_results.json` | `test_json2csv.py` | Valid JSON that is not a PlantCV results file. |
| `valid.json` | `test_process_results.py` | Valid results JSON without the keys `process_results` appends to. |
| `parallel_results/_PCV_PARALLEL_CHECKPOINT_/VIS_SV_0_z1_h1_g0_e82_117770.jpg.txt` | `test_process_results.py` | Per-image result file as written by a workflow during `run_parallel`. |
| `new_results.json`, `appended_results.json` | `test_process_results.py`, `parallel/test_cli.py` | Expected output after processing the result above once and twice. |
| `workflowconfig_template.json` | `parallel/` tests | Expected `WorkflowConfig.save_config` output. |
| `plantcv-script.py` | `parallel/` tests | Minimal workflow script run by `parallel`. |
| `dummy.ipynb` | `parallel/test_jupyterconfig.py` | Notebook converted by `JupyterConfig.notebook2script`. |

## Learn inputs

| File | Used by | Why it is kept |
|---|---|---|
| `pixel_inspector_rgb_values.txt` | `learn/test_naive_bayes.py`, `learn/test_cli.py` | ImageJ Pixel Inspector export read by `learn.naive_bayes_multiclass`. |
| `rgb_values_table.txt` | `learn/test_naive_bayes.py`, `learn/test_cli.py` | Tab-delimited class table of RGB samples. |
| `rgb_values_table_bad.txt` | `learn/test_naive_bayes.py` | Class table with duplicate and empty columns, for the error paths. |

## Homology inputs

| File | Used by | Why it is kept |
|---|---|---|
| `plms_df.csv` | `homology/test_space.py` | Pseudolandmark table read by `homology.space`. |
| `plms_space_df.csv` | `homology/test_starscape.py`, `homology/test_constella.py` | `homology.space` output. |
| `plms_starscape_df.csv` | `homology/test_constella.py` | `homology.starscape` output. |
| `plms_landmarks.csv`, `plms_annotated.csv` | `homology/test_constellaqc.py` | Landmark tables and their annotations. |
