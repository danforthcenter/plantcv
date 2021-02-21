# Exercise 1: Overview of the Acute pseudo-landmarking 

This is an introduction to the pseudo-landmarking method based around the acute function found within PlantCV. This tool is designed for morphometric analysis which due to it's relative simplicity can easily scale between different datasets in order to capture informative shape data in the form of de novo landmarks.  This notebook serves as demonstration of the image data curration required by acute and also documents the initial outputs of acute which can be used either to optimzie this workflow. Later exercises will build off of what is covered within this document in order to show the potential of this method to end users. To begin, let's start by loading the modules we'll need and then take stock of the acute function and how it operates by running help to see what inputs it requires...


```python
import cv2
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plantcv.plantcv.plm_homologies.acute import acute

debug = True 

help(acute)
```

    Help on function acute in module plantcv.plantcv.plm_homologies.acute:
    
    acute(obj, mask, win, threshold, debug)
        acute: identify landmark positions within a contour for morphometric analysis
        
        Inputs:
        obj         = An opencv contour array of interest to be scanned for landmarks
        mask        = binary mask used to generate contour array (necessary for ptvals)
        win         = maximum cumulative pixel distance window for calculating angle
                      score; 1 cm in pixels often works well
        thresh      = angle score threshold to be applied for mapping out landmark
                      coordinate clusters within each contour
        debug       = Debugging mode enabled/disabled for use in troubleshooting
        
        Outputs:
        homolog_pts = pseudo-landmarks selected from each landmark cluster
        start_pts   = pseudo-landmark island starting position; useful in parsing homolog_pts in downstream analyses
        stop_pts    = pseudo-landmark island end position ; useful in parsing homolog_pts in downstream analyses
        ptvals      = average values of pixel intensity from the mask used to generate cont;
                      useful in parsing homolog_pts in downstream analyses
        chain       = raw angle scores for entire contour, used to visualize landmark
                      clusters
        verbose_out = supplemental file which stores coordinates, distance from
                      landmark cluster edges, and angle score for entire contour.  Used
                      in troubleshooting.
        
        :param obj: ndarray
        :param mask: ndarray
        :param win: int
        :param thresh: int
        :return homolog_pts:
    


# Required image input variables
We'll need 4 variables for each image we run.  Two are derived from the image itself, a contour array representing the outline of a plants image mask (obj) and the image mask itself which is used for output purposes (mask). 

Let's first start by creating these first two objects. To begin, let's load our first image from a time series sequence.


```python
day=10

path='/Users/johnhodge/Documents/GitHub/Doust-lab-workflows/plm_tutorial/'
name='B100_rep1_d'+str(day)

img = cv2.imread(path+name+'.jpg')

#Plot results
fig1=plt.figure(figsize=(6, 8))
fig1=plt.imshow(img)
fig1=plt.xscale('linear')
fig1=plt.axis('off')
fig1=plt.title('B100 day '+str(day))
plt.show(fig1)
```


![png](output_3_0.png)


# Reviewing our loaded image

From what we can see, the plant is on a mostly homogeneous white background. It should be relatively easy to use the color channel differences to threshold the pixels representing our plant from the rest of the image to create our mask.  To begin let's take a look at the color channels to see which will be the most useful.



```python
lab_img=cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
hsv_img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

img_hsv_lab_colorspaces = cv2.hconcat((lab_img, hsv_img))

#Plot results
fig1=plt.figure(figsize=(12, 8))
fig1=plt.imshow(img_hsv_lab_colorspaces)
fig1=plt.xscale('linear')
fig1=plt.axis('off')
fig1=plt.title('Images of \'Lab\' and \'HSV\' color spaces respectively')
plt.show(fig1)
```


![png](output_5_0.png)


# Selecting color channels for thresholding

In comparing the 'Lab' and 'HSV' color spaces it appears there's a bit more contrast to work within the HSV space, but that soil near the stage for the pot could be a problem.  With that in mind the 'Lab' color space is our best bet. Let's take a look at which individual channels are the most informative...


```python
img_l, img_a, img_b = cv2.split(lab_img)

img_lab_channels = cv2.hconcat((img_l, img_a, img_b))

#Plot results
fig1=plt.figure(figsize=(21, 10))
fig1=plt.imshow(img_lab_channels, 'gray')
fig1=plt.xscale('linear')
fig1=plt.axis('off')
fig1=plt.title('Grayscale images of \'L\', \'a\', and \'b\' channels respectively')
plt.show(fig1)
```


![png](output_7_0.png)


# Binary thresholding

The 'L' channel unfortunately doesn't appear to help very much in denoting the plant pixels from the background.  However, there's good signal in the 'a' channel (darker pixels) and the 'b' channel (brighter pixels) so using a conjunction of these two grayscale images should give us a reasonable mask to work with!


