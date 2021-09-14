# Exercise 4: Batch homology grouping and downstream QC analyses

Following on the same strategy we employed in exercises 1 and 2 of first learning how to employ acute on a single image and then scaling up to batch image data we will now take what we have learned in exercise 3 for homology grouping with the StarScape and Constella workflow and scale this method up for use on batch image data.  Following the generation of serial ID number homology groups and assigning them to our acute plms we will then assay the accuracy of these results through the use of a Quality Control (QC) test for Constella and discuss how these outputs should be interpreted.

To begin lets load the libraries and other input files we'll need to proceed...


```python
import cv2
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plantcv as pcv

from plantcv.plantcv.homology.acute import acute
from plantcv.plantcv.homology.space import space
from plantcv.plantcv.homology.starscape import starscape
from plantcv.plantcv.homology.constella import constella
from plantcv.plantcv.homology.constellaqc import constellaqc

win=25
thresh=90
debug = True 

path='/Path/To/Images/plm_tutorial/'
days=range(10,14)
name_prefix='B100_rep1_d'
outpath='/Path/To/Output/Directory/'
outfile_prefix = outpath+'B100_test'

group_iter = 1
```

Now with our libraries loaded and initial parameters assigned let us begin by running a batch workflow with acute to generate our list of plms as a landmark dataframe.


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


Before we continue lets check our landmarks once more to ensure we'll have what we need to run our homology grouping workflow...


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



Provided the head of our table loaded in properly we're now ready to begin a batch run of our homology pipeline which follows the same structure as our previous exercise  utilizing StarScape and Constella. Note that we have left out Space from this workflow, studies of this pipelines accuracy have suggested that this function isn't essential for generating tangible improvements in homology grouping.  As such this workflow of parsing segmented morphological data directly into Starscape is considered the present best practice of this approach. Notice how our groups within landmark_pandas are universally assigned to 'None'? On the other side of this code block we should see the results of transfering group IDs from paired frames to this original dataframe resulting in forthcoming changes to this columns values.  Let's get started! 


```python
for di in range(0,len(days)-1):

    print('\nBeginning next iteration for days '+str(days[di])+' and '+str(days[di]+1)+'\n')
    filenames=landmark_pandas.loc[:,['filename']].values
    cur_plms=landmark_pandas[filenames==name_prefix+str(days[di])]
    cur_plms=cur_plms.append(landmark_pandas[filenames==name_prefix+str(days[di]+1)])
    cur_plms

    groupA = name_prefix+str(days[di])
    groupB = name_prefix+str(days[di]+1)

    print('\nRunning StarScape...\n')    
    finalDf, eigenvals, loadings = starscape(cur_plms, groupA, groupB, 'B100_rep1_d'+str(days[di])+'_test', True)
    plt.show()

    print('\nRunning Constella...\n')
    cur_plms, group_iter = constella(cur_plms, finalDf, group_iter, 'B100_rep1_d'+str(days[di])+'_test', True)
    plt.show()

    plmnames=landmark_pandas.loc[:,['plmname']].values
    cur_plmnames=cur_plms.loc[:,['plmname']].values

    for name in cur_plmnames:
        landmark_index=[i for i, x in enumerate(plmnames==name) if x]
        cur_plms_index=[i for i, x in enumerate(cur_plmnames==name) if x]
        if landmark_pandas.iloc[landmark_index,0].values == None:
            landmark_pandas.iloc[landmark_index,0] = cur_plms.iloc[cur_plms_index,0]

    if 1==1:
        img1 = cv2.imread(path+name_prefix+str(days[di])+'.jpg')

        for p in range(0,cur_plms.shape[0]):
            if name_prefix+str(days[di]) in cur_plms.iloc[p, 2]:        
                cv2.putText(img1, str(cur_plms.iloc[p, 0]), 
                            (int(cur_plms.iloc[p, 3])-10, int(cur_plms.iloc[p, 4])), 
                            cv2.FONT_ITALIC, 1.5, (255,0,0), 6)

        img2 = cv2.imread(path+name_prefix+str(days[di]+1)+'.jpg')

        for p in range(0,cur_plms.shape[0]):
            if name_prefix+str(days[di]+1) in cur_plms.iloc[p, 2]:        
                cv2.putText(img2, str(cur_plms.iloc[p, 0]), 
                            (int(cur_plms.iloc[p, 3])-10, int(cur_plms.iloc[p, 4])), 
                            cv2.FONT_ITALIC, 1.5, (0,0,255), 6)

        img_neighbors = cv2.hconcat((img1, img2))

        plm_groups_fig=plt.figure(figsize=(16, 12))
        plm_groups_fig=plt.imshow(img_neighbors)
        plm_groups_fig=plt.xscale('linear')
        plm_groups_fig=plt.axis('off')
        plm_groups_fig=plt.title('B100 day '+str(days[di])+'-'+str(days[di]+1))
        plt.show(plm_groups_fig)
            

```

    
    Beginning next iteration for days 10 and 11
    
    
    Running StarScape...
    
    Eigenvalues:  [3.80272283 2.68008038 0.92036756 0.00479015] 
    
    
    Var. Explained:  [0.51306578 0.36159815 0.12417658 0.00064629] 
    
    
    Cumul. Var. Explained:  [0.51306578 0.87466393 0.9988405  0.99948679] 
    
    
    2  components sufficiently informative
    
    Running Constella...
    
    18 plms to group



