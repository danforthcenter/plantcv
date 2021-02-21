# Exercise 3: Generating homology groups from pseudo-landmark data

In this third exercise we will review one of the downstream applications of our batch plm data we generated in our previous exercise by generating de novo homology groups.  It should be noted that this method, while incredibly powerful, has some prior assumptions in it's usage.  To drive home the point, THIS METHOD IS DESIGNED TO ESTIMATE GROUPS BY MAKING ASSUMPTIONS ABOUT BIOLOGICAL HOMOLOGY (i.e. not persistent homology which is an completely different analytical method!).  

Ideally, when image data of sufficient quality is presented to this workflow homology groups could even be inferred to be orthologous to one another although, similar to (phylo)genetic clustering methods, you get out what you put in and so this may be subjective based on your dataset.  That being said, there are concievably two datasets where this homology grouping set is applicable:

1) Linking landmarks through time series image data to survey growth and development of independent structures through time.

2) Linking landmarks between comparable static materials either between individuals or genotypes for comparing variability of these landmarks in analogous organismal datasets (i.e. leaves with readily apparent lobes, awns, or sinuses, as one example).

Given our homology grouping workflow was designed for the former dataset we will work through a demonstration of how this works and how best to go about performing this analysis in an idealized dataset.  Let's get started by importing what we need...


```python
import cv2
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from plantcv.plantcv.homology.acute import acute
from plantcv.plantcv.homology.space import space
from plantcv.plantcv.homology.starscape import starscape
from plantcv.plantcv.homology.constella import constella

win=25
thresh=90
debug = True 

path='/Path/To/Images/plm_tutorial/'
days=range(10,14)
name_prefix='B100_rep1_d'

group_iter = 1
```

#### Before we get rolling though we'll have you enter in a output file path to save some graphs this workflow will generate which will be appended to our output prefix.


```python
outpath='/Path/To/Output/Directory/'
outfile_prefix = outpath+'B100_d10_d11_test'
```

Now that we have what we need to rerun the script we walked through in the previous exercise let's run through the code block we covered last time and then think about how best to move forward with our landmark outputs.


