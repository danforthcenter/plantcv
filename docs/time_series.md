## time_series

This function is designed to get leaf instance growth information for a plant given a series of images (images taken across a time period, e.g. images taken every several hours, recording the growth of the plant, where ideally there should be no or at least minimum movement for plant or camera).

To run this function, the instance segmentation for every image should be achieved beforehand. For more information and a demo of instance segmentation, check here: [Instance Segmentation](instance_segmentation_tutorial.md).
 
When using instance segmentation algorithms like maskRCNN, the assignment for the instance labels is random, i.e. the same index does not necessarily represents the same instance in different images. 

To understand the growth of every leaf instance of a plant, we need to re-assign the instance labels so that the same leaf always have the same instance label across the whole time period. 

**plantcv.time_series.time_series_linking**(*imagedir, segmentationdir, savedir, time_cond, link_logic=1, class_names=['BG', 'Leaf'], mode='link', suffix='.jpg'*)

**returns** An instance that is a Plant object

- **Parameters:**
    - imagedir: directory of original image used
    - segmentationdir: directory of leaf instance segmentation result
    - savedir: desired saving directory of linking result. Note that this function will generate a folder under your specified saving directory, with the date and time you run this programme
    - time_cond: condition of data used, indicated by list of times, e.g. time_cond = ['08-05', '15-05'] represents for including data collected at 8:05am and 3:05pm everyday in this experiment
    - link_logic: 1: IoU (intersection over union), 2: Io1A (intersection over 1st area), default value: 1
    - class_names: used in bounding box visualization. by default there are background and leaf, i.e. class_names = ['BG', 'leaf']
    - mode: can be either 'link' or 'load', use 'link' when trying to get linked time-series from instance segmentation; use 'load' when trying to load from saved linking
    - suffix: the suffix of original images, make sure all images having the same suffix, e.g. suffix='.jpg' or suffix='-img8.jpg'. Make sure all the images desired having the same suffix pattern.
- **Output:**
        An instance of Plant object is returned, with all information (original image series, mask series, link information, etc.) included. Besides, all the results will be saved in user defined "savedir".
        
Note: under the user specified saving directory, a new folder named after the date and time (format: YYYY-MM-DD-HH-mm) the function runs will be created to save results. 
        
1. colors.pkl: the colors (represented by arrays) used in bounding box visualization. With this predefined color set, same color will represent for the leaf instance with same instance label all the time, i.e. same color represents leaf with the same label. Without this predefined list of color, the assignment of color will be random, i.e. the color provides no information to leaf indices.  
2. details.txt: the logic of linking as well as time condition will be saved in this text file, so that would be easier for users to check these parameters for the specific expreiment.
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

path_img          = '/shares/mgehan_share/acasto/auto_crop/output_10.1.9.214_wtCol/maskrcnn_test'
path_segmentation = '/shares/mgehan_share/hsheng/projects/maskRCNN/results/output_10.1.9.214_wtCol/exp3/detection/modified'
path_save         = '/shares/mgehan_share/hsheng/projects/maskRCNN/results/output_10.1.9.214_wtCol/exp3/test'
time_cond         = ['08-05', '11-05', '17-05', '21-05']
link_logic        = 1
class_names       = ['BG', 'Leaf']
mode              = 'link'
suffix            = '.jpg'
​linked_Plant = pcv.time_series.time_series_linking(imagedir=path_img, segmentationdir=path_segmentation, savedir=path_save, time_cond=time_cond, link_logic=link_logic, class_names=class_names, mode=mode, suffix=suffix)

# Print the saving directory so that you can go check the result:
linked_Plant.savedir

# Print visualization directory:
linked_Plant.visualdir

# Print linking information on the screen for a quick check:
linked_Plant.link_series
```

1. Analysing shapes:
Create a workflow and use the PlantCV analyze_object function to traverse all images inside the 1st visualization folder. 

2. Making time-lapse videos to visualize the growth of every leaf:
To make videos, you will need video editing softwares, e.g. imovie.\
Direct yourself to the visualization folder, and go into 'visualization2'. Every folder represents for a leaf. Include all images for one leaf in a video project, sort them by name in an ascending order, and generate a time-lapse video. 
Here is an example of time-lapse of one leaf: 

<iframe src="https://player.vimeo.com/video/434378499" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>
<p><a href="https://vimeo.com/434378499">growth of plant focusing on single leaf</a> from <a href="https://vimeo.com/user118465122">Hudanyun Sheng</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

3. Making a time-lapse video to visualize the growth of the plant by showing the segmentation in bounding boxes, with the same leaf always shown with the same color. Direct yourself to "visualization 3" folder and include all images to a video project, sort them by name in an ascending order, and generate a time-lapse video. 
An example of time-lapse video with visualization shown in bounding boxes is shown below. When compare to the video made of instance segmentation, result, you will observe that now every leaf is represented by the same color all the time, which means the label re-assignemnt is successful.

<iframe src="https://player.vimeo.com/video/434158572" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/time_series/time_series.py)
