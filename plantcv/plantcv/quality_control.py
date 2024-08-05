# Do quality control of images by determining if there is problematic color data

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug

def quality_control(img):

    # Convert the img from BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Split the img into its Red, Green, and Blue channels
    red_channel, green_channel, blue_channel = img_rgb[:, :, 0], img_rgb[:, :, 1], img_rgb[:, :, 2]
    
    # Function to check for over- or underexposure
    def check_exposure(channel):
        total_pixels = channel.size
        zero_count = np.sum(channel == 0)
        max_count = np.sum(channel == 255)
        return (zero_count / total_pixels > 0.05) or (max_count / total_pixels > 0.05)
    
    # Check each channel for over- or underexposure
    if check_exposure(red_channel) or check_exposure(green_channel) or check_exposure(blue_channel):
        print("WARNING: The image is over- or underexposed because more than 5% of pixels are equal to 0 or 255 intensity. Color cannot be analyzed responsibly, as color values are lost above the minimum (0) and maximum (255). Change camera settings to capture appropriate images.")
    
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
    plt.show()