![png](output_7_1.png)


    
    Beginning next iteration for days 11 and 12
    
    
    Running StarScape...
    
    Eigenvalues:  [3.79893075 2.6753918  0.88539829 0.0045825 ] 
    
    
    Var. Explained:  [0.51556917 0.36308889 0.1201612  0.00062191] 
    
    
    Cumul. Var. Explained:  [0.51556917 0.87865806 0.99881926 0.99944117] 
    
    
    2  components sufficiently informative
    
    Running Constella...
    
    20 plms to group



![png](output_7_3.png)


    
    Beginning next iteration for days 12 and 13
    
    
    Running StarScape...
    
    Eigenvalues:  [3.55972863 2.8587077  0.9428435  0.00363656] 
    
    
    Var. Explained:  [0.48310603 0.38796747 0.12795733 0.00049353] 
    
    
    Cumul. Var. Explained:  [0.48310603 0.8710735  0.99903083 0.99952437] 
    
    
    2  components sufficiently informative
    
    Running Constella...
    
    20 plms to group



![png](output_7_5.png)


With the homology grouping workflow now completed a decent array of graphical outputs should be visible above displaying not only our PCA related graphs and the dendrogram used for our hierarchical clustering at each step, but also side by side images of our plants as well as their labeled homology groups to enable for easy point of reference for calling accuracy.  Let's have a look at our de novo homology groups on our original landmark_pandas dataframe, this time we'll have a look at the full table though instead of just taking a quick glance at the head.