```python
landmark_output=[['group', 'plmname', 'filename', 'plm_x', 'plm_y', 'SS_x', 'SS_y', 'TS_x', 'TS_y', 'CC_ratio']]

for day in days:

    #1. Reading our image into the environment

    img = cv2.imread(path+name_prefix+str(day)+'.jpg')

    #2. Converting our RGB image into an Lab color space

    lab_img=cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    #3. Splitting our Lab image into separate color spaces

    img_l, img_a, img_b = cv2.split(lab_img)

    img_lab_channels = cv2.hconcat((img_l, img_a, img_b))

    #4. Thresholding our a and b color channels to create two masks

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

    #5. Merging our individual a and b thresholded masks

    mask=cv2.bitwise_and(mask_a[1], mask_b[1])

    #6. Extracting our contours from the final mask

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

    #7. Extracting pseudo-landmarks from the plant contours
    for l in cont_list:
        if cv2.arcLength(cont[l],True) > 2*win:
            print('Contour volume: '+str(cv2.arcLength(cont[l],True)))

            cv2.drawContours(mask, cont[l], -1, (128,0,0), 3)
            homolog_pts, homolog_start, homolog_stop, homolog_cc, chain, verbose = acute(cont[l], mask, win, thresh, debug)
            homolog_hier = l*len(homolog_pts)
            cv2.drawContours(mask, homolog_pts, -1, (0,0,255), 3)
            print('    ' + 'landmark number: ' + str(len(homolog_pts)))

            for h in range(0, len(homolog_pts)):
                landmark_output.append([None, name_prefix+str(day)+'_plm'+str(h+1), name_prefix+str(day), homolog_pts[h][0][0], homolog_pts[h][0][1], homolog_start[h][0][0], homolog_start[h][0][1], homolog_stop[h][0][0], homolog_stop[h][0][1], homolog_cc[h],])

#Convert out output to a pandas dataframe for ease of use hereafter...
landmark_pandas=pd.DataFrame(landmark_output[1:len(landmark_output)], columns=landmark_output[0][0:11])

```

    Contour volume: 2134.4002673625946
    Fusing contour edges
    route C
    Landmark site:  1125  , Start site:  1113  , Term. site:  19
    Landmark point indices:  [1125]
    Starting site indices:  [1113]
    Termination site indices:  [19]
    route C
    Landmark site:  203  , Start site:  188  , Term. site:  221
    Landmark point indices:  [1125, 203]
    Starting site indices:  [1113, 188]
    Termination site indices:  [19, 221]
    route C
    Landmark site:  353  , Start site:  337  , Term. site:  363
    Landmark point indices:  [1125, 203, 353]
    Starting site indices:  [1113, 188, 337]
    Termination site indices:  [19, 221, 363]
    route C
    Landmark site:  538  , Start site:  531  , Term. site:  547
    Landmark point indices:  [1125, 203, 353, 538]
    Starting site indices:  [1113, 188, 337, 531]
    Termination site indices:  [19, 221, 363, 547]
    route C
    Landmark site:  594  , Start site:  571  , Term. site:  602
    Landmark point indices:  [1125, 203, 353, 538, 594]
    Starting site indices:  [1113, 188, 337, 531, 571]
    Termination site indices:  [19, 221, 363, 547, 602]
    route C
    Landmark site:  672  , Start site:  655  , Term. site:  689
    Landmark point indices:  [1125, 203, 353, 538, 594, 672]
    Starting site indices:  [1113, 188, 337, 531, 571, 655]
    Termination site indices:  [19, 221, 363, 547, 602, 689]
    route C
    Landmark site:  809  , Start site:  795  , Term. site:  824
    Landmark point indices:  [1125, 203, 353, 538, 594, 672, 809]
    Starting site indices:  [1113, 188, 337, 531, 571, 655, 795]
    Termination site indices:  [19, 221, 363, 547, 602, 689, 824]
    route C
    Landmark site:  895  , Start site:  877  , Term. site:  908
    Landmark point indices:  [1125, 203, 353, 538, 594, 672, 809, 895]
    Starting site indices:  [1113, 188, 337, 531, 571, 655, 795, 877]
    Termination site indices:  [19, 221, 363, 547, 602, 689, 824, 908]
        landmark number: 8
    Contour volume: 2406.708920955658
    Fusing contour edges
    route C
    Landmark site:  1180  , Start site:  1166  , Term. site:  7
    Landmark point indices:  [1180]
    Starting site indices:  [1166]
    Termination site indices:  [7]
    route C
    Landmark site:  167  , Start site:  153  , Term. site:  180
    Landmark point indices:  [1180, 167]
    Starting site indices:  [1166, 153]
    Termination site indices:  [7, 180]
    route C
    Landmark site:  237  , Start site:  224  , Term. site:  249
    Landmark point indices:  [1180, 167, 237]
    Starting site indices:  [1166, 153, 224]
    Termination site indices:  [7, 180, 249]
    route C
    Landmark site:  331  , Start site:  316  , Term. site:  346
    Landmark point indices:  [1180, 167, 237, 331]
    Starting site indices:  [1166, 153, 224, 316]
    Termination site indices:  [7, 180, 249, 346]
    route C
    Landmark site:  474  , Start site:  462  , Term. site:  484
    Landmark point indices:  [1180, 167, 237, 331, 474]
    Starting site indices:  [1166, 153, 224, 316, 462]
    Termination site indices:  [7, 180, 249, 346, 484]
    route C
    Landmark site:  652  , Start site:  642  , Term. site:  656
    Landmark point indices:  [1180, 167, 237, 331, 474, 652]
    Starting site indices:  [1166, 153, 224, 316, 462, 642]
    Termination site indices:  [7, 180, 249, 346, 484, 656]
    route C
    Landmark site:  709  , Start site:  689  , Term. site:  722
    Landmark point indices:  [1180, 167, 237, 331, 474, 652, 709]
    Starting site indices:  [1166, 153, 224, 316, 462, 642, 689]
    Termination site indices:  [7, 180, 249, 346, 484, 656, 722]
    route C
    Landmark site:  782  , Start site:  759  , Term. site:  791
    Landmark point indices:  [1180, 167, 237, 331, 474, 652, 709, 782]
    Starting site indices:  [1166, 153, 224, 316, 462, 642, 689, 759]
    Termination site indices:  [7, 180, 249, 346, 484, 656, 722, 791]
    route C
    Landmark site:  893  , Start site:  881  , Term. site:  906
    Landmark point indices:  [1180, 167, 237, 331, 474, 652, 709, 782, 893]
    Starting site indices:  [1166, 153, 224, 316, 462, 642, 689, 759, 881]
    Termination site indices:  [7, 180, 249, 346, 484, 656, 722, 791, 906]
    route C
    Landmark site:  974  , Start site:  965  , Term. site:  982
    Landmark point indices:  [1180, 167, 237, 331, 474, 652, 709, 782, 893, 974]
    Starting site indices:  [1166, 153, 224, 316, 462, 642, 689, 759, 881, 965]
    Termination site indices:  [7, 180, 249, 346, 484, 656, 722, 791, 906, 982]
        landmark number: 10
    Contour volume: 2661.887634396553
    Fusing contour edges
    route C
    Landmark site:  0  , Start site:  1352  , Term. site:  9
    Landmark point indices:  [0]
    Starting site indices:  [1352]
    Termination site indices:  [9]
    route C
    Landmark site:  180  , Start site:  165  , Term. site:  186
    Landmark point indices:  [0, 180]
    Starting site indices:  [1352, 165]
    Termination site indices:  [9, 186]
    route C
    Landmark site:  301  , Start site:  286  , Term. site:  318
    Landmark point indices:  [0, 180, 301]
    Starting site indices:  [1352, 165, 286]
    Termination site indices:  [9, 186, 318]
    route C
    Landmark site:  458  , Start site:  448  , Term. site:  481
    Landmark point indices:  [0, 180, 301, 458]
    Starting site indices:  [1352, 165, 286, 448]
    Termination site indices:  [9, 186, 318, 481]
    route C
    Landmark site:  610  , Start site:  601  , Term. site:  627
    Landmark point indices:  [0, 180, 301, 458, 610]
    Starting site indices:  [1352, 165, 286, 448, 601]
    Termination site indices:  [9, 186, 318, 481, 627]
    route C
    Landmark site:  787  , Start site:  778  , Term. site:  800
    Landmark point indices:  [0, 180, 301, 458, 610, 787]
    Starting site indices:  [1352, 165, 286, 448, 601, 778]
    Termination site indices:  [9, 186, 318, 481, 627, 800]
    route C
    Landmark site:  846  , Start site:  830  , Term. site:  851
    Landmark point indices:  [0, 180, 301, 458, 610, 787, 846]
    Starting site indices:  [1352, 165, 286, 448, 601, 778, 830]
    Termination site indices:  [9, 186, 318, 481, 627, 800, 851]
    route C
    Landmark site:  902  , Start site:  889  , Term. site:  919
    Landmark point indices:  [0, 180, 301, 458, 610, 787, 846, 902]
    Starting site indices:  [1352, 165, 286, 448, 601, 778, 830, 889]
    Termination site indices:  [9, 186, 318, 481, 627, 800, 851, 919]
    route C
    Landmark site:  1033  , Start site:  1015  , Term. site:  1046
    Landmark point indices:  [0, 180, 301, 458, 610, 787, 846, 902, 1033]
    Starting site indices:  [1352, 165, 286, 448, 601, 778, 830, 889, 1015]
    Termination site indices:  [9, 186, 318, 481, 627, 800, 851, 919, 1046]
    route C
    Landmark site:  1127  , Start site:  1113  , Term. site:  1134
    Landmark point indices:  [0, 180, 301, 458, 610, 787, 846, 902, 1033, 1127]
    Starting site indices:  [1352, 165, 286, 448, 601, 778, 830, 889, 1015, 1113]
    Termination site indices:  [9, 186, 318, 481, 627, 800, 851, 919, 1046, 1134]
        landmark number: 10
    Contour volume: 2923.1912364959717
    Fusing contour edges
    route C
    Landmark site:  0  , Start site:  1540  , Term. site:  13
    Landmark point indices:  [0]
    Starting site indices:  [1540]
    Termination site indices:  [13]
    route C
    Landmark site:  222  , Start site:  205  , Term. site:  245
    Landmark point indices:  [0, 222]
    Starting site indices:  [1540, 205]
    Termination site indices:  [13, 245]
    route C
    Landmark site:  370  , Start site:  355  , Term. site:  381
    Landmark point indices:  [0, 222, 370]
    Starting site indices:  [1540, 205, 355]
    Termination site indices:  [13, 245, 381]
    route C
    Landmark site:  590  , Start site:  579  , Term. site:  598
    Landmark point indices:  [0, 222, 370, 590]
    Starting site indices:  [1540, 205, 355, 579]
    Termination site indices:  [13, 245, 381, 598]
    route C
    Landmark site:  634  , Start site:  616  , Term. site:  653
    Landmark point indices:  [0, 222, 370, 590, 634]
    Starting site indices:  [1540, 205, 355, 579, 616]
    Termination site indices:  [13, 245, 381, 598, 653]
    route C
    Landmark site:  708  , Start site:  690  , Term. site:  722
    Landmark point indices:  [0, 222, 370, 590, 634, 708]
    Starting site indices:  [1540, 205, 355, 579, 616, 690]
    Termination site indices:  [13, 245, 381, 598, 653, 722]
    route C
    Landmark site:  833  , Start site:  832  , Term. site:  850
    Landmark point indices:  [0, 222, 370, 590, 634, 708, 833]
    Starting site indices:  [1540, 205, 355, 579, 616, 690, 832]
    Termination site indices:  [13, 245, 381, 598, 653, 722, 850]
    route C
    Landmark site:  916  , Start site:  908  , Term. site:  924
    Landmark point indices:  [0, 222, 370, 590, 634, 708, 833, 916]
    Starting site indices:  [1540, 205, 355, 579, 616, 690, 832, 908]
    Termination site indices:  [13, 245, 381, 598, 653, 722, 850, 924]
    route C
    Landmark site:  1173  , Start site:  1162  , Term. site:  1192
    Landmark point indices:  [0, 222, 370, 590, 634, 708, 833, 916, 1173]
    Starting site indices:  [1540, 205, 355, 579, 616, 690, 832, 908, 1162]
    Termination site indices:  [13, 245, 381, 598, 653, 722, 850, 924, 1192]
    route C
    Landmark site:  1357  , Start site:  1342  , Term. site:  1375
    Landmark point indices:  [0, 222, 370, 590, 634, 708, 833, 916, 1173, 1357]
    Starting site indices:  [1540, 205, 355, 579, 616, 690, 832, 908, 1162, 1342]
    Termination site indices:  [13, 245, 381, 598, 653, 722, 850, 924, 1192, 1375]
        landmark number: 10


