import numpy as np
from skimage.filters import gaussian
from sklearn.feature_extraction import image


def _patch_extract(img, patch_size=10, sigma=5, sampling=None, seed=1):
    """Extracts patches from an image.

    Parameters:
    -----------
    img        : numpy.ndarray,
        An image from which to extract patches
    patch_size : positiv non zero int,
        Size of the NxN neighborhood around each pixel
    sigma      : positive real or sequence of positive reals,
        Gaussian blur sigma. Denotes severity of gaussian blur performed before patch identification
    sampling   : float (0, 1],
        Fraction of image from which patches are identified
    seed       : int,
        Seed for determinism of random elements like sampling of patches

    Returns:
    --------
    patches_lin : numpy.ndarray
    """
    # Gaussian blur
    if len(img.shape) == 2:
        img_blur = np.round(gaussian(img, sigma=sigma)*255).astype(np.uint16)
    elif len(img.shape) == 3 and img.shape[2] == 4:  # rgba
        img = img[:, :, :3]  # removes alpha channel
        img_blur = np.round(gaussian(img, sigma=sigma, channel_axis=2)*255).astype(np.uint16)
    elif len(img.shape) == 3 and img.shape[2] >= 3:  # rgb or multi/hyperspec
        img_blur = np.round(gaussian(img, sigma=sigma, channel_axis=2)*255).astype(np.uint16)

    # Extract patches
    patches = image.extract_patches_2d(img_blur, (patch_size, patch_size),
                                       max_patches=sampling, random_state=seed)
    N = patches.shape[0]
    patches_lin = patches.reshape(N, -1)
    return patches_lin
