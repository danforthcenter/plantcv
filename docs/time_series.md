## time_series

This function is designed to get leaf instance growth information for a plant given a series of images (images taken across a time period, recording the growth of the plant, where there should be minimum or none movement of plant or camera).

To run this function, the instance segmentation for every image should be achieved beforehand. For a demo of instance segmentation, check here:
As a reminder, you will need a maskRCNN environemnt to be able to use this tool. For more information, check here:
 
When using instance segmentation algorithms like maskRCNN, the assignment for the instance labels is random, i.e. the same index does not necessarily represents the same instance in different images. (Another example is k-means)

To understand the growth of every leaf instance of a plant, we need pull out the same leaf across the whole time period. 


**plantcv.time_series.time_series_linking**(*imagedir, segmentationdir, savedir, time_cond, link_logic=1, class_names=['BG', 'Leaf']*)

**returns** no returned values, all the results are saved in the user specified directory

- **Parameters:**
    - imagedir: directory of original image used
    - segmentationdir: directory of leaf instance segmentation result
    - savedir: desired saving directory of linking result
    - time_cond: condition of data used, indicated by list of times, e.g. time_cond = ["08-05", "15-05"] represents for including data collected at 8:05am and 3:05pm everyday in this experiment
    - link_logic: 1: IoU (intersection over union), 2: Io1A (intersection over 1st area), default value: 1
    - class_names: used in bounding box visualization. by default there are background and leaf
- **Output:**
        There is no returned values as output, though the results will be saved in user defined "savedir"
        1. colors.pkl: the colors (indicated by arrays) used in bounding box visualization. Without this predefined list of color, the assignment of color will be random. With this predefined color set, same color will represent for the same leaf all the time
        2. details.txt: the logic of linking as well as time condition will be shown, so that would be easier for users to check these parameters for the specific expreiment
        3. saved_plant.pkl: a "Plant" instance will be saved, with all the information included: time points, original images, instance segmentation masks, etc.
        4. a folder called "visualization", which contains 3 subfolders:
            1) a folder call "visualization 1", which contains 1st set of visualization
                In this set of visualization, the instance segmentation masks are applied to original images, so that there is only 1 leaf in every image. 
                result name: {}_{}_{}_{}_{}.png
                Naming rules for file names: 
                    1st digit: time of 1st emergence of the leaf
                    2nd digit: leaf index when it first emerges
                    3rd digit: current time point
                    4th digit: current leaf index
                    5th digit: date and time included in original file name, typically, it follows the format of YYYY-MM-DD-HH-MM.

            2) a folder called "visualization 2", which contains 2nd set of visualization
                This set of visualization show results with an alpha channel, such that we can see the main leaf in the original image, with other parts being half transparent
                There are several subfolders, the number of subfolders depends on the number of "new leaves" in total
                Every subfolder is a "new leaf", whose name is {}_{}, with 1st digit represents time of 1st emergence of the leaf and 2nd digit represents leaf index when it first emerges
                    Inside every folder, images of leaves with names "{}.png" are contained; inside the {} the date-time of the original image is contained, typically, it follows the format of YYYY-MM-DD-HH-MM. 

            3) a folder called "visualization 3", which containes 3rd set of visualization 
                This set of visualization show results with bounding boxes. In every image, different leaves are show in bounding boxes with different colors. 
                Naming format: {}_visual.png; inside the {} the date-time of the original image is contained, typically, it follows the format of YYYY-MM-DD-HH-MM. 

```python
from plantcv import plantcv as pcv
# Below are examples of input variables, always adjust base on your own application. 

path_img          = '/shares/mgehan_share/acasto/auto_crop/output_10.1.9.214_wtCol/maskrcnn_test'
path_segmentation = '/shares/mgehan_share/hsheng/projects/maskRCNN/results/output_10.1.9.214_wtCol/exp3/detection/modified'
path_save         = '/shares/mgehan_share/hsheng/projects/maskRCNN/results/output_10.1.9.214_wtCol/exp3/test'
time_cond         = ['08-05', '11-05', '17-05', '21-05']
​pcv.time_series.time_series_linking(imagedir=path_img, segmentationdir=path_segmentation, savedir=path_save, time_cond=time_cond, link_logic=1, class_names=['BG', 'Leaf'])
```
**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/time_series/time_series.py)
