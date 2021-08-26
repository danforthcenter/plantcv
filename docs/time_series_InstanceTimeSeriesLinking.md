## Time-series Tracking

This class is designed to track segmented instances over time. Images should be taken across a time (e.g. every 4 hours 
for several days), and ideally either plant or camera should have minimal or no movment. 

To use this class for generating time-series linking, instance segmentation for every image is required. For more 
information of instance segmentation, check out here: [Instance Segmentation](instance_segmentation_tutorial.md) for 
a demo of instance segmentation.
 
The goals are:
1) Assign global unique indices to every instance at every timepoint
2) Learn how instances connect with each other between consective timepoints

For details of using this class, see examples below.

*initialize an instance of InstanceTimeSeriesLinking class:* 

**inst_ts_linking = plantcv.time_series.InstanceTimeSeriesLinking()**

*use the class method `link` to track time-series*

**inst_ts_linking.link**(*masks, metric, thres*)
**returns** No returned value, the inst_ts_linking is an instance object which belongs to InstanceTimeSeriesLinking class. 

- **Parameters**
    - masks: a list of instance segmentation masks. Every element of this list is a numpy array represents instance 
      segmentation masks correspond to one image (one timepoint). To be specific, a numpy array of size `r*c*n` represents 
      that there are `n` segmented instances in the image (hence `n` masks), and the size of the original image is `r*c`.

    - metric (optional): the metric to measure how likely two instances (segmentation masks) appear in two timepoints 
      can be considered as the same object appear in different timepoints. Currently, two overlap-based metrics are 
      available: IoU (intersection-over-union) and IoF (Intersection-over-first timepoint area). 
      Default value is "IOU".

    - thres (optional): how large the weight `W_t1_i_t2_j` (calculated based on the metric of choice) should be to for the 
      connection from i-th segment from t1 to j-th segment from t2 to be considered as a potential link. 
      Different threshold should be chosen when using different metric. Default value is 0.2.

- **Output:**
        An instance object of InstanceTimeSeriesLinking class, with all information (original, mask series, link information, etc.) included.   
    
- images: a list of images. Every element of this list is an array represents one image
- timepoints: a list of timepoints. The lengths for images, masks and timepoint should be the same and the elements are correspond to each other
Note: when comparing instances from two timepoints, we are comparing n1 masks from t1 and n2 masks from t2, 


```python
from plantcv.plantcv.time_series  import time_series_linking as tsl
## Load all segmentation masks and put them into a list in the correct order here
# masks = 

# Below are examples of input variables, always adjust base on your own application. 
metric = 'IOU'
thres = 0.1

## Initialize an instance of class InstanceTimeSeriesLinking
inst_ts_linking = tsl.InstanceTimeSeriesLinking()
inst_ts_linking.link(masks=masks, metric=metric, thres=thres)
```
Make sure the list of all the masks is temporarily sorted. 

To save the instance object, simply specify the directory of saving as well as the name (prefix)
```python
## Specify the desired directory to save results
dir_save = "./results"

## Specify the desired name to save the result (prefix)
savename = "linked_series"

inst_ts_linking.save_linked_series(savedir=dir_save, savename=savename)
```

To import a previously saved result:
```python
dir_save = "./results"
savename = "linked_series"
## Initialize an instance of class InstanceTimeSeriesLinking
inst_ts_linking = tsl.InstanceTimeSeriesLinking()
inst_ts_linking.import_linked_series(savedir=dir_save, savename=savename)
```

To visualize the time-series tracking result, a list of images corresponding to every set of masks in the list of masks 
must be provided. Besides, a list of timepoints also need to be provided.
The visualization assigns colors based on unique object indices information, in other words, all objects in the time-series 
with the same unique index will be assigned the same color.
The information can be achieved from `inst_ts_linking.ti`.
The visualization results are saved in the provided directory `savedir`.
```python
## Load all original images and put them into a list in the correct order here (same order as masks)
# imgs = 

## Get a list of timepoints (usually from the file names of original images)
# timepoints = 

# specify the directory to save visualization
visualdir = "./results/visualization"
inst_ts_linking.visualize(imgs=imgs, masks=masks, tps=timepoints, savedir=visualdir, ti=inst_ts_linking.ti, color_all=None)
```
Note: `visualize` is a static method of class `InstanceTimeSeriesLinking`. In other words, it can be called without initialization 
of a class object, as long as all required parameters as passed in. See example below. If `ti` is not provided, the color 
assignment is based on local indices.
```python
## Load all segmentation masks and put them into a list in the correct order here
# masks = 

## Load all original images and put them into a list in the correct order here (same order as masks)
# imgs = 

## Get a list of timepoints (usually from the file names of original images)
# timepoints = 

# specify the directory to save visualization
visualdir = "./results/visualization"

tsl.InstanceTimeSeriesLinking.visualize(imgs=imgs, masks=masks, tps=timepoints, savedir=visualdir)
```

In some cases, objects disappear in one or several timepoints and re-appear. To lower the rate of assigning new indices
(false positive) to those objects, updating the time-series tracking is also possible by indicating the expected maximum 
time gap of disappearance `max_gap`. By default `max_gap=5`. A larger number of `max_gap` is not recommended. 

