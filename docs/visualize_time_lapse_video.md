## Automatically Generate a Time-Lapse Video given A Directory of Images

This function generates and saves the time-lapse video based on a list of paths to the images.

**plantcv.visualize.time_lapse_video**(*source, out_filename='./time_lapse_video.mp4', fps=29.97*)

**returns** None

- **Parameters:**
    - source         - File path to a directory of images to use, list of paths to the images, or list of `numpy.ndarray` objects to create the video
    - out_filename   - Name of file to save the generated video to.
    - fps            - Frame rate (frames per second) By default fps=29.97. Commonly used values: 23.98, 24, 25, 29.97, 30, 50, 59.94, 60

- **Context:**
    - Used to generate time-lapse video given a list of images.

- **Example Use:**
    - Below


```python
from plantcv import plantcv as pcv
# Note you will have to change this part on your own path
img_directory = './path_to_images_directory/'

pcv.visualize.time_lapse_video(source=img_directory,
                               out_filename='./eg_time_lapse.mp4')
```

**Video generated**

The generated video should look similar to the one below:
<iframe src="https://player.vimeo.com/video/436453444" width="640" height="640" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/time_lapse_video.py)
