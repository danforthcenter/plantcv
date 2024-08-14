# Perform quality control by checking for problematic color data
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from plantcv.plantcv import outputs, params, warn


# Function to check for over- or underexposure
def _check_exposure(channel, warning_threshold, channel_name):
    """Check if a color channel is over- or underexposed.

    This function analyzes the given color channel to determine if
    more than the specified percentage of its pixels are either at the
    minimum (0) or maximum (255) intensity values, which may indicate
    over- or underexposure issues.

    Parameters
    ----------
    channel : numpy.ndarray
        A 2D numpy array representing the color channel of an image.
    warning_threshold : float
        The threshold value for triggering a warning for over- or underexposure.
    channel_name : str
        Name of the channel being analyzed (e.g., "red", "green", "blue").

    Returns
    -------
    bool
        True if the channel is over- or underexposed; False otherwise.
    """
    total_pixels = channel.size
    zero_count = np.sum(channel == 0)
    max_count = np.sum(channel == 255)
    proportion_bad_pix = zero_count / total_pixels
    outputs.add_metadata(term=f"{channel_name}_percent_bad_exposure_qc", datatype=float, value=proportion_bad_pix)
    return (zero_count / total_pixels > warning_threshold) or (max_count / total_pixels > warning_threshold)


def exposure(rgb_img, warning_threshold=0.05):
    """Perform quality control by checking for problematic color data and plotting histograms.

    This function performs an analysis of an image to check for over- or underexposure
    in the red, green, and blue color channels. It also generates and displays histograms
    for each color channel to visualize the distribution of pixel intensities.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Color image data.
    warning_threshold : float, optional
        The threshold value for triggering a warning for over- or underexposure, by default 0.05
    """
    # Convert the img from BGR to RGB
    img_rgb = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)

    # Split the img into its Red, Green, and Blue channels
    red_channel, green_channel, blue_channel = img_rgb[:, :, 0], img_rgb[:, :, 1], img_rgb[:, :, 2]

    # Check each channel for over- or underexposure
    if (
        _check_exposure(red_channel, warning_threshold, channel_name="red") or
        _check_exposure(green_channel, warning_threshold, channel_name="green") or
        _check_exposure(blue_channel, warning_threshold, channel_name="blue")
    ):
        warn(
            f"The image is over- or underexposed because more than {warning_threshold * 100}% of "
            "pixels are equal to 0 or 255 intensity. Color cannot be analyzed "
            "responsibly, as color values are lost above the minimum (0) and maximum "
            "(255). Change camera settings to capture appropriate images.")

    if params.debug is not None:
        # Plot the histograms
        plt.figure(figsize=(10, 5))

        # Red histogram
        plt.subplot(131)
        plt.hist(red_channel.ravel(), bins=256, color='red', alpha=0.5)
        plt.title('Red Histogram')
        plt.xlabel('Intensity Value')
        plt.ylabel('Count')

        # Green histogram
        plt.subplot(132)
        plt.hist(green_channel.ravel(), bins=256, color='green', alpha=0.5)
        plt.title('Green Histogram')
        plt.xlabel('Intensity Value')
        plt.ylabel('Count')

        # Blue histogram
        plt.subplot(133)
        plt.hist(blue_channel.ravel(), bins=256, color='blue', alpha=0.5)
        plt.title('Blue Histogram')
        plt.xlabel('Intensity Value')
        plt.ylabel('Count')

        plt.tight_layout()
        if params.debug == "print":
            plt.savefig(os.path.join(params.debug_outdir, str(params.device) + '_bad_exposure_hist.png'))
            plt.close()
        elif params.debug == "plot":
            plt.show()