```python
nax_gap = 3
inst_ts_linking.update_ti(max_gap=nax_gap)
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/time_series/time_series_linking.py)

<!--
You will get two sets of results: those end with "_old" are results before updating; others are final results.
1. {}.pkl (or {}_old.pkl): an "InstanceTimeSeriesLinking" class instance, with all the information included: time points, original images, instance segmentation masks, etc. The filename is specified by user. 
2. {}.csv (or {}_old.csv): a csv file includes the linking series information (every row in the table is a unique instance throughtout time).
3. link_info.csv (or {}_old.csv): a csv file includes the linking information.
4. a folder called "visualization" ("visualization_old"), which contains 3 subfolders:

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
It is always a good practice to check the quality of instance segmentation before running time_series_linking. One way to check the instance segmentation is to make a time-lapse video with your instance segmentation result shown in bounding boxes. To make time-lapse videos, you will need video editing softwares, e.g. imovie. An example is shown below. Notice that in almost all cases, you would observe that the colors for the same leaf change during the time. That is due to the random assignment of labels. You can later compare this time lapse video to that generate after all labels re-assigned by running time_series_linking function. 

Instead of making a video, another way to check the quality of instance segmentation is by checking the segmented image one by one.

<iframe src="https://player.vimeo.com/video/434385132" width="640" height="480" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>

```python
from plantcv import plantcv as pcv
# Below are examples of input variables, always adjust base on your own application. 
inst_ts_linking = InstanceTimeSeriesLinking(images, masks, timepoints, logic, thres, name_sub)
inst_ts_linking(save_dir, visualdir_, visualdir, savename_, savename, csvname_, csvname)
```
When it finished, you can go ahead and check the saved result. If you are not sure where the results are saved, you can type:
```inst_ts_linking.savedir```
in a cell to print out the saving directory.

You can also type ```inst_ts_linking.link_series``` in a cell to print linking information on the screen for a quick check.

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

You might have noticed that to use the method described above, you will have to get data prepared, i.e. the images should be in a list and the masks should be in a list of same lenghth. 
Both of them should be sorted chronologically. You can absolutely do this, and it is not hard to do, but alternatively, you are also welcome to use another class, which is a wrapper, by which 
you would only need to provide directories, and conditions for time points. 
InstanceTSLinkingWrapper(object):

**inst_ts_link_wrapper = plantcv.time_series.InstanceTSLinkingWrapper**(*dir_save, savename*)
**inst_ts_link = inst_ts_link_wrapper**(*dir_img, dir_seg, pattern_dt, time_cond, logic, thres, name_sub, suffix, suffix_seg*)
**returns** An instance which belongs to InstanceTimeSeriesLinking class. 

- **Parameters for initialization:**
    - dir_save: the desired directory to save the results
    Note: under the user specified saving directory, a new folder named after the date and time (format: YYYY-MM-DD-HH-mm) the function runs will be created to save results.    
    - savename: the desired name to save the result

Once you get the class object initialized, it is callable, which means it is a callable function itself so that you can get the linking result by running the 2nd line of code presented above. 
- **Parameters to call functions:**
    - dir_img: directory of original images
    - dir_seg: directory of segmentation results
    - pattern_dt: the pattern of date and time part in original file names, dafault value '\d{4}-\d{2}-\d{2}-\d{2}-\d{2}' which represents YYYY-MM-DD-hh-mm. 
    - time_cond: condition of data used, indicated by list of times, e.g. time_cond = ['08-05', '15-05'] represents for including data collected at 8:05am and 3:05pm everyday in this experiment. Make sure the format of date matches the pattern-datetime.
    - logic: the logic used in linking. Segments from different timepoints are believed to be the same instance appeared in different timepoints based on either their IOU (intersection-over-union) or IOS (Intersection-over-self_area)
      If the value is larger than the threshold, they will be connected. The logic can be either "IOU" or "IOS". "IOS" is recommended. 
    - thres: threshold used in the linking logic as mentioned above. For "IOS" it is recommended to start with a threshod of 0.2.
    - name_sub: name of the main subject we care about. By default name_sub = 'instance', which means the instances we care about in images are called "instance". Other examples can be "leaf" which means that we call one instance in images a "leaf".
    - suffix: the suffix of original images, make sure all images having the same suffix, e.g. suffix='.jpg' or suffix='-img8.jpg'. Make sure all the images desired having the same suffix pattern. By default ".jpg"
    - suffix_seg: the suffix of segmentation results, make sure all segmentation results having the same suffix. By default '.pkl'
    
```python
from plantcv import plantcv as pcv
# Below are examples of input variables, always adjust base on your own application. 
## Specify the desired directory to save results
dir_save = '/shares/mgehan_share/hsheng/projects/maskRCNN/results/output_10.1.9.214_wtCol_512/index12/2020-08-24-07-29/time_series_linking'

## Specify the desired name to save the result (prefix)
savename = 'linked_series'

## Initialize and instance of class InstanceTSLinkingWrapper
inst_ts_linking_wrap = InstanceTSLinkingWrapper(dir_save=path_save, savename=name_series)

## Specify the directory of original image
dir_img          = '/shares/mgehan_share/acasto/auto_crop/output_10.1.9.214_wtCol_512'
## Specify the directory of instance segmentation result 
dir_seg = '/shares/mgehan_share/hsheng/projects/maskRCNN/results/output_10.1.9.214_wtCol_512/index12/2020-08-24-07-29/segmentation/updated'
## Specify the date-time pattern of original image names
pattern_dt = '\d{4}-\d{2}-\d{2}-\d{2}-\d{2}' # YYYY-MM-DD-hh-mm
## Specify the desired time point to include in to the analysis
time_cond = ['08-05', '11-05', '17-05', '21-05'] 
## Specify the linking logic and threshold
logic = 'IOS'
thres = 0.2
## Specify the main subject
name_sub = 'leaf'
## Specify the common suffix of interested original images
suffix   = '-img12.jpg'
## Specify the common suffix of interested segmentation result
suffix_seg = '.pkl'

inst_ts_linking = pcv.time_series.inst_ts_linking_wrap(dir_img, dir_seg, pattern_dt, time_cond, logic, thres, name_sub, suffix, suffix_seg)
```
All the analysis for the results are same to what described above.
-->





