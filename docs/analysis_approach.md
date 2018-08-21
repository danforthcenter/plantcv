## Approaches to Image Analysis with PlantCV

The following are suggestions on how to approach image analysis with PlantCV. 

###**Image Processing Goals**

When starting an image-based phenotyping project it is important to consider what the end goals of the project are.
This is important because the goals of the project will determine the the camera type, imaging layout, and will help to 
guide downstream analysis. For example, if the goal of the project is to quantify the growth rates of a population of 
Arabidopsis plants, you may want to take timelapse images of whole flats of plants with an RGB (VIS) camera. If it was 
an experiment focused on drought of maize plants and your goal was to get information about water content of plants you
might want to take side-view and top-view images of a single plant with a near-infrared camera. If the goal of the 
project is to classify disease symptoms on leaves then you may want to use a scanner to take detailed images of leaf 
tissue. 

###**Image Layout Considerations**

It is a good idea to capture a test image and process it using PlantCV (or any other software that you might use) 
before capturing a full set of data. It is ALWAYS best to try to reduce potential image processing problems up front, 
rather than to try to process 'bad' / inconsistent images. Things to think about:

*  If color is analyzed, do you need a color card for color correction in each image?
*  If lighting is changing do you need a color card / white balance card to 'normalize' lighting across images?
*  Is the camera set at exactly the same vantage point in each image or do you need a size marker?
*  Is there enough contrast between the target object (plant) and the background or do you need to add materials to 
increase contrast (blue material for example).
*  If you are going to image more than one plant in an image, how long before the plants overlap each other? Is this 
long enough for the trait you are interested in?

###**Developing Image Processing Workflows (Pipeline Development)**

There are two major steps to developing an image analysis pipeline:

1.  Object segmentation (detection/isolation) - This is likely a multi-step process. There are many ways to approach 
object segmentation, we detail those approaches below.
2.  Object analysis - Analysis on isolated objects, the categories of object analysis are below.

We primarily use Jupyter notebooks for pipeline development, and there is more information about using Jupyter 
notebooks [here](jupyter.md). Once a pipeline has been developed for one image, it's best to test it on other images in 
the dataset to determine how robust the pipeline will be. Example pipelines and tutorials are available and are meant 
to demonstrate how modules can be used. Keep in mind that modules can be linked together in a variety of different 
configurations to meet image processing goals so the tutorials simply examples of a few approaches:

*  [VIS Image Pipeline](vis_tutorial.md)
*  [NIR Image Pipeline](nir_tutorial.md)
*  [PSII Pipeline](psII_tutorial.md)
*  [VIS / NIR Dual Pipeline](vis_nir_tutorial.md)
*  [Multi Plant Tutorial](multi-plant_tutorial.md)
*  [Machine Learning Tutorial](machine_learning_tutorial.md)
*  [Color Correction Tutorial](transform_color_correction_tutorial.md)

####**1. Methods of Isolating Target Objects**

Regardless of the objective of the experiment, it will likely be necessary to segment features of interest in 
the image (likely the plant material in the image). Isolating the target object or objects can be approached a number 
of different ways in PlantCV.

##### Image Normalization

*  White balancing an image can help to reduce variation between images due to overall lighting changes. This may help 
downstream image processing steps like thresholding to be the same between images.

#####Object Segmentation Approaches

*  Thresholding method (auto or manual) - A single channel of an image is selected for either 
[binary thresholding](binary_threshold.md) or auto thresholding ([Gaussian](gaussian_threshold.md), 
[mean](mean_threshold.md), [Otsu](otsu_threshold.md), or [triangle](triangle_threshold.md)). For a color image, 
selecting a channel of an image for thresholding likely involves conversion from RGB to [HSV](rgb2hsv.md) or 
[LAB](rgb2lab.md) colorspace, then selecting Hue, Saturation, Value, Lightness, Green-Magenta, or Blue-Yellow channels. 
It's best to select a channel that maximizes contrast between the target object and the background. When thresholding 
an image to segment a target object, it may not be possible to isolate just the target object. Multiple thresholding 
steps on various channels may be necessary as well as downstream noise reduction steps. For an example of this approach 
see the [VIS Image Pipeline](vis_tutorial.md). 