```python
landmark_pandas
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
      <td>8</td>
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
      <td>5</td>
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
      <td>7</td>
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
      <td>1</td>
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
      <td>4</td>
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
    <tr>
      <th>5</th>
      <td>2</td>
      <td>B100_rep1_d10_plm6</td>
      <td>B100_rep1_d10</td>
      <td>803</td>
      <td>1555</td>
      <td>796</td>
      <td>1538</td>
      <td>807</td>
      <td>1535</td>
      <td>205.491525</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>B100_rep1_d10_plm7</td>
      <td>B100_rep1_d10</td>
      <td>922</td>
      <td>1415</td>
      <td>898</td>
      <td>1420</td>
      <td>900</td>
      <td>1416</td>
      <td>133.183673</td>
    </tr>
    <tr>
      <th>7</th>
      <td>3</td>
      <td>B100_rep1_d10_plm8</td>
      <td>B100_rep1_d10</td>
      <td>800</td>
      <td>1477</td>
      <td>816</td>
      <td>1459</td>
      <td>801</td>
      <td>1454</td>
      <td>48.893258</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>B100_rep1_d11_plm1</td>
      <td>B100_rep1_d11</td>
      <td>912</td>
      <td>1123</td>
      <td>905</td>
      <td>1142</td>
      <td>896</td>
      <td>1139</td>
      <td>201.460784</td>
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
    </tr>
    <tr>
      <th>11</th>
      <td>5</td>
      <td>B100_rep1_d11_plm4</td>
      <td>B100_rep1_d11</td>
      <td>780</td>
      <td>1420</td>
      <td>780</td>
      <td>1398</td>
      <td>767</td>
      <td>1404</td>
      <td>57.927007</td>
    </tr>
    <tr>
      <th>12</th>
      <td>7</td>
      <td>B100_rep1_d11_plm5</td>
      <td>B100_rep1_d11</td>
      <td>576</td>
      <td>1353</td>
      <td>595</td>
      <td>1343</td>
      <td>595</td>
      <td>1350</td>
      <td>153.015152</td>
    </tr>
    <tr>
      <th>13</th>
      <td>1</td>
      <td>B100_rep1_d11_plm6</td>
      <td>B100_rep1_d11</td>
      <td>789</td>
      <td>1523</td>
      <td>791</td>
      <td>1511</td>
      <td>780</td>
      <td>1517</td>
      <td>61.134328</td>
    </tr>
    <tr>
      <th>14</th>
      <td>4</td>
      <td>B100_rep1_d11_plm7</td>
      <td>B100_rep1_d11</td>
      <td>706</td>
      <td>1510</td>
      <td>728</td>
      <td>1506</td>
      <td>728</td>
      <td>1510</td>
      <td>136.659091</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2</td>
      <td>B100_rep1_d11_plm8</td>
      <td>B100_rep1_d11</td>
      <td>802</td>
      <td>1553</td>
      <td>791</td>
      <td>1532</td>
      <td>801</td>
      <td>1533</td>
      <td>206.361702</td>
    </tr>
    <tr>
      <th>16</th>
      <td>6</td>
      <td>B100_rep1_d11_plm9</td>
      <td>B100_rep1_d11</td>
      <td>914</td>
      <td>1417</td>
      <td>893</td>
      <td>1423</td>
      <td>891</td>
      <td>1417</td>
      <td>145.431373</td>
    </tr>
    <tr>
      <th>17</th>
      <td>3</td>
      <td>B100_rep1_d11_plm10</td>
      <td>B100_rep1_d11</td>
      <td>798</td>
      <td>1475</td>
      <td>807</td>
      <td>1466</td>
      <td>795</td>
      <td>1459</td>
      <td>57.528090</td>
    </tr>
    <tr>
      <th>18</th>
      <td>8</td>
      <td>B100_rep1_d12_plm1</td>
      <td>B100_rep1_d12</td>
      <td>932</td>
      <td>1108</td>
      <td>925</td>
      <td>1131</td>
      <td>919</td>
      <td>1121</td>
      <td>200.401869</td>
    </tr>
    <tr>
      <th>19</th>
      <td>9</td>
      <td>B100_rep1_d12_plm2</td>
      <td>B100_rep1_d12</td>
      <td>784</td>
      <td>1362</td>
      <td>793</td>
      <td>1343</td>
      <td>780</td>
      <td>1343</td>
      <td>51.891892</td>
    </tr>
    <tr>
      <th>20</th>
      <td>10</td>
      <td>B100_rep1_d12_plm3</td>
      <td>B100_rep1_d12</td>
      <td>720</td>
      <td>1151</td>
      <td>730</td>
      <td>1170</td>
      <td>724</td>
      <td>1175</td>
      <td>176.054054</td>
    </tr>
    <tr>
      <th>21</th>
      <td>5</td>
      <td>B100_rep1_d12_plm4</td>
      <td>B100_rep1_d12</td>
      <td>779</td>
      <td>1425</td>
      <td>779</td>
      <td>1402</td>
      <td>763</td>
      <td>1407</td>
      <td>43.620112</td>
    </tr>
    <tr>
      <th>22</th>
      <td>7</td>
      <td>B100_rep1_d12_plm5</td>
      <td>B100_rep1_d12</td>
      <td>568</td>
      <td>1367</td>
      <td>585</td>
      <td>1358</td>
      <td>591</td>
      <td>1361</td>
      <td>140.915254</td>
    </tr>
    <tr>
      <th>23</th>
      <td>1</td>
      <td>B100_rep1_d12_plm6</td>
      <td>B100_rep1_d12</td>
      <td>790</td>
      <td>1523</td>
      <td>789</td>
      <td>1511</td>
      <td>778</td>
      <td>1518</td>
      <td>67.282051</td>
    </tr>
    <tr>
      <th>24</th>
      <td>4</td>
      <td>B100_rep1_d12_plm7</td>
      <td>B100_rep1_d12</td>
      <td>713</td>
      <td>1509</td>
      <td>736</td>
      <td>1506</td>
      <td>719</td>
      <td>1511</td>
      <td>162.192308</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2</td>
      <td>B100_rep1_d12_plm8</td>
      <td>B100_rep1_d12</td>
      <td>801</td>
      <td>1555</td>
      <td>790</td>
      <td>1534</td>
      <td>801</td>
      <td>1535</td>
      <td>221.172897</td>
    </tr>
    <tr>
      <th>26</th>
      <td>6</td>
      <td>B100_rep1_d12_plm9</td>
      <td>B100_rep1_d12</td>
      <td>919</td>
      <td>1422</td>
      <td>897</td>
      <td>1426</td>
      <td>895</td>
      <td>1422</td>
      <td>130.591837</td>
    </tr>
    <tr>
      <th>27</th>
      <td>3</td>
      <td>B100_rep1_d12_plm10</td>
      <td>B100_rep1_d12</td>
      <td>797</td>
      <td>1475</td>
      <td>807</td>
      <td>1467</td>
      <td>793</td>
      <td>1461</td>
      <td>53.073171</td>
    </tr>
    <tr>
      <th>28</th>
      <td>10</td>
      <td>B100_rep1_d13_plm1</td>
      <td>B100_rep1_d13</td>
      <td>659</td>
      <td>1079</td>
      <td>673</td>
      <td>1097</td>
      <td>670</td>
      <td>1101</td>
      <td>140.700000</td>
    </tr>
    <tr>
      <th>29</th>
      <td>5</td>
      <td>B100_rep1_d13_plm2</td>
      <td>B100_rep1_d13</td>
      <td>771</td>
      <td>1425</td>
      <td>770</td>
      <td>1405</td>
      <td>753</td>
      <td>1408</td>
      <td>60.049383</td>
    </tr>
    <tr>
      <th>30</th>
      <td>7</td>
      <td>B100_rep1_d13_plm3</td>
      <td>B100_rep1_d13</td>
      <td>560</td>
      <td>1373</td>
      <td>581</td>
      <td>1362</td>
      <td>581</td>
      <td>1368</td>
      <td>164.285714</td>
    </tr>
    <tr>
      <th>31</th>
      <td>1</td>
      <td>B100_rep1_d13_plm4</td>
      <td>B100_rep1_d13</td>
      <td>784</td>
      <td>1526</td>
      <td>784</td>
      <td>1506</td>
      <td>771</td>
      <td>1518</td>
      <td>54.060345</td>
    </tr>
    <tr>
      <th>32</th>
      <td>4</td>
      <td>B100_rep1_d13_plm5</td>
      <td>B100_rep1_d13</td>
      <td>714</td>
      <td>1512</td>
      <td>736</td>
      <td>1507</td>
      <td>736</td>
      <td>1513</td>
      <td>137.769231</td>
    </tr>
    <tr>
      <th>33</th>
      <td>2</td>
      <td>B100_rep1_d13_plm6</td>
      <td>B100_rep1_d13</td>
      <td>798</td>
      <td>1557</td>
      <td>784</td>
      <td>1543</td>
      <td>796</td>
      <td>1539</td>
      <td>210.764045</td>
    </tr>
    <tr>
      <th>34</th>
      <td>6</td>
      <td>B100_rep1_d13_plm7</td>
      <td>B100_rep1_d13</td>
      <td>916</td>
      <td>1423</td>
      <td>900</td>
      <td>1423</td>
      <td>892</td>
      <td>1421</td>
      <td>128.000000</td>
    </tr>
    <tr>
      <th>35</th>
      <td>3</td>
      <td>B100_rep1_d13_plm8</td>
      <td>B100_rep1_d13</td>
      <td>789</td>
      <td>1480</td>
      <td>799</td>
      <td>1473</td>
      <td>787</td>
      <td>1464</td>
      <td>54.436782</td>
    </tr>
    <tr>
      <th>36</th>
      <td>8</td>
      <td>B100_rep1_d13_plm9</td>
      <td>B100_rep1_d13</td>
      <td>971</td>
      <td>1115</td>
      <td>958</td>
      <td>1132</td>
      <td>950</td>
      <td>1125</td>
      <td>193.185841</td>
    </tr>
    <tr>
      <th>37</th>
      <td>9</td>
      <td>B100_rep1_d13_plm10</td>
      <td>B100_rep1_d13</td>
      <td>776</td>
      <td>1355</td>
      <td>784</td>
      <td>1337</td>
      <td>771</td>
      <td>1332</td>
      <td>64.000000</td>
    </tr>
  </tbody>
</table>
</div>



We see group serial numbers 1-10 repeating once for each frame so it appears things ran pretty well! Moreover, when we glance at the side-by-side images with the serial numbers superimposed onto the original images things look like they're grouping as we'd expect.  

However, as with all de novo methods there is the possibility for errors to be introduced which we might miss at a glance.  This brings us to a key aspect of our plm workflow when scaling up to a full sized project which is Quality Control (QC) assessment of our de novo homologies.  This is often done with a reduced subset of our full dataset in order to give us a general idea of the overall accuracy of our calls.  Although there is currently one method of producing input StarScape files to feeding to Constella eventually as other ways to rescale our acute outputs are developed this method can provide a helpful means of comparing what method of metadata generation (plmSpace) and multivariate space transformation (StarScape) is the best for maximizing biologically informative signal.  With this being said let's begin by loading in a table of our landmarks which have been annotated to represent the biological structures they represent*.

*Although not seen in this situation it is common practice to denote random plms which don't represent any meaningful features as '-'.


```python
landmark_feat_standards = pd.read_csv('/Users/johnhodge/Documents/GitHub/Doust-lab-workflows/B100_timeseries_test_plms_annotated.csv')
landmark_feat_standards.head(10)
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
      <td>leaf5</td>
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
      <td>ligule4</td>
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
      <td>leaf4</td>
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
      <td>ligule2</td>
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
      <td>leaf2</td>
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
    <tr>
      <th>5</th>
      <td>base</td>
      <td>B100_rep1_d10_plm6</td>
      <td>B100_rep1_d10</td>
      <td>803</td>
      <td>1555</td>
      <td>796</td>
      <td>1538</td>
      <td>807</td>
      <td>1535</td>
      <td>205.491525</td>
    </tr>
    <tr>
      <th>6</th>
      <td>leaf3</td>
      <td>B100_rep1_d10_plm7</td>
      <td>B100_rep1_d10</td>
      <td>922</td>
      <td>1415</td>
      <td>898</td>
      <td>1420</td>
      <td>900</td>
      <td>1416</td>
      <td>133.183673</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ligule3</td>
      <td>B100_rep1_d10_plm8</td>
      <td>B100_rep1_d10</td>
      <td>800</td>
      <td>1477</td>
      <td>816</td>
      <td>1459</td>
      <td>801</td>
      <td>1454</td>
      <td>48.893258</td>
    </tr>
    <tr>
      <th>8</th>
      <td>leaf5</td>
      <td>B100_rep1_d11_plm1</td>
      <td>B100_rep1_d11</td>
      <td>912</td>
      <td>1123</td>
      <td>905</td>
      <td>1142</td>
      <td>896</td>
      <td>1139</td>
      <td>201.460784</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ligule5</td>
      <td>B100_rep1_d11_plm2</td>
      <td>B100_rep1_d11</td>
      <td>786</td>
      <td>1370</td>
      <td>792</td>
      <td>1350</td>
      <td>783</td>
      <td>1347</td>
      <td>91.428571</td>
    </tr>
  </tbody>
