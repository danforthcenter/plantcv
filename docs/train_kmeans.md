## Kmeans clustering training 

This function takes in a collection of training images and fits a patch-based kmeans cluster model for later use in classifying cluster assignment in a target image. The target and training images may be in grayscale, RGB, or multispectral image format.


**plantcv.learn.train_kmeans**(img_dir, k, out_path="./kmeansout.fit", prefix="", patch_size=10, mode=None, sigma=5, sampling=None, seed=1, num_imgs=0, n_init=10)

**outputs** A model fit file

- **Parameters:**
    - img_idr = Path to directory where training images are stored
    - k = Number of clusters to fit
    - out_path = Path to directory where the model output should be stored
    - prefix = Keyword for target images. Anything in img_dir without the prefix will be skipped
    - patch_size = Size of the NxN neighborhood around each pixel
    - mode = Either None (default) for RGB image input or "spectral" for multispectral images
    - sigma = Gaussian blur sigma. Denotes severity of gaussian blur performed before patch identification
    - sampling = Fraction of image from which patches are identified
    - seed = Seed for determinism of random elements like sampling of patches 
    - num_imgs = Number of images to use for training. Default is all of them in img_dir with prefix 
    - n_init = Number of random initiations tried by MiniBatchKMeans. The algorithm is run on the best one

- **Context:**
    - Used to fit a kmeans cluster model on a set of training images. Intended to be used with `pcv.predict_kmeans`
    and `pcv.mask_kmeans` downstream, which are documented [here](kmeans_classifier.md). 

- **Example use:**
    - [Use in kmeans tutorial](https://plantcv.org/tutorials/kmeans-clustering) 

```python

from plantcv import plantcv as pcv


# Use 10 images to train 6 clusters with a patch size of 4
pcv.learn.train_kmeans(img_dir="./silphium_integrifolium_root_images", 
             out_path="./kmeansout_.fit", prefix="Silphium", k=6, patch_size=4, num_imgs=10)

```


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/learn/train_kmeans.py)
