## Sample Images

Samples a subset of images to separate sections of a dataset or create a testing split.

**plantcv.parallel.sample_images**(*source, dest_path="./sampled_images", num=100*)

**returns** None

- **Parameters:**
    - source  - Path to image directory as a string, path to a [`WorkflowConfig`](parallel_config.md) json file, or a `WorkflowConfig` object. A `WorkflowConfig` object/json file will only sample from images that the workflow would select.
	- dest_path - Path to write images to, note that the original subdirectory structure will be preserved.
	- num - Number of images to sample, defaults to 100.

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/sample_images.py)

!!! note
    Sampling from a directory instead of from a configuration file makes some assumptions. If there is a `SnapshotInfo.csv` file then data is assumed to be from a Phenofront system. If there is a `metadata.json` file then a Phenodata system is assumed. Otherwise images are randomly sampled from all files with a recognized image extension ('bmp', 'dib', 'jpeg', 'jpg', 'jpe', 'jp2', 'png', 'ppm', 'pgm', 'ppm', 'sr', 'ras', 'tiff', or 'tif'). In general, sampling using a configuration file file is more useful as it will only sample from images that your workflow would run on.