Now that we have our analyses run again let's have another look at data to think about how we'll proceed...


```python
landmark_pandas.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
      <th>plmname</th>
      <th>filename</th>
      <th>plm_x</th>
      <th>plm_y</th>
      <th>SS_x</th>
      <th>SS_y</th>
      <th>TS_x</th>
      <th>TS_y</th>
      <th>CC_ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>None</td>
      <td>B100_rep1_d10_plm1</td>
      <td>B100_rep1_d10</td>
      <td>901</td>
      <td>1151</td>
      <td>894</td>
      <td>1171</td>
      <td>885</td>
      <td>1167</td>
      <td>179.786408</td>
    </tr>
    <tr>
      <th>1</th>
      <td>None</td>
      <td>B100_rep1_d10_plm2</td>
      <td>B100_rep1_d10</td>
      <td>786</td>
      <td>1423</td>
      <td>789</td>
      <td>1402</td>
      <td>772</td>
      <td>1404</td>
      <td>51.358025</td>
    </tr>
    <tr>
      <th>2</th>
      <td>None</td>
      <td>B100_rep1_d10_plm3</td>
      <td>B100_rep1_d10</td>
      <td>571</td>
      <td>1344</td>
      <td>592</td>
      <td>1336</td>
      <td>593</td>
      <td>1342</td>
      <td>136.758621</td>
    </tr>
    <tr>
      <th>3</th>
      <td>None</td>
      <td>B100_rep1_d10_plm4</td>
      <td>B100_rep1_d10</td>
      <td>793</td>
      <td>1523</td>
      <td>796</td>
      <td>1512</td>
      <td>783</td>
      <td>1519</td>
      <td>77.395349</td>
    </tr>
    <tr>
      <th>4</th>
      <td>None</td>
      <td>B100_rep1_d10_plm5</td>
      <td>B100_rep1_d10</td>
      <td>712</td>
      <td>1511</td>
      <td>735</td>
      <td>1508</td>
      <td>734</td>
      <td>1512</td>
      <td>165.041667</td>
    </tr>
  </tbody>
</table>
</div>



Thus far, we've largely been considering this data as a table where we really only cared about our X-Y coordinates that describe our plms. However, when we think about this matrix beyond the the filename and plm x/y columns we can see that we really have quite a few extra dimensions which add some context to our data.  These added dimensions were originally deemed to be potentially useful for generating a rich multivariate dataset to to pull these plms together into homology groups.  Space no longer is seen as a required component of this pipeline, however, given that analyses seem to only produce negligibly better results with it's inclusion.  That being said, this approach does produce some novel types of metadata which could have alternative applications so we'll at least discuss what Space is doing here in it's original context, even if we gloss over it in tutorial 4. You may have also noticed we now have a new empty column we've added that didn't exist before called 'group' but for now we'll just ignore it. 

To begin, let's take our initial outputs from Acute and expand them into our expanded multivariate space to use for homology grouping.


```python
day=10