```python
#These threshold bounds will provide the best signal but feel free to experiment!
a_bound = np.array([123, 255])
b_bound = np.array([133, 255])

#Note that we're inverting the binary threshold of color channel 'a' so that the areas 
#with the darkest pixels will be flagged as a white mask.  This will be important when 
#compared against the mask generated from color channel 'b'. 
mask_a = cv2.threshold(img_a, a_bound[0], a_bound[1], cv2.THRESH_BINARY_INV)
a_thresh = cv2.cvtColor(mask_a[1], cv2.COLOR_GRAY2RGB)

mask_b = cv2.threshold(img_b, b_bound[0], b_bound[1], cv2.THRESH_BINARY)
b_thresh = cv2.cvtColor(mask_b[1], cv2.COLOR_GRAY2RGB)

img_ab_thresholds = cv2.hconcat((a_thresh, b_thresh))

#Plot results
fig1=plt.figure(figsize=(12, 8))
fig1=plt.imshow(img_ab_thresholds, 'gray')
fig1=plt.xscale('linear')
fig1=plt.axis('off')
fig1=plt.title('Binary images of \'a\' and \'b\' thresholds respectively')
plt.show(fig1)
```


![png](output_9_0.png)


# Merging binary thresholds into our mask

In both cases we have a few stray pixels (more so in mask a), but we're certainly on the right track! Now lets go ahead and identify which pixels these thresholds can agree on keeping.


```python
mask=cv2.bitwise_and(mask_a[1], mask_b[1])

#Plot results
fig1=plt.figure(figsize=(6, 8))
fig1=plt.imshow(mask, 'gray')
fig1=plt.xscale('linear')
fig1=plt.axis('off')
fig1=plt.title('Merged mask')
plt.show(fig1)
```


![png](output_11_0.png)


# Extracting OpenCV image contour arrays

Now with our merged mask defining the shape our our plant we can extract our contour to use for pseudo-landmark identification. This will be done through the use of the findContours function latent to openCV where we will use a simple approximation (to make this step less computationally intensive) and a tree hierarchy will be extracted as well (important for images in which internal volumes resulting from crossovers between structures occurs). 

Although not necessary yet in this demonstration the steps below demonstration how the plants outer contour is defined based on which bears the largest volume. Contours contained within this 'parent' contour are then stored as well for downstream analysis within a contour list. This will effectively exclude other components of the mask unrelated to our plant.


```python
cont, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

mask_contour = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

#Find largest contour of subject (outer boundary of subject)
cont_list = []
hull = [0, 0]
for c in range(len(cont)):
    a = cv2.contourArea(cont[c])
    if a > hull[0]:
        hull = [a, c]

cont_list.append(hull[1])
#Capture children of parent contour
for e in range(len(hierarchy[0])):
    if (hierarchy[0][e][3] == hull[1]) & (len(cont[e]) > 10):
        cont_list.append(e)

#Draw the individual contour outlines onto the duplicate mask in a purple hue
for c in cont_list:
    cv2.drawContours(mask_contour, cont[c], -1, (180, 0, 180), 8)

#Plot results
fig1=plt.figure(figsize=(6, 8))
fig1=plt.imshow(mask_contour)
fig1=plt.xscale('linear')
fig1=plt.axis('off')
fig1=plt.title('Plant contour (purple)')
plt.show(fig1)
```


![png](output_13_0.png)


# Acute pseudo-landmark identification

Now that we have our contours we can come back to the previous two input parameters of acute which we have thus far ignored but are key to it's functionality.  Acute operates using a modified form of chain-coding akin to a navigators compass taking steps along a contour and within a local window two bounding points on either side of this window are defined from which an angle score can be calculated for the vertex of the 3 points.  The size of this local window is defined as a pixel distance using the 'win' variable.  Following the calculation of this angle score it is then weighed against a threshold that is stored in our last variable 'thresh' allowing for features of interest to be defined de novo.  Given that acute regions are often areas of interest for morphometric analysis setting this threshold to maximize the 'acuteness' of the contour serves to provide a relatively simple way to identify pseudo-landmarks. 

When specifying 'win' it is often best to select a value which is at least half the distance of the smallest feature in the plant that is deemed relevant.  In the case of Setaria which we are using in this demonstration the first leaf is usually 2 cm long so selecting a window size <=1 cm is optimal to prevent conflict between adjacent landmarks along the contour.

When specifying 'thresh' the best practice is to leave this value at 90 given in order to identify acute regions. However, to provide downstream flexibility this parameter has the capacity to use other user defined values in case more stringent or lax thresholds are required.


```python
win=25
thresh=90
```

# Running acute in debugging mode

As is standard with other PlantCV packages acute is built with debugging features that produces verbose outputs for the sake of troubleshooting. Given this is our first attempt at running this function lets go ahead and run it with debugging enabled to see what these outputs are... 

*Note: while iterating through the contour list isn't necessary for a single outline as we have here this step is invaluable in later stages where volumes internal to our plant outline are present.


```python
landmark_output=[]

for l in cont_list:
    if cv2.arcLength(cont[l],True) > 2*win:
        print('Contour volume: '+str(cv2.arcLength(cont[l],True)))

        cv2.drawContours(mask, cont[l], -1, (128,0,0), 3)
        homolog_pts, homolog_start, homolog_stop, homolog_cc, chain, verbose = acute(cont[l], mask, win, thresh, debug)
        homolog_hier = l*len(homolog_pts)
        cv2.drawContours(mask, homolog_pts, -1, (0,0,255), 3)
        print('    ' + 'landmark number: ' + str(len(homolog_pts)))

        for h in range(0,len(homolog_pts)):
            landmark_output.append([name, homolog_pts[h][0][0], homolog_pts[h][0][1], homolog_start[h][0][0], homolog_start[h][0][1], homolog_stop[h][0][0], homolog_stop[h][0][1], homolog_cc[h],])


```

    Contour volume: 2134.4002673625946
    Fusing contour edges
        landmark number: 8


    /Users/johnhodge/Documents/GitHub/plantcv/plantcv/plantcv/plm_homologies/acute.py:175: FutureWarning: Using a non-tuple sequence for multidimensional indexing is deprecated; use `arr[tuple(seq)]` instead of `arr[seq]`. In the future this will be interpreted as an array index, `arr[np.array(seq)]`, which will result either in an error or a different result.
    /Users/johnhodge/Documents/GitHub/plantcv/plantcv/plantcv/plm_homologies/acute.py:176: FutureWarning: Using a non-tuple sequence for multidimensional indexing is deprecated; use `arr[tuple(seq)]` instead of `arr[seq]`. In the future this will be interpreted as an array index, `arr[np.array(seq)]`, which will result either in an error or a different result.


# Acute angle score chain-code output

We did quite a bit of work just above so let's go ahead and try to break it down item by item.  To start we successfully ran acute which used it's chain coding based scoring method to identify landmarks (8 in this example).  However we started with several hundred vertices comprising our outline (the purple dots we saw earlier) so how did we reduce those down to 8 pseudo-landmarks!? 

Acute actually undergoes an extra step beyond simply calculating angle scores in that it attempts to identify 'islands' of acute points and upon finding these regions it approximates the best mid point of each location within the contour. Let's have a look at our contour described by it's acute angle scores...


```python
chain_pos=range(0, len(chain))

fig, (fig1, fig2) = plt.subplots(1, 2, figsize=(12, 6))

#Plot results
fig1.plot(chain_pos, chain, color='black')
fig1.axhline(y=thresh, color='r', linestyle='-')
fig1.set_title('Angle scores by position')

fig2.hist(chain, color='black')
fig2.axvline(x=thresh, color='r', linestyle='-')
fig2.set_title('Angle score histogram')

plt.show(fig)
```


![png](output_19_0.png)


If we focus on our first graph on the left the black line representing the individual acute angle scores of each vertex along our contour outline we can see there definitely seems to be a waveform that quickly decays to zero as we hit each acute island. It's also probably apparent we're actually splitting on of these islands in half at either end of our chain in linearizing this output.  The 'Fusing contour edges' step acute does automatically (appeared in the output panel) is performed to remedy mistaking these two segments as different regions. 

When we compare these regions to our threshold (the red line) it becomes clear these 'waves' correspond to our landmarks.  If we felt a particular need to optimize this threshold since we should optimally have a bimodal output a histogram of the angle scores can be generated as shown on the right to train this threshold in order to better optimize signal.


Now that we have a general idea of how acute is determining it's primary outputs let's see how they compare to our original image...


```python
img_plms = img.copy()

for c in cont_list:
    cv2.drawContours(img_plms, homolog_pts, -1, (255, 255, 255), 14)    

#Plot results
plm_fig=plt.figure(figsize=(7, 10))
plm_fig=plt.imshow(img_plms)
plm_fig=plt.xscale('linear')
plm_fig=plt.axis('off')
plm_fig=plt.title('B100 day '+str(day))
plt.show(plm_fig)
```


![png](output_21_0.png)


In viewing our plms plotted in white while looking back on our original image we used for this exercise we can see that not only were we able to clearly define regions of interest using a threshold on our angle score waveforms but these do in fact appear to correlate with regions of interest for morphometric analysis such as the tips of leaves as well as the ligules where the base of each leaf attaches to the culm (the grass equivalent to a stem).  This is the basis by which acute functions and serves as the basic mode of operation for this workflow.  In the next exercise 2 we will expand on this knowledge by learning to interact with and store time series data which in exercise 3 can subsequently be fused together into homology groups.  


```python

```
