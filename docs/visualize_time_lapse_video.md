## Automatically Generate Time-Lapse Videos 

This function automatically generates and saves time-lapse videos given the folder of images. 

**plantcv.visualize.time_lapse_video**(*path_img, list_img, suffix_img, size_frame=None, fps=29.97, name_video='time_lapse_video',
                     path_video=path_img, display='on'*)

**returns** There is no returned value for this function. The generated video would be saved in the user specified directory. 

- **Parameters:**
    - img_directory   - Directory of images desired to be made into a video
    - list_img        -  desired list of images in img_directory to create the video. If None is passed, all images would be included by default.
    - suffix_img - The suffix of all input images. e.g. suffix='.jpg' or suffix='.png' or suffix='img10.jpg'. Make sure all images have the same suffix
            
            Note: If neigher list_img nor suffix_img is provided, all images in the directory will be included
            
    - size_frame - The desired size of every frame.
    
            Note: In a video, every frame should have the same size.
            The assumption is that all images given should have same size. However, in some cases, the sizes of images are slightly differ from each other.
            With a given frame size, if an images is larger than that, the image would be cropped automatically; if an image is smaller than that, the image would be zero-padded automatically
            If the frame size is not given, the largest size of all images would be used as the frame size.
    
    - fps: (frames per second) frame rate. By default fps=29.97.
            Commonly used values: 23.98, 24, 25, 29.97, 30, 50, 59.94, 60   
    - name_video - The desired name of output video name. By default the name would be 'time_lapse_video'
    - path_video - The desired saving path of the video file. By default, the video will be saved at the same directory of the images. 
    - display    - Indicator of whether to display current status (by displaying saving directory and saving name) while running this function. By default the display is turned on. 

- **Context:**
    - Used to generate time-lapse video given a bunch of images. 
    
- **Example Use:**
    - Below
    - [Use in Time Series Documentation](time_series.md)

**Folder of images**

As an example, you can used the sample saved inside PlantCV to test. You will need to know the directory of your PlantCV package. 
You can find the test data here: "./plantcv/tests/seires_data/raw_im". We are to use all images inside the folder "raw_im" to generate a time-lapse video.
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

pcv.visualize.time_lapse_video(img_directory=img_directory, list_img=list_img, size_frame=size_frame, fps=fps, name_video=name_video, path_video=path_video, display=display)
pcv.visualize.time_lapse_video(img_directory=img_directory, suffix_img=suffix_img, size_frame=size_frame, fps=fps, name_video=name_video, path_video=path_video, display=display)


```

**Video generated**

The generated video is saved automatically in the user-specified directory (path_video). The generated video should look similar to the one below:
<iframe src="https://player.vimeo.com/video/436453444" width="640" height="640" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/time_lapse_video.py)
