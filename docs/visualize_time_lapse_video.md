## Automatically Generate a Time-Lapse Video given A Directory of Images

This function generates and saves the time-lapse video based on a list of paths to the images.

**plantcv.visualize.time_lapse_video**(*img_list, out_filename='./time_lapse_video.mp4', fps=29.97, display=True*)

**returns** frame_size

- **Parameters:**
    - list_img       - List of paths to the images to create the video.    
    - out_filename   - Name of file to save the generated video to.
    - fps            - Frame rate (frames per second) By default fps=29.97. Commonly used values: 23.98, 24, 25, 29.97, 30, 50, 59.94, 60   
    - display        - if True (default), displays the path to the generated video.

- **Context:**
    - Used to generate time-lapse video given a list of images.
    - List of image paths can be generated with [`plantcv.io.read_dataset`](io_read_dataset.md). 

- **Example Use:**
    - Below


```python
from plantcv import plantcv as pcv
# Note you will have to change this part on your own path
img_directory = './path_to_images_directory/'
img_paths_list = pcv.io.read_dataset(source_path=img_directory, sort=True)

fps = 29.97
name_video = './eg_time_lapse'
display    = True

frame_size = pcv.visualize.time_lapse_video(img_list=img_paths_list,
                                                    out_filename=name_video,
                                                    fps=fps, display=display)
```

**Video generated**

The generated video is saved automatically in the user-specified directory name_video. The user defined directory must already exist. The generated video should look similar to the one below:
<iframe src="https://player.vimeo.com/video/436453444" width="640" height="640" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/time_lapse_video.py)
