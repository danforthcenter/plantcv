## Train the Gaussian Mixture Model or Mini-Batch Kmeans to segment image by color.

Trains the Gaussian Mixture Model or Mini-Batch Kmeans used to classify pictures based on color.

**plantcv.learn.color_clustering_train**(*img, remove, num_components, project_name, remove_grays, sample_pixels, sample_pixel_file*)

**returns** none

- **Parameters:**
    - img - RGB image data to train the Gaussian Mixture Model or Mini-Batch Kmeans.  This can be either a single image or a comma-delimited list of image data.
    - remove - List of colors to remove from the training data set.  This is useful for removing a white or black background.
    - num_components - The number of binary masks into which you wish to divide the RGB image.
    - project_name - This name is prepended to the output Gaussian Mixture Model file as well as any other file output by this function.  This tells the Segmentation function which Gaussian Mixture Model file to use.
    - remove_grays - A boolean.  If True, then pixels in which the r,g, and b are removed before segmentation.  Default is False.
    - algorithm - Either "Gaussian" or "Kmeans."  Choose which algorithm to use to segment the image based on color.  Mini-Batch Kmeans is faster than Gaussian Mixture Model, but Gaussian Mixture Model is more sensitive and can cluster different "shades" of the same color. 
    - sample_pixels - How many pixels are output per binary mask.  It can take the following values: 
                    - an integer value: which will output pixels in the order they were assigned to a group.  The number of pixels is determined by the integer value.
                    - "n most": The 'n' most pixel values are output.
                    - "n least": The 'n' least pixel values are output.
                    - "n random": 'n' random pixel values are output.
    - sample_pixel_file - The file to which sample pixels are output.  




- **Context:**
    - This function segment an image by color.  You must choose the number of colors by which you wish to cluster your image.

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/learn/color_clustering_train.py)