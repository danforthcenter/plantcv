## Train the Gaussian Mixture Model to segment image by color.

Trains the Gaussian Mixture Model used to classify pictures based on color.

**plantcv.learn.gmm_clustering_train**(*img, remove, num_components, project_name*)

**returns** none

- **Parameters:**
    - img - RGB image data to train the Gaussian Mixture Model.  This can be either a single image or a comma-delimited list of image data.
    - remove - List of colors to remove from the training data set.  This is useful for removing a white or black background.
    - num_components - The number of components you into which you wish to divide the mask.
    - project_name - This name is prepended to the output Gaussian Mixture Model file.  This tells the Segmentation function which Gaussian Mixture Model file to use.

- **Context:**
    - This function segment an image by color.  You must choose the number of colors by which you wish to cluster your image.

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/learn/color_clustering_train.py)