filenames=landmark_pandas.loc[:,['filename']].values
cur_plms=landmark_pandas[filenames==name_prefix+str(day)]
cur_plms=cur_plms.append(landmark_pandas[filenames==name_prefix+str(day+1)])

cur_plms = space(cur_plms, debug=True, include_bound_dist=True, include_centroid_dist=True, include_orient_angles=True)
```

      group             plmname       filename  plm_x  plm_y  SS_x  SS_y  TS_x  \
    0  None  B100_rep1_d10_plm1  B100_rep1_d10    901   1151   894  1171   885   
    1  None  B100_rep1_d10_plm2  B100_rep1_d10    786   1423   789  1402   772   
    2  None  B100_rep1_d10_plm3  B100_rep1_d10    571   1344   592  1336   593   
    3  None  B100_rep1_d10_plm4  B100_rep1_d10    793   1523   796  1512   783   
    4  None  B100_rep1_d10_plm5  B100_rep1_d10    712   1511   735  1508   734   
    
       TS_y    CC_ratio  bot_left_dist  bot_right_dist  top_left_dist  \
    0  1167  179.786408     521.647390      404.545424     331.185748   
    1  1404   51.358025     252.287534      189.525724     369.086711   
    2  1342  136.758621     211.000000      409.538765     221.000000   
    3  1519   77.395349     224.294449      132.909744     457.475682   
    4  1512  165.041667     147.705789      214.560015     412.825629   
    
       top_right_dist  centroid_dist  orientation  centroid_orientation  
    0       35.000000     283.704071  -147.425943            155.422333  
    1      329.387310      14.317821   -15.376251             12.094757  
    2      414.779459     221.740840   103.091893            -72.954263  
    3      420.286807     114.437756   -25.016893              5.013114  
    4      441.184769     124.277914    92.544804           -145.159056  


Now as we look at our outputs from the space function we can see that there is clearly quite a bit of extra information we've just added. Let's breakdown what each of these new elements are item by item just to understand what new information we've generated.  

To begin we can consider five distance elements, 'bot_left_dist', 'bot_right_dist', 'top_left_dist', 'top_right_dist', and 'centroid_dist'.  These new values are distances between the plms representing each row and the bounding box corners capturing our current image pairs plms. In addition, we also calculate a centroid point for our current image pair to generate a distance from the 'center of gravity' for these paired plms.  Given we've largely focused on spatial positions alone distance measures, while analogous in terms of being pixel measures, help by giving us some added indication as to where in space our landmarks fall compared to one another.  

Beyond these distance measures we have two other elements, 'orientation' and 'centroid_orientation'.  As could be anticipated from these names these elements are both providing some additional information about the direction of the plms in space as opposed to raw distance measures, however, they are accomplishing this in very different ways.  The 'orientation' measures are based purely on the plm, SS, TS coordinates in which the midpoint between SS and TS are calculated and this midpoint is then used to drive a line towards the plm to generate a slope. Following the generation of a slope an angle can be generated using the formula:
   
    angle = arctan(slope)*(180/pi)

By contrast, the 'centroid_orientation' begins at the centroid and drives a line towards the plm to generate a slope then uses a similar formula to what was described above in order to calculate an angle of orientation.  

Now that we have a multivariate dataset that is rich in context for comparisons to be made we can begin to determine how similar or distant they are to one another through time. For the initial steps we will use two approaches, PCA which is extremely useful in maximizing the amount of variation while reducing dimensionality (key in a dataset such as ours) followed by clustering approaches used to link nearest neighbors (which will help us stitch our plms together through time).

Let's begin with our PCA approach which will be found within our StarScape function...


```python
groupA = name_prefix+str(day)
groupB = name_prefix+str(day+1)
finalDf, eigvals, loadings = starscape(cur_plms, groupA, groupB, outfile_prefix, True)
plt.show()

finalDf.head()
```

    Eigenvalues:  [7.64245625 4.69779072 1.43669426 0.55238408] 
    
    
    Var. Explained:  [0.51556252 0.31691445 0.09691985 0.03726401] 
    
    
    Cumul. Var. Explained:  [0.51556252 0.83247698 0.92939683 0.96666083] 
    
    
    3  components sufficiently informative





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>plmname</th>
      <th>filename</th>
      <th>PC1</th>
      <th>PC2</th>
      <th>PC3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>B100_rep1_d10_plm1</td>
      <td>B100_rep1_d10</td>
      <td>678.087482</td>
      <td>-66.393699</td>
      <td>-41.954341</td>
    </tr>
    <tr>
      <th>1</th>
      <td>B100_rep1_d10_plm2</td>
      <td>B100_rep1_d10</td>
      <td>-42.672012</td>
      <td>-29.263175</td>
      <td>87.104739</td>
    </tr>
    <tr>
      <th>2</th>
      <td>B100_rep1_d10_plm3</td>
      <td>B100_rep1_d10</td>
      <td>-5.424657</td>
      <td>464.544858</td>
      <td>-45.729843</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B100_rep1_d10_plm4</td>
      <td>B100_rep1_d10</td>
      <td>-219.879998</td>
      <td>-120.743091</td>
      <td>-36.344972</td>
    </tr>
    <tr>
      <th>4</th>
      <td>B100_rep1_d10_plm5</td>
      <td>B100_rep1_d10</td>
      <td>-288.475024</td>
      <td>91.257940</td>
      <td>-66.560096</td>
    </tr>
  </tbody>
</table>
</div>



Using the StarScape function above a principal component analysis is undertaken to reduce the dimensionality of our multivariate space to a minimal number of maximally informative dimensions (3 in this example) while also providing some helpful outputs for consideration as we perform our later homology grouping with Constella.  When running StarScape in debugging mode as we have it should be noted that various attributes of the PCA which was performed such as the eigenvalues and eigenvectors will be printed as outputs.

The first of the graphical outputs that StarScape produces is a scree plot.  The eigenvalues plotted in this graph are used to dynamically define the number of components required for explaining the relationship of our plms groupings within multivariate space.  As we can observe in this scree plot, as can be expected with most PCA analyses, that the vast majority of our variance can be explained with the first few dimensions which are then stored as an output dataframe. The number of output components can be defined by the user although it is recommended to have a strong reasoning from deviating from the default setting built within this script. 

Following the identification of our number of informative components we can then observe our 'starscape' as two overlaid scatter plots reflecting the first three PC dimensions.  In this graph we can also observe that our two perspectives in time between this image neighbor pair are color coded allowing us to see that in fact several of these plms appear to be almost perfectly overlapping through time suggesting they likely represent the same structure. This neighbor pair was purposefully chosen for this demonstration as we can see day 11 has 2 points which appear to lack partners.  This is due to the fact that a new leaf was exerted in this frame resulting in two new plms representing a leaf tip and ligule.  

This PC space will provide a perfect test case for our demonstrating the methodology of our homology grouping script Constella...  



```python
cur_plms, group_iter = constella(cur_plms, finalDf, group_iter, outfile_prefix, True)
plt.show()
```

    18 plms to group


Although we initially only see the hierarchical cluster used by Constella shown as a dendrogram graphic quite a bit has actually happened when we ran this function in order to generate our homology groupings!

Let's start by thinking about what our hierarchical cluster of our neighboring frames looks like in this graphic.  We can see that for the vast majority of our plms there appear to be paired points which correspond to a plm from each frame (given the 3D plot from our starscape plot this probably isn't much of a surprise!).  Given this initial finding it would almost seem at first glance that focusing on groups consisting of two plms would be sufficient, however, there is some nuance to plm datasets given they are dynamically describing growth as it occurs.  For example, we can see at least one case in which clusters of three plms form within this dendrogram, and another more complex situation in which day 11 plm 2 becomes a rogue point in the proximity of a pair of homology groups.  In each of these cases one of the emergent plms that just appeared in the day 11 frame is clustering around its nearest cluster pair in the starscape output.  Even when they are no longer emergent it is often common for these new points to rapidly migrate for several days before reaching stationarity as the structure they represent grows and eventually arrests its development.  As such we need a fairly robust means of describing structures which are more or less non-moving while also being able to dynamically characterize noisier subcomponents of the dataset which may be undertaking fairly rapid change for a transient period of time.  Ultimately Constella is designed around the concept for describing groups as duets which are adjacent to one another in time.  Let's use a series of examples to grasp this concept:

## Constella homology grouping example (i.e. identifying duets, quartets, and rogues)

1)
                                        
                     --- Day 11 Group 1   |   As we look at this initial illustration of a dendrogram it is clear
    ----------------|                     |   that there is a clear group which we refer to as a 'duet' which will
                     --- Day 12 Group 1   |   share a group ID serial number during Constella de novo assignment.

2)

                     --- Day 11 Group 1   |  As development continues things often become more complicated with
                ----|                     |  novel structures begin to appear and lacking partners due to their 
               |     --- Day 12 Group 1   |  recent appearance they often cluster around a known duet. These 
    -----------|                          |  points which appear to lack any notable partner to pair with are
                -------- Day 12 Group 2   |  referred to as rogues and are often given their own group ID number.
                
3) 

                     --- Day 12 Group 1   |  Development continues and further evidence begins to accumuluate for 
                ----|                     |  group 2 with a partner now appearing in day 13.  However, when growth
               |     --- Day 13 Group 1   |  is rapidly occuring duets sometimes have difficulty manifesting due 
             --|                          |  to rapid changes between day 12 and 13 for group 2. This leads to a
            |  |                          |  grade luck structure as shown here we refer to as a quartet which is
    --------|   -------- Day 12 Group 2   |  merely an artifact of a similar problem known as 'long branch attract
            |                             |  -ion' in phylyogenetics. So long as a grade of 2 plms exactly can be
             ----------- Day 13 Group 2   |  resolved a quartet can be used to assign the identity of group 2.

4)

                     --- Day 13 Group 1   |  As development continues and the rapid growth that gave rise to the   
         -----------|                     |  quartet structure abates we can begin to clearly resolve duets for
        |            --- Day 14 Group 1   |  groups 1 and 2.  These structured duets often make up the bulk of 
    ----|                                 |  our dendrogram results as shown above which, like figure (1) can 
        |        ------- Day 13 Group 2   |  readily be used to assign group identities to duets.
         -------|
                 ------- Day 14 Group 2
                     
In the manner described above, Constella operates through iteratively assigning points identities through an expanding nearest neighbor homology grouping scheme which is superfically similar to neighbor joining.  Although these steps are critical to defining how Constella weighs homology, as important is how Constella chooses to define new serial number identities vs. perserving existing ones:  

## Constella groups: seeding vs. linking

Now that we have covered the basics of how Constella detects groups it is worth taking a moment to discuss how Constella assigns names.  There are generally two strategies which largely are based on if prior encounters with plms that are being grouped through image series/time series data has occurred.  When we first began this notebook we assigned the variable 'group_iter' to 1 which serves as our counter variable for assigning serial numbers to each homology group as Constella detects them.  When a novel group is detected, be it a duet, graded pair in a quartet, or rogue plms Constella 'seeds' these groups by assigning them the current group_iter number and iterating the counter by one.  By contrast, some groups should be expected to appear for several images in a row, especially in time series data, and in these cases an identity is already established for one of the current pair.  In these cases 'linking' occurs in which the known identity for one of the pair is passed on to the yet to be defined member so that the identity of this group is allowed to be carried through time or across an image series of analogous data. 

Given this naming strategy of assigning numbers as identities it is probably worth noting that although Constella is designed for use in homology-based approaches it operates in an analogous sphere to de novo genome assemblers in that although both can identify probable relationships (either as genomic scaffolds or plm linkage groups) it makes no attempt to assign known identity to these groups akin to changing scaffold identities to that of known chromosomes for a given genome.  This step of defining plm groups as a specific leaf tip, a leaf axil/ligule, or a floral structure such as an inflorescence apex is a post analysis step to be undertaken by an end user.

#### Where we left off...

Now that we have a thorough understanding of exactly what we did by running running Constella it would probably be good to see how well it did wouldn't it? Let's have a look!


```python
cur_plms
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
      <th>plmname</th>
      <th>filename</th>
      <th>plm_x</th>
      <th>plm_y</th>
      <th>SS_x</th>
      <th>SS_y</th>
      <th>TS_x</th>
      <th>TS_y</th>
      <th>CC_ratio</th>
      <th>bot_left_dist</th>
      <th>bot_right_dist</th>
      <th>top_left_dist</th>
      <th>top_right_dist</th>
      <th>centroid_dist</th>
      <th>orientation</th>
      <th>centroid_orientation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>B100_rep1_d10_plm1</td>
      <td>B100_rep1_d10</td>
      <td>901</td>
      <td>1151</td>
      <td>894</td>
      <td>1171</td>
      <td>885</td>
      <td>1167</td>
      <td>179.786408</td>
      <td>521.647390</td>
      <td>404.545424</td>
      <td>331.185748</td>
      <td>35.000000</td>
      <td>283.704071</td>
      <td>-147.425943</td>
      <td>155.422333</td>
    </tr>
    <tr>
      <th>1</th>
      <td>8</td>
      <td>B100_rep1_d10_plm2</td>
      <td>B100_rep1_d10</td>
      <td>786</td>
      <td>1423</td>
      <td>789</td>
      <td>1402</td>
      <td>772</td>
      <td>1404</td>
      <td>51.358025</td>
      <td>252.287534</td>
      <td>189.525724</td>
      <td>369.086711</td>
      <td>329.387310</td>
      <td>14.317821</td>
      <td>-15.376251</td>
      <td>12.094757</td>
    </tr>
    <tr>
      <th>2</th>
      <td>6</td>
      <td>B100_rep1_d10_plm3</td>
      <td>B100_rep1_d10</td>
      <td>571</td>
      <td>1344</td>
      <td>592</td>
      <td>1336</td>
      <td>593</td>
      <td>1342</td>
      <td>136.758621</td>
      <td>211.000000</td>
      <td>409.538765</td>
      <td>221.000000</td>
      <td>414.779459</td>
      <td>221.740840</td>
      <td>103.091893</td>
      <td>-72.954263</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>B100_rep1_d10_plm4</td>
      <td>B100_rep1_d10</td>
      <td>793</td>
      <td>1523</td>
      <td>796</td>
      <td>1512</td>
      <td>783</td>
      <td>1519</td>
      <td>77.395349</td>
      <td>224.294449</td>
      <td>132.909744</td>
      <td>457.475682</td>
      <td>420.286807</td>
      <td>114.437756</td>
      <td>-25.016893</td>
      <td>5.013114</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>B100_rep1_d10_plm5</td>
      <td>B100_rep1_d10</td>
      <td>712</td>
      <td>1511</td>
      <td>735</td>
      <td>1508</td>
      <td>734</td>
      <td>1512</td>
      <td>165.041667</td>
      <td>147.705789</td>
      <td>214.560015</td>
      <td>412.825629</td>
      <td>441.184769</td>
      <td>124.277914</td>
      <td>92.544804</td>
      <td>-145.159056</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1</td>
      <td>B100_rep1_d10_plm6</td>
      <td>B100_rep1_d10</td>
      <td>803</td>
      <td>1555</td>
      <td>796</td>
      <td>1538</td>
      <td>807</td>
      <td>1535</td>
      <td>205.491525</td>
      <td>232.000000</td>
      <td>119.000000</td>
      <td>490.354973</td>
      <td>448.090393</td>
      <td>147.363496</td>
      <td>-4.635463</td>
      <td>7.800188</td>
    </tr>
    <tr>
      <th>6</th>
      <td>4</td>
      <td>B100_rep1_d10_plm7</td>
      <td>B100_rep1_d10</td>
      <td>922</td>
      <td>1415</td>
      <td>898</td>
      <td>1420</td>
      <td>900</td>
      <td>1416</td>
      <td>133.183673</td>
      <td>377.890196</td>
      <td>140.000000</td>
      <td>456.579675</td>
      <td>292.000000</td>
      <td>139.129436</td>
      <td>-97.431408</td>
      <td>87.528335</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2</td>
      <td>B100_rep1_d10_plm8</td>
      <td>B100_rep1_d10</td>
      <td>800</td>
      <td>1477</td>
      <td>816</td>
      <td>1459</td>
      <td>801</td>
      <td>1454</td>
      <td>48.893258</td>
      <td>241.919408</td>
      <td>144.803315</td>
      <td>421.612381</td>
      <td>374.432905</td>
      <td>70.092796</td>
      <td>157.479434</td>
      <td>14.036243</td>
    </tr>
    <tr>
      <th>8</th>
      <td>7</td>
      <td>B100_rep1_d11_plm1</td>
      <td>B100_rep1_d11</td>
      <td>912</td>
      <td>1123</td>
      <td>905</td>
      <td>1142</td>
      <td>896</td>
      <td>1139</td>
      <td>201.460784</td>
      <td>550.368059</td>
      <td>432.115725</td>
      <td>341.000000</td>
      <td>10.000000</td>
      <td>313.746713</td>
      <td>-146.689369</td>
      <td>155.722295</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
      <td>B100_rep1_d11_plm2</td>
      <td>B100_rep1_d11</td>
      <td>786</td>
      <td>1370</td>
      <td>792</td>
      <td>1350</td>
      <td>783</td>
      <td>1347</td>
      <td>91.428571</td>
      <td>283.637092</td>
      <td>229.610540</td>
      <td>327.466029</td>
      <td>281.966310</td>
      <td>39.115214</td>
      <td>176.009087</td>
      <td>175.601295</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10</td>
      <td>B100_rep1_d11_plm3</td>
      <td>B100_rep1_d11</td>
      <td>752</td>
      <td>1236</td>
      <td>761</td>
      <td>1252</td>
      <td>754</td>
      <td>1260</td>
      <td>181.622222</td>
      <td>366.772409</td>
      <td>361.470607</td>
      <td>213.377600</td>
      <td>204.129861</td>
      <td>175.755512</td>
      <td>15.376251</td>
      <td>-10.159056</td>
    </tr>
    <tr>
      <th>11</th>
      <td>8</td>
      <td>B100_rep1_d11_plm4</td>
      <td>B100_rep1_d11</td>
      <td>780</td>
      <td>1420</td>
      <td>780</td>
      <td>1398</td>
      <td>767</td>
      <td>1404</td>
      <td>57.927007</td>
      <td>248.809164</td>
      <td>195.931110</td>
      <td>363.166628</td>
      <td>329.200547</td>
      <td>11.401754</td>
      <td>-18.886087</td>
      <td>-164.744881</td>
    </tr>
    <tr>
      <th>12</th>
      <td>6</td>
      <td>B100_rep1_d11_plm5</td>
      <td>B100_rep1_d11</td>
      <td>576</td>
      <td>1353</td>
      <td>595</td>
      <td>1343</td>
      <td>595</td>
      <td>1350</td>
      <td>153.015152</td>
      <td>202.061872</td>
      <td>400.649473</td>
      <td>230.054341</td>
      <td>415.470817</td>
      <td>214.441134</td>
      <td>108.886087</td>
      <td>-74.862050</td>
    </tr>
    <tr>
      <th>13</th>
      <td>3</td>
      <td>B100_rep1_d11_plm6</td>
      <td>B100_rep1_d11</td>
      <td>789</td>
      <td>1523</td>
      <td>791</td>
      <td>1511</td>
      <td>780</td>
      <td>1517</td>
      <td>61.134328</td>
      <td>220.336107</td>
      <td>136.795468</td>
      <td>455.548022</td>
      <td>421.531731</td>
      <td>114.157786</td>
      <td>-21.250506</td>
      <td>3.012788</td>
    </tr>
    <tr>
      <th>14</th>
      <td>5</td>
      <td>B100_rep1_d11_plm7</td>
      <td>B100_rep1_d11</td>
      <td>706</td>
      <td>1510</td>
      <td>728</td>
      <td>1506</td>
      <td>728</td>
      <td>1510</td>
      <td>136.659091</td>
      <td>142.302495</td>
      <td>220.637712</td>
      <td>409.870711</td>
      <td>443.198601</td>
      <td>127.003937</td>
      <td>95.194429</td>
      <td>-142.678964</td>
    </tr>
    <tr>
      <th>15</th>
      <td>1</td>
      <td>B100_rep1_d11_plm8</td>
      <td>B100_rep1_d11</td>
      <td>802</td>
      <td>1553</td>
      <td>791</td>
      <td>1532</td>
      <td>801</td>
      <td>1533</td>
      <td>206.361702</td>
      <td>231.008658</td>
      <td>120.016666</td>
      <td>488.119862</td>
      <td>446.430286</td>
      <td>145.248064</td>
      <td>-16.313852</td>
      <td>7.516442</td>
    </tr>
    <tr>
      <th>16</th>
      <td>4</td>
      <td>B100_rep1_d11_plm9</td>
      <td>B100_rep1_d11</td>
      <td>914</td>
      <td>1417</td>
      <td>893</td>
      <td>1423</td>
      <td>891</td>
      <td>1417</td>
      <td>145.431373</td>
      <td>369.720164</td>
      <td>138.231690</td>
      <td>451.757678</td>
      <td>294.108823</td>
      <td>131.244047</td>
      <td>-97.765166</td>
      <td>86.505361</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2</td>
      <td>B100_rep1_d11_plm10</td>
      <td>B100_rep1_d11</td>
      <td>798</td>
      <td>1475</td>
      <td>807</td>
      <td>1466</td>
      <td>795</td>
      <td>1459</td>
      <td>57.528090</td>
      <td>240.684441</td>
      <td>147.566934</td>
      <td>418.847228</td>
      <td>373.202358</td>
      <td>67.683085</td>
      <td>166.504267</td>
      <td>12.804266</td>
    </tr>
  </tbody>
</table>
</div>



It definitely appears as if we have paired groups between the majority of our plms across days 10 and 11! The only exceptions appear to be two plms specific to day 11 which are assigned to groups 9 and 10.  It would probably be worth seeing how these stack up on our original data (i.e. the images) since these data tables are often aren't the easiest to process.  With that being said, let's superimpose these groups onto the plms coordinates on each frame to see if they are in agreement.


```python
img1 = cv2.imread(path+name_prefix+str(day)+'.jpg')

for p in range(0,cur_plms.shape[0]):
    if name_prefix+str(day) in cur_plms.at[p, 'plmname']:        
        cv2.putText(img1, str(cur_plms.at[p, 'group']), 
                    (int(cur_plms.at[p, 'plm_x'])-10, int(cur_plms.at[p, 'plm_y'])), 
                    cv2.FONT_ITALIC, 1.5, (255,0,0), 6)

img2 = cv2.imread(path+name_prefix+str(day+1)+'.jpg')

for p in range(0,cur_plms.shape[0]):
    if name_prefix+str(day+1) in cur_plms.at[p, 'plmname']:        
        cv2.putText(img2, str(cur_plms.at[p, 'group']), 
                    (int(cur_plms.at[p, 'plm_x'])-10, int(cur_plms.at[p, 'plm_y'])), 
                    cv2.FONT_ITALIC, 1.5, (0,0,255), 6)
  
img_neighbors = cv2.hconcat((img1, img2))

plm_groups_fig=plt.figure(figsize=(16, 12))
plm_groups_fig=plt.imshow(img_neighbors)
plm_groups_fig=plt.xscale('linear')
plm_groups_fig=plt.axis('off')
plm_groups_fig=plt.title('B100 day '+str(day)+'-'+str(day+1))
plt.show(plm_groups_fig)        
```


![png](output_17_0.png)


Looking at our groups overlaid against the leaf tips and ligules it seems like our attempts at forming homology groups through our workflow was a success! And note how our ligule and leaf tip plms corresponding to the emergent leaf in day 11 are represented by groups '9' and '10' which didn't appear in our first frame, seeding new groups as novel structures appear is clearly working as advertised as well! 

Now that we understand how homology grouping works through the use of our Space >>> StarScape >>> Constella workflow we will use our final exercise to expand on what we've learned and apply it to store time series data and utilize groundtruthed plms of QC steps during pipeline development.