</table>
</div>



After glancing at the table above we essentially have 3 types of features we're classifying, our leaf tips denoted as 'leaf', our axils where leaf blades attach to the stem as 'ligule' (common term for this feature in grasses), and 'base' which represents the bottom landmark at the base of our plant.  Now we have a list of known features which we can compare to our corresponding list of our predicted homology groups.


```python
constellaqc(landmark_pandas, landmark_feat_standards, debug)
```

    Known Feature-Predicted Group Scoring Matrix:
    
             1   2   3   4   5   6   7   8   9   10
    base      0   4   0   0   0   0   0   0   0   0
    leaf2     0   0   0   4   0   0   0   0   0   0
    leaf3     0   0   0   0   0   4   0   0   0   0
    leaf4     0   0   0   0   0   0   4   0   0   0
    leaf5     0   0   0   0   0   0   0   4   0   0
    leaf6     0   0   0   0   0   0   0   0   0   3
    ligule2   4   0   0   0   0   0   0   0   0   0
    ligule3   0   0   4   0   0   0   0   0   0   0
    ligule4   0   0   0   0   4   0   0   0   0   0
    ligule5   0   0   0   0   0   0   0   0   3   0
    
    
    Valid Call Rate:      100.0 %
    Splitting Call Rate:  0.0 %
    Clumping Call Rate:   0.0 %