*  Background subtraction method - This approach can be used if there are 'null' images (images with everything but the 
object in them). The null image can be a single image, or an averaged background image. For more information on 
background subtraction see [the background subtraction function](background_subtraction.md). There still may need to be 
noise reduction steps following the background subtraction method.

*  Machine Learning (classification) methods - For these approaches, target objects can be segmented after a training 
set is built (the training set might need to be built using background subtraction or thresholding methods). Once the 
training set is built, the trained classifier is used to segment the features of interest. See the 
[machine learning tutorial](machine_learning_tutorial.md) and the [naive bayes function](naive_bayes.md) for more 
information. There still may need to be noise reduction steps following machine learning-based segmentation.

#####Noise Reduction 

*  After a thresholding, background subtraction, or a machine learning approach for object segmentation, there will 
likely be some 'noise' (non-target-object spots) in the image. Those can be filled in using modules like fill or blur 
(median blur or Gaussian blur). Keep in mind that filling in noise can be a very slow step if there are too many 
non-target objects to evaluate. If the step seems to be taking too long (longer than 30 seconds for example), then you 
should check previous steps to see if it is possible to reduce noise further before using a fill (for example consider 
doing a threshold on a different channel then joining the two channels with a Logical operation like an 
['And'](logical_and.md)).

#####Region of Interest

*  To further isolate an object from surrounding background a region of interest can be used to select the region of 
the image that contains the target object. To do this you first [detect all the objects](find_objects.md) in the image, 
then define the [region of interest](roi_rectangle.md), then determine if the objects are  within, touching, or outside of 
the region of interest with the [roi_objects function](roi_objects.md).

#####Connecting Objects or Splitting Objects

*  Once the target object or objects are segmented you then need to decide if it is desirable to connect or split the 
objects.
*  Even if there is a single plant in an image it may be detected as multiple objects, in which case it may need to be
joined or composed together using the [object_composition function](object_composition.md).
*  If there are multiple plants in an object and you would like to analyze them individually (get shape parameters for 
each plant for example) then there are functions in PlantCV to split the image apart so there is a single target object 
in each sub-image. For more information on this process see the [Multi Plant Tutorial](multi-plant_tutorial.md). 

####**2. Object Analysis in PlantCV**
    
These are the general categories of object analysis that are available in PlantCV  

*  Object shape parameters: see the [analyze_shape](analyze_shape.md) and [analyze_bound](analyze_bound_horizontal.md) functions.
*  Object color or other signal intensity values: see the [analyze_color](analyze_color.md), 
[analyze_NIR_intensity](analyze_NIR_intensity.md), and [fluor_fvfm](fluor_fvfm.md) functions.
*  Object classification (For example, classification of disease symptoms, identification of organ structures 
[naive-bayesian multiclass mode](naive_bayes_multiclass.md)).

For a detailed list of types of PlantCV measurement outputs see 
['Summary of Output Measurements'](output_measurements.md).

### Parallelizing Pipelines

*  Once a satisfactory pipeline has been developed and tested, the next step is to translate it from a Jupyter notebook 
to a Python script. For detailed instructions see the 
[Using Jupyter Notebooks](jupyter.md) page. 
*  Once the Jupyter notebook has been translated to a Python script (and tested!) the next step is to parallelize that 
script over a set of images. To do this follow the [pipeline parallelization instructions](pipeline_parallel.md). 
 
### Troubleshooting

Recommendations for troubleshooting.

1.  If you run into an error, first use the error message as Google search terms to see if anyone else has run into 
(and solved) a similar problem. This isn't snark, the internet is a magical place.
2.  If your problem isn't solved after a search post an issue on GitHub 
[here](https://github.com/danforthcenter/plantcv/issues). It's possible that you have discovered a bug, or there is a 
use error.
3.  When posting an issue on GitHub the community can better help you if you provide detailed information. If you have 
triggered an error be sure to paste in the error message, the situation that you think triggered that error message, 
and what you are trying to do (end goal). 
4.  If you are having issues processing a specific image it is also fine to post on GitHub 
[here](https://github.com/danforthcenter/plantcv/issues). But again, be sure to include the image, the specific problem 
you are having and the end goal. Also, make sure you have looked over the available tutorials.
