## time_series

This function is designed to link segmented objects over time. Images should be taken across a time (e.g. every several hours) and ideally there should be minimal movment of plant/camera.

To run this function, the instance segmentation for every image is required. For more information on instance segmentation and a demo of instance segmentation, check here: [Instance Segmentation](instance_segmentation_tutorial.md).
 
When using instance segmentation algorithms like maskRCNN, the assignment for the instance labels is random, i.e. the same index does not necessarily represents the same instance in different images. 

To understand the growth of every leaf instance of a plant, we need to re-assign the instance labels so that the same leaf always has the same instance label (identifier) across the whole time period. 

**plantcv.time_series.time_series_linking**(*imagedir, segmentationdir, savedir, time_cond, link_logic=1, class_names=['BG', 'Leaf'], mode='link', suffix='.jpg'*)

**returns** An instance that is a Plant object

- **Parameters:**
    - imagedir: directory of original image used
    - segmentationdir: directory of leaf instance segmentation result
    - savedir: desired saving directory of linking result. Note that this function will generate a folder under your specified saving directory, with the date and time you run this programme
    - pattern_datetime: the pattern of date and time part in original file names, dafault value '\d{4}-\d{2}-\d{2}-\d{2}-\d{2}' which represents YYYY-MM-DD-hh-mm. 
    - time_cond: condition of data used, indicated by list of times, e.g. time_cond = ['08-05', '15-05'] represents for including data collected at 8:05am and 3:05pm everyday in this experiment. Make sure the format of date matches the pattern-datetime.
    - link_logic: 1: IoU (intersection over union), 2: Io1A (intersection over 1st area), default value: 1
    - class_names: used in bounding box visualization. by default there are background and leaf, i.e. class_names = ['BG', 'leaf']
    - mode: can be either 'link' or 'load', use 'link' when trying to get linked time-series from instance segmentation; use 'load' when trying to load from saved linking
    - suffix: the suffix of original images, make sure all images having the same suffix, e.g. suffix='.jpg' or suffix='-img8.jpg'. Make sure all the images desired having the same suffix pattern.
- **Output:**
        An instance of Plant object is returned, with all information (original image series, mask series, link information, etc.) included. Besides, all the results will be saved in user defined "savedir".
        
Note: under the user specified saving directory, a new folder named after the date and time (format: YYYY-MM-DD-HH-mm) the function runs will be created to save results. 
        
1. colors.pkl: the colors (represented by arrays) used in bounding box visualization. With this predefined color set, same color will represent for the leaf instance with same instance label all the time, i.e. same color represents leaf with the same label. Without this predefined list of color, the assignment of color will be random, i.e. the color provides no information to leaf indices.  
2. details.txt: the logic of linking as well as time condition will be saved in this text file, so that would be easier for users to check these parameters for the specific experiment.
3. saved_plant.pkl: a "Plant" object instance will be saved, with all the information included: time points, original images, instance segmentation masks, etc.
4. a folder called "visualization", which contains 3 subfolders:

    1) a folder call "visualization 1", which contains 1st set of visualization
        In this set of visualization, the instance segmentation masks are applied to original images, so that there is only 1 leaf in every image. 
        Naming convention for the saving names of the result:
        
        {}_{}-{}-{}-{}_{}.png
            1st digit: unique identifier of the leaf
            2nd digit: time of first emergence of the leaf
            3rd digut: leaf index when it first emerges
            4rd digit: current time point
            5th digit: current leaf index
            6th digit: original image name
    This set of visualization is designed for shape analysis by easily applying plantcv workflow. 

    2) a folder called "visualization 2", which contains 2nd set of visualization
        This set of visualization show results with an alpha channel, such that we can see the main leaf in the original image, with other parts being half transparent
        There are several subfolders, the number of subfolders depends on the number of "new leaves" in total
        Every subfolder is a "new leaf". Naming convention for folder names:
        
        Folder name: {}_{}-{}
            1st digit: unique identifier of the leaf
            2nd digit: time of first emergence of the leaf
            3rd digut: leaf index when it first emerges
            Inside every folder, images of leaves with names same as original image names are contained.
    This set of visualization is designed for making videos to track the growth of every single leaf. Images inside a folder are supposed to represent for the save leaf. So simply using all images inside one folder and sort them by name in an ascending manner would create a video showing how this leaf grows. 

    3) a folder called "visualization 3", which containes 3rd set of visualization 
        This set of visualization show results with bounding boxes. In every image, different leaves are show in bounding boxes with different colors. 
        Naming convention: 
        
        {}-visual.png
        The original image name is inside the {}.
    This set of visualization is designed for making time-lapse videos of segmentation shown with bounding boxes. With the instance labels re-assigned such that one label represents one leaf across the whole time, we would observe that every leaf is represented by a specific color across the whold time period. 
                
Before running the time_series_linking function, it is always a good practice to check the quality of instance segmentation before run time_series_linking. One way to check the instance segmentation is to make a time-lapse video with your instance segmentation result shown in bounding boxes. To make time-lapse videos, you will need video editing softwares, e.g. imovie. An example is shown below. Notice that in almost all cases, you would observe that the colors for the same leaf change during the time. That is due to the random assignment of labels. You can later compare this time lapse video to that generate after all labels re-assigned by running time_series_linking function. 