And there we have it! As expected the valid calls were perfect within this tutorial although error, and importantly the type of error is important to keep track of when developing this workflow for your own research.  To provide a bit of context let's discuss what our two sources of error represent.

## Splitting Error

Splitting errors are essentially calls in which more than one de novo homology group was generated to represent a single, known, feature.  Within this workflow these errors are often considered less egregious given that they can easily be reconciled together during manual curation of homology groups prior to using plm homology groups for morphometric analyses.  A good analogy to this problem is that of scaffold generation during whole genome sequencing in which often only fragments of rather than complete chromosomes are reconstructed from the data.  This issue is easily reconciled by a user specifying that these two scaffolds belong together and manually assigning linkage based on known attributes of this data which exist beyond the capacity of the de novo assembler.  In a similar vein of logic, if a leaf tip is broken into two groups it can easily be tied together as these groups are given a biologically relevant name.

## Clumping Error

Clumping errors by contrast are calls in which multiple known features are linked together under a single de novo homology group.  Understandably this error is considered far more troubling and all efforts in designing this workflow have been to drive this error rate as low as possible (in most cases hovering in the 5% range for true experimental data).  Often datasets which have a high degree of parallax (possessing perspective related artifacts of compressing 3-dimensional structures into a 2-dimensional frame) tend to drive up this error rate.  It is often best to check this error rate under a reduced dataset of each genotype or environmental treatment that is anticipated to be used given that it can provide a user with an overall grasp of how well Constella's de novo assignments work within this pool of the data.  Cases in which clumping error rates are higher may require a more stringent round of manual curration in order to ensure that morphometric analyses performed on this data afterwards are meaningful.



# In Conclusion

And there you have it! We've successfully started with a handful of time series images and learned how to prepare binary masks which can be used for acute in Tutorial 1.  We then learned in Tutorial 2 how to scale up what we had learned in our first exercise to work on batch image datasets. Following the generation of this batch plm data we were then able to explore de novo homology grouping through the use of our StarScape & Constella pipeline in Tutorial 3. And finally in our last exercise we again scaled up what we learned for homology grouping on to batch datasets then were able to test what we generated using ConstellaQC in order to get a general idea of how much confidence we can have in our calls.  

I hope this tutorial series have been informative and provides you with some quick-start code to get your own projects running. Cheers!

    -JGH


```python

```
