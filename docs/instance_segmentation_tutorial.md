## Tutorial: Instance Segmentation using maskRCNN

Instance segmentation is identifying each object instance for every known object within an image. Instance segmentation assigns a label to each pixel of the image. It can be used for tasks such as counting the number of objects. [reference: https://towardsdatascience.com/computer-vision-instance-segmentation-with-mask-r-cnn-7983502fcad1]

Instance segmentation requires:

1. Object detection of all objects in an image. Here the goal is to classify individual objects and localize each object instance using a bounding box.
2. Segmenting each instance. Here the goal is to classify each pixel into a fixed set of categories without differentiating object instances. 

Taking an image of plant as an example. As shown in the image below, the 1st image is an RGB image of an arabidopsis, the one in the middle is image segmentation result, and the 3rd image is the result of instance segmentation. 
Now it is easy for us to tell that the goal for image segmentation is to have pixel level labels indicating "plant" or "not plant" for every pixel, and the output for image segmentation is a binary mask indicating where the plant is in the image. At this point we have no information regarding number of leaves in this image. 
While for instance segmentation, as shown in the 3rd image, we can see that the goal is to segment out every leaf (hence, there is a label for every leaf, e.g. leaf 1, leaf 2, etc.) instance. In this specific example, 5 binary masks would be generated, every one represents for one leaf. Hence we are also able to tell that there are 5 leaves present in this image. 

![Screenshot](img/tutorial_images/instance_segmentation/original.jpg)
![Screenshot](img/tutorial_images/instance_segmentation/threshold.jpg)
![Screenshot](img/tutorial_images/instance_segmentation/instance_seg.jpg)


There are plenty of methods for instance segmentation, instance segmentation using maskRCNN is shown here as an example. 

For detailed information regrading maskRCNN, please check here:
https://github.com/matterport/Mask_RCNN

Follow the installation steps, and it is highly recommended to create a conda environment for mask_rcnn.

- Create a conda environment with tensorflow 1.13.1 and keras 2.1.0.
    - Open a terminal window, type:
```
    conda create -n mrcnn tensorflow=1.13.1
    conda activate mrcnn
    pip install keras==2.1.0
    conda install plantcv # install plantcv tools for this environment
```
This would create a tensorflow environment (with tensorflow 1.13.1 and keras 2.1.0, those are required by the MaskRCNN package we are to install) with a name of mrcnn. You are free to change the name "mrcnn" based on you own preference. 

- Install MaskRCNN
    - Clone [this](https://github.com/matterport/Mask_RCNN) github repository to your desired location. (It is suggested to put the same directory as you put your plantcv folder)
    - Open a terminal, follow the instructions below:
    
```
    cd Mask_RCNN # direct yourself to the folder of Mask_RCNN
    pip install -r requirements.txt # install dependencies
    python3 setup.py install # run setup
```   
     
- (Option) Install pycocotools.
    - Clone [this](https://github.com/cocodataset/cocoapi) github repository, and put to your desired destiny location. 
    - Open a terminal window, type:
```
    pip install pycocotools
```

With conda environment mrcnn activated (```conda activate mrcnn```), you are ready to get instance level segmentation with Mask_RCNN using a pre-trained model. You can find the download the pre-trained model here:
/home/nfahlgren/projects/mrcnn/mask_rcnn_leaves_0060.h5

It is recommended that you put this pre-trained model in the same folder of your project. 

Following this notebook for step-by-step implementation of instance segmentation.

```python 
# import packages 
import os
import inferencing_utilities as funcs
```

The following block is where you want to change based on your own application:
```python
## suffix of original image files. Make sure that all files have the same suffix format
suffix = 'crop-img17.jpg'

## pattern for the date-tima part in your data. Make sure that the date-time part in all filenames follow the same pattern
pattern_datetime = '\d{4}-\d{2}-\d{2}-\d{2}-\d{2}'

## directory of original images
imagedir = '/shares/mgehan_share/acasto/auto_crop/output_10.1.9.214_wtCol'

## desired saving directory for results
savedir = '/shares/mgehan_share/hsheng/projects/maskRCNN/results/output_10.1.9.214_wtCol/plant17/segmentation'
if not os.path.exists(savedir):
    os.makedirs(savedir)

## class names. Since a pre-trained model is used here, and the model is trained with 2 classes: either "Background" or "Leaf", there is really nothing to change here
class_names = ['BG', 'Leaf']
```

Some detailed regarding parameters "suffix":

For the next several blocks, there is really nothing for you to change. 
```python
## Root directory of the project
rootdir = os.path.abspath("./")

## initialize the instance segmentation
instance_seg =  funcs.instance_seg_inferencing(imagedir, savedir, rootdir, pattern_datetime, suffix, class_names)

## get configuration for instance segmentation
instance_seg.get_configure()

## load the pre-trained model
instance_seg.load_model()

## pre-define colors for visualization used later
instance_seg.define_colors()

## get the list of all files
instance_seg.get_file_list()

## option (print the file list)
instance_seg.list_f
```

For the next block, a randomly selected example is used to show the instance segmentation result
```python
## show one randomly selected image as an example
instance_seg.inferencing_random_sample()
```

If you run the following block, it will loop over all files in the file list you defined. Note it might take some time for the process to finish.
```python
## get the result of all images
instance_seg.inferencing_all()
```

If you would like to check the results inside the folder, you can print out the directory for results saving:
```python
instance_seg.segmentation_dir
```