Instead of making a video, another way to check the quality of instance segmentation is by checking the segmented image one by one.

<iframe src="https://player.vimeo.com/video/434385132" width="640" height="480" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>


```python
from plantcv import plantcv as pcv
# Below are examples of input variables, always adjust base on your own application. 

## Specify the directory of original image
path_img          = '/shares/mgehan_share/acasto/auto_crop/output_10.1.9.214_wtCol_512'

## Specify the directory of instance segmentation result 
path_segmentation = '/shares/mgehan_share/hsheng/projects/maskRCNN/results/output_10.1.9.214_wtCol_512/index7/2020-06-25-10-35/subsampled/2020-06-30-10-51/'

## Specify the desired directory to save results
path_save         = '/shares/mgehan_share/hsheng/projects/maskRCNN/results/output_10.1.9.214_wtCol_512/index7/2020-06-25-10-35/time_series_linking'

## Specify the date-time pattern of original image names
pattern_datetime = '\d{4}-\d{2}-\d{2}-\d{2}-\d{2}' # YYYY-MM-DD-hh-mm

## Specify the desired time point to include in to the analysis
time_cond = ['08-05', '11-05', '17-05', '21-05'] 

link_logic  = 1
class_names = ['BG', 'Leaf']
mode        = 'link'

## Specify the suffix for all images you want to include, note that all the images shown have the same suffix as you specified
## Normally it would be something like '.png' or '.jpg', in this specific case, the image contained in the folder have name like 
## 'xxx-img{}.jpg', the number inside the {} represents the index of plant. So in this case, to include images for the same plant, 
## you will have to specify the index of plant.
suffix      = '-img7.jpg'
​linked_Plant = pcv.time_series.time_series_linking(path_img, path_segmentation, path_save, pattern_datetime, 
                               time_cond, link_logic, class_names, mode, suffix)
```
When it finished, you can go ahead and check the saved result. If you are not sure where the results are saved, you can type:
```linked_Plant.savedir```
in a cell to print out the saving directory.

You can also type ```linked_Plant.link_series``` in a cell to print linking information on the screen for a quick check.

Now that we have the linking results saved, we can have some analysis based on them. There are 3 suggested analysis described as below:

1. Analysing shapes:
    Create a workflow and use the PlantCV analyze_object function to traverse all images inside the 1st visualization folder. 

2. Making time-lapse videos to visualize the growth of every leaf.
You have two options of making time-lapse videos: using video editing software (e.g. iMovie) or using the PlantCV tool.
    - Generate time-lapse video using video editing software:
    
        Direct yourself to the visualization folder, and go into 'visualization2'. Every folder represents for a leaf. Include all images for one leaf in a video project, sort them by name in an ascending order, and generate a time-lapse video. 
        Here is an example of time-lapse of one leaf: 

        <iframe src="https://player.vimeo.com/video/434378499" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>
        <p><a href="https://vimeo.com/434378499">growth of plant focusing on single leaf</a> from <a href="https://vimeo.com/user118465122">Hudanyun Sheng</a> on <a href="https://vimeo.com">Vimeo</a>.</p>
    
    - There is also a PlantCV tool that is able to automatically generate and save time-lapse videos. Check here for the usage. The example code is provided at the end of this documentation. 
    
    

3. Making a time-lapse video to visualize the growth of the plant by showing the segmentation in bounding boxes, with the same leaf always shown with the same color. Direct yourself to "visualization 3" folder and include all images to a video project, sort them by name in an ascending order, and generate a time-lapse video. 
An example of time-lapse video with visualization shown in bounding boxes is shown below. When compare to the video made of instance segmentation, result, you will observe that now every leaf is represented by the same color all the time, which means the label re-assignemnt is successful.

    <iframe src="https://player.vimeo.com/video/434158572" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>
```python
## Videos generated using the 2nd set of visualization
# The directory of the 2nd set of visualization
from plantcv import plantcv as pcv
path_visual2 = os.path.join(Plant.visualdir, 'visualization2')

# Getting subfolders of the 2nd set of visualization
sub_folders  = [x[0] for x in os.walk(path_visual2)][1:]

# You are also to change this to your desired saving directory of the video. By default it will be saved in the same directory of the 2nd set of visualization.
path_video   = path_visual2

print('\n Saving videos for 2nd set of visualization.')
for sub_f in sub_folders:
    name_video     = os.path.split(sub_f)[1] # name of the videos are set to be same as the name of subfolders (i.e. the "identifier" of leaves)  
    pcv.visualize.time_lapse_video(img_directory=sub_f, suffix_img=Plant.ext, name_video=name_video, path_video=path_video, display='off')
print('\nfinished')

## Videos generated using the 3rd set of visualization
# The directory of the 3rd set of visualization
path_visual3 = os.path.join(Plant.visualdir, 'visualization3')
print('\n Saving videos for 3rd set of visualization.')

# You are free to change the name of the video to your desired ones
name_video_3 = 'visualization_w_bounding_box'

# You are free to change this to your desired saving directory of the video. By default it will be save in the same directory of visualization.
path_video_3 = Plant.visualdir
pcv.visualize.time_lapse_video(img_directory=path_visual3, suffix_img=Plant.ext, name_video=name_video_3, path_video=path_video_3, display='on')
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/time_series/time_series.py)


