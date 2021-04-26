## Automatically Generate a Time-Lapse Video given A Directory of Images

This function automatically generates and saves the time-lapse video generated based on the given the folder of images. 

**plantcv.visualize.time_lapse_video**(*img_directory, list_img=None, auto_sort=True, suffix_img=None, size_frame=None, 
fps=29.97, name_video='time_lapse_video', path_video=None, display='on'*)

**returns** list_img, size_frame

- **Parameters:**
    - img_directory         - Directory of images desired to be made into a video
    - list_img (optional)   - Desired list of images in img_directory to create the video. If None is passed, all images would be included by default.    
    - auto_sort             - indicator of whether to sort the images.
    - suffix_img (optional) - The suffix of all input images. e.g. suffix='.jpg' or suffix='.png' or suffix='img10.jpg'. Make sure all images have the same suffix
            
    If neigher list_img nor suffix_img is provided, all images in the directory will be included.
    - size_frame (optional) - The desired size of every frame.
    
    To generate a video, the image used in every frame shold have the same size, known as frame size. 
    In most cases where the images have the same size, the image size is frame size, e.g. ```size_frame=(640, 480)```. 
    In some cases where not all images have the same size, image resizing would be done automaticaly
    to be able to generate the video, with a warning message generated. 
    
    If no value is passed to this parameter, the largest size of all images would be used as the frame size.
    
    The resizing is done by cropping for those larger then desired sizes, zero-padding for those smaller than desired sizes.
    
            Note: The most commonly used definition of frame size/image size is different from most commonly 
            used definition of matrix size (e.g. numpy arrays). The frame size/image size is defined as (width, height), 
            while the matrix size is defined as (num_rows, num_columns). 
            If you are trying to get the frame size/image size from the size of matrix (array), remember of change the 
            order of first and second dimension of the matrix, i.e. frame size = (num_columns, num_rows). 
    
    - fps: (frames per second, optional) - frame rate. By default fps=29.97. Commonly used values: 23.98, 24, 25, 29.97, 30, 50, 59.94, 60   
            
    - name_video (optional)              - The desired name of output video name. By default, the name would be 'time_lapse_video'
    - path_video (optional)              - The desired saving path of the video file. By default, the video will be saved at the same directory 
    of the images. 
    - display (optional)                 - Indicator of whether to display current status (by displaying saving directory and saving name) while 
    running this function. By default, the display is turned on. 

- **Context:**
    - Used to generate time-lapse video given a bunch of images. 
    
- **Example Use:**
    - Below
<!---
    - [Use in Time Series Documentation](time_series.md)


**Folder of images**

As an example, you can the sample saved inside PlantCV to test. You will need to know the directory of your PlantCV package. 
You can find the test data here: "./plantcv/tests/seires_data/raw_im". We are to use all images inside the folder "raw_im" to generate a time-lapse video.
--->

```python
from plantcv import plantcv as pcv
# Note you will have to change this part on your own
img_directory = './plantcv/tests/seires_data/raw_im'

list_img = [img for img in os.listdir(dir_img) if img.endswith('.jpg')]

# In this specific case, every image has a suffix of ".jpg"
suffix_img = '.jpg'

# In this case I know the sizes for all of the images is from (499, 499) to (501, 501), and here I decide I want the frame size to be (500, 500).
size_frame = (500, 500)

fps = 29.97

name_video = 'eg_time_lapse'

# In this specific case the video will be saved in the save directory of the images
path_video = path_img

display    = 'on'

list_img, frame_size = pcv.visualize.time_lapse_video(img_directory=img_directory, list_img=list_img, size_frame=size_frame, fps=fps, name_video=name_video, path_video=path_video, display=display)
list_img, frame_size = pcv.visualize.time_lapse_video(img_directory=img_directory, suffix_img=suffix_img, size_frame=size_frame, fps=fps, name_video=name_video, path_video=path_video, display=display)


```

**Video generated**

The generated video is saved automatically in the user-specified directory (path_video). The generated video should look similar to the one below:
<iframe src="https://player.vimeo.com/video/436453444" width="640" height="640" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/time_lapse_video.py)
