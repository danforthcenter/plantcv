# Exercise 2: Applying acute on batch datasets

In the previous exercise we learned how to use some basic tools latent to PlantCV to explore color spaces and extract plant shapes from an image then use this shape data for generating pseudo-landmarks (plms) with acute while thinking a bit about how acute is making its calls for de novo landmarks.  While this is useful and necessary we also need to think about how best to scale up our code in order to be used on batch datasets which can consist of multiple images either of the same genotype or of comparable stages of different genotypes.  For the sake of this demonstration we'll design a loop to run acute on a time series from the dataset we began to explore in the previous exercise.  With that all being said lets get started by taking a look at the files we have on hand...


```python
import cv2
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from plantcv.plantcv.plm_homologies.acute import acute

win=25
thresh=90
debug = True 

path='/Users/johnhodge/Documents/GitHub/Doust-lab-workflows/plm_tutorial/'

os.listdir(path)
```




    ['.DS_Store',
     'B100_rep1_d12.jpg',
     'B100_rep1_d13.jpg',
     'B100_rep1_d11.jpg',
     'B100_rep1_d10.jpg']



So already we can see that there seems to be a general theme with how these images are named following a 'Genotype' + 'Timepoint' + '.jpg' format.  Although this is just one form of serial naming strategy it is always advised with projects that will consist of large scale datasets to perform some initial step of data carpentry and decide a consistent manner of naming early on.  The reason this is important we'll see below when we design a for loop. Before we run the loop itself let's go ahead and specify the variables we'll need for this serial naming scheme and discuss what each one represents...


```python
days=range(10,14)
name_prefix='B100_rep1_d'
```

So we have 3 different variables we'll need we've created above days which is a list of integers that ranges from 10-13 in a pythonic fashion, a name prefix we can attach to each days integer to complete our serial names, and we'll also need a path to our files in the directory space which we have already specified earlier. Before we go ahead and scale up our code from the previous exercise let's first build a dummy loop which can perform a simple task on these files to be sure that we can read them in properly...


```python
for day in days:
    img = cv2.imread(path+name_prefix+str(day)+'.jpg')
    fig1=plt.figure(figsize=(6, 8))
    fig1=plt.imshow(img)
    fig1=plt.xscale('linear')
    fig1=plt.axis('off')
    fig1=plt.title(name_prefix+str(day))
    plt.show(fig1)
```


![png](output_5_0.png)



![png](output_5_1.png)



![png](output_5_2.png)



![png](output_5_3.png)


Notice in the script above that we have largely reused some code from our previous exercise, however, just to call attention to a concept we didn't discuss before notice how we can stitch together strings in python by concatenating them with the '+'. One caveat is that numeric/integer variables such as day need to be converted into a string so that python isn't confused by the operation of the '+' symbol that is desired, hence why we wrapped it in the str() function!  We're almost ready to iteratively run the acute workflow but before we do that we'll need to create an empty list (but we'll at least fill it with a header at least to start).


```python
landmark_output=[['name', 'plm_x', 'plm_y', 'SS_x', 'SS_y', 'TS_x', 'TS_y', 'CC_ratio']]
```

As we iteratively run acute on each frame we'll end up storing the landmarks generated from that day within landmark output. Note that if we didn't have this on hand (or another comparable list) before we started our variables wouldn't have anywhere to go for us to successfully save them! Now let's repeat what we learned from the previous exercise at scale...


```python
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
                landmark_output.append([name_prefix+str(day), homolog_pts[h][0][0], homolog_pts[h][0][1], homolog_start[h][0][0], homolog_start[h][0][1], homolog_stop[h][0][0], homolog_stop[h][0][1], homolog_cc[h],])

    #8. Plotting pseudo-landmarks on current image
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

    Contour volume: 2134.4002673625946
    Fusing contour edges
        landmark number: 8


    /Users/johnhodge/Documents/GitHub/plantcv/plantcv/plantcv/plm_homologies/acute.py:175: FutureWarning: Using a non-tuple sequence for multidimensional indexing is deprecated; use `arr[tuple(seq)]` instead of `arr[seq]`. In the future this will be interpreted as an array index, `arr[np.array(seq)]`, which will result either in an error or a different result.
    /Users/johnhodge/Documents/GitHub/plantcv/plantcv/plantcv/plm_homologies/acute.py:176: FutureWarning: Using a non-tuple sequence for multidimensional indexing is deprecated; use `arr[tuple(seq)]` instead of `arr[seq]`. In the future this will be interpreted as an array index, `arr[np.array(seq)]`, which will result either in an error or a different result.



![png](output_9_2.png)


    Contour volume: 2406.708920955658
    Fusing contour edges
        landmark number: 10



![png](output_9_4.png)


    Contour volume: 2661.887634396553
    Fusing contour edges
        landmark number: 10



![png](output_9_6.png)


    Contour volume: 2923.1912364959717
    Fusing contour edges
        landmark number: 10



![png](output_9_8.png)


In running the code block we should have recovered a comparable series of images with the pseudo-landmarks overlaid on top of them.  So how do our pseudo-landmarks look that we stored? Let's have a look!


```python
landmark_output
```




    [['name', 'plm_x', 'plm_y', 'SS_x', 'SS_y', 'TS_x', 'TS_y', 'CC_ratio'],
     ['B100_rep1_d10', 901, 1151, 894, 1171, 885, 1167, 179.7864077669903],
     ['B100_rep1_d10', 786, 1423, 789, 1402, 772, 1404, 51.358024691358025],
     ['B100_rep1_d10', 571, 1344, 592, 1336, 593, 1342, 136.75862068965517],
     ['B100_rep1_d10', 793, 1523, 796, 1512, 783, 1519, 77.3953488372093],
     ['B100_rep1_d10', 712, 1511, 735, 1508, 734, 1512, 165.04166666666666],
     ['B100_rep1_d10', 803, 1555, 796, 1538, 807, 1535, 205.4915254237288],
     ['B100_rep1_d10', 922, 1415, 898, 1420, 900, 1416, 133.18367346938774],
     ['B100_rep1_d10', 800, 1477, 816, 1459, 801, 1454, 48.89325842696629],
     ['B100_rep1_d11', 912, 1123, 905, 1142, 896, 1139, 201.4607843137255],
     ['B100_rep1_d11', 786, 1370, 792, 1350, 783, 1347, 91.42857142857143],
     ['B100_rep1_d11', 752, 1236, 761, 1252, 754, 1260, 181.62222222222223],
     ['B100_rep1_d11', 780, 1420, 780, 1398, 767, 1404, 57.92700729927007],
     ['B100_rep1_d11', 576, 1353, 595, 1343, 595, 1350, 153.0151515151515],
     ['B100_rep1_d11', 789, 1523, 791, 1511, 780, 1517, 61.134328358208954],
     ['B100_rep1_d11', 706, 1510, 728, 1506, 728, 1510, 136.6590909090909],
     ['B100_rep1_d11', 802, 1553, 791, 1532, 801, 1533, 206.36170212765958],
     ['B100_rep1_d11', 914, 1417, 893, 1423, 891, 1417, 145.4313725490196],
     ['B100_rep1_d11', 798, 1475, 807, 1466, 795, 1459, 57.52808988764045],
     ['B100_rep1_d12', 932, 1108, 925, 1131, 919, 1121, 200.4018691588785],
     ['B100_rep1_d12', 784, 1362, 793, 1343, 780, 1343, 51.891891891891895],
     ['B100_rep1_d12', 720, 1151, 730, 1170, 724, 1175, 176.05405405405406],
     ['B100_rep1_d12', 779, 1425, 779, 1402, 763, 1407, 43.62011173184357],
     ['B100_rep1_d12', 568, 1367, 585, 1358, 591, 1361, 140.91525423728814],
     ['B100_rep1_d12', 790, 1523, 789, 1511, 778, 1518, 67.28205128205128],
     ['B100_rep1_d12', 713, 1509, 736, 1506, 719, 1511, 162.19230769230768],
     ['B100_rep1_d12', 801, 1555, 790, 1534, 801, 1535, 221.1728971962617],
     ['B100_rep1_d12', 919, 1422, 897, 1426, 895, 1422, 130.59183673469389],
     ['B100_rep1_d12', 797, 1475, 807, 1467, 793, 1461, 53.073170731707314],
     ['B100_rep1_d13', 659, 1079, 673, 1097, 670, 1101, 140.7],
     ['B100_rep1_d13', 771, 1425, 770, 1405, 753, 1408, 60.04938271604938],
     ['B100_rep1_d13', 560, 1373, 581, 1362, 581, 1368, 164.28571428571428],
     ['B100_rep1_d13', 784, 1526, 784, 1506, 771, 1518, 54.060344827586206],
     ['B100_rep1_d13', 714, 1512, 736, 1507, 736, 1513, 137.76923076923077],
     ['B100_rep1_d13', 798, 1557, 784, 1543, 796, 1539, 210.76404494382024],
     ['B100_rep1_d13', 916, 1423, 900, 1423, 892, 1421, 128.0],
     ['B100_rep1_d13', 789, 1480, 799, 1473, 787, 1464, 54.4367816091954],
     ['B100_rep1_d13', 971, 1115, 958, 1132, 950, 1125, 193.18584070796462],
     ['B100_rep1_d13', 776, 1355, 784, 1337, 771, 1332, 64.0]]



This looks like it saved quite a bit more than an X-Y coordinates and a name for the file it came from...  We glossed over a few of the acute outputs in the previous exercise but it's probably worth sitting down and thinking about what they are now.  

If we look at the first 3 'columns' of this output we can see that there are names that correspond to our original files alongside a X-Y coordinate list which represents the plms we've been plotting.  So what these other SS and TS coordinates that we seem to be storing as well? Let's review a graph we've seen before in the previous exercise and then discuss...


```python
chain_pos=range(0, len(chain))

#Plot results
fig1=plt.plot(chain_pos, chain, color='black')
fig1=plt.axhline(y=thresh, color='r', linestyle='-')
fig1=plt.title('Angle scores by position')
plt.show(fig1)
```


![png](output_13_0.png)


This is that waveform we've been introduced to before that defines our landmarks acute is generating.  Notice that as we walk along this contour there are clearly a consecutive span of points defining an acute 'region' rather than and clear point in space (hence why we have a little valley of low angles rather than an abrupt dip)? When a pseudo-landmark is defined the midpoint of each of these valleys is taken as THE 'pseudo-landmark' and the ends of either side of these acute regions is stored as well and defined as the 'acute region start site (SS)' and the 'acute region termination site (TS)' (yes, this terminology may have been appropriated from molecular biology).  So in fact we're actually storing a bit of extra spatial information than what is needed to plot as we generate our pseudo-landmarks.  

Now that we solved that mystery let's run 'landmark_output' and pick up where we left off...


```python
landmark_output
```




    [['name', 'plm_x', 'plm_y', 'SS_x', 'SS_y', 'TS_x', 'TS_y', 'CC_ratio'],
     ['B100_rep1_d10', 901, 1151, 894, 1171, 885, 1167, 179.7864077669903],
     ['B100_rep1_d10', 786, 1423, 789, 1402, 772, 1404, 51.358024691358025],
     ['B100_rep1_d10', 571, 1344, 592, 1336, 593, 1342, 136.75862068965517],
     ['B100_rep1_d10', 793, 1523, 796, 1512, 783, 1519, 77.3953488372093],
     ['B100_rep1_d10', 712, 1511, 735, 1508, 734, 1512, 165.04166666666666],
     ['B100_rep1_d10', 803, 1555, 796, 1538, 807, 1535, 205.4915254237288],
     ['B100_rep1_d10', 922, 1415, 898, 1420, 900, 1416, 133.18367346938774],
     ['B100_rep1_d10', 800, 1477, 816, 1459, 801, 1454, 48.89325842696629],
     ['B100_rep1_d11', 912, 1123, 905, 1142, 896, 1139, 201.4607843137255],
     ['B100_rep1_d11', 786, 1370, 792, 1350, 783, 1347, 91.42857142857143],
     ['B100_rep1_d11', 752, 1236, 761, 1252, 754, 1260, 181.62222222222223],
     ['B100_rep1_d11', 780, 1420, 780, 1398, 767, 1404, 57.92700729927007],
     ['B100_rep1_d11', 576, 1353, 595, 1343, 595, 1350, 153.0151515151515],
     ['B100_rep1_d11', 789, 1523, 791, 1511, 780, 1517, 61.134328358208954],
     ['B100_rep1_d11', 706, 1510, 728, 1506, 728, 1510, 136.6590909090909],
     ['B100_rep1_d11', 802, 1553, 791, 1532, 801, 1533, 206.36170212765958],
     ['B100_rep1_d11', 914, 1417, 893, 1423, 891, 1417, 145.4313725490196],
     ['B100_rep1_d11', 798, 1475, 807, 1466, 795, 1459, 57.52808988764045],
     ['B100_rep1_d12', 932, 1108, 925, 1131, 919, 1121, 200.4018691588785],
     ['B100_rep1_d12', 784, 1362, 793, 1343, 780, 1343, 51.891891891891895],
     ['B100_rep1_d12', 720, 1151, 730, 1170, 724, 1175, 176.05405405405406],
     ['B100_rep1_d12', 779, 1425, 779, 1402, 763, 1407, 43.62011173184357],
     ['B100_rep1_d12', 568, 1367, 585, 1358, 591, 1361, 140.91525423728814],
     ['B100_rep1_d12', 790, 1523, 789, 1511, 778, 1518, 67.28205128205128],
     ['B100_rep1_d12', 713, 1509, 736, 1506, 719, 1511, 162.19230769230768],
     ['B100_rep1_d12', 801, 1555, 790, 1534, 801, 1535, 221.1728971962617],
     ['B100_rep1_d12', 919, 1422, 897, 1426, 895, 1422, 130.59183673469389],
     ['B100_rep1_d12', 797, 1475, 807, 1467, 793, 1461, 53.073170731707314],
     ['B100_rep1_d13', 659, 1079, 673, 1097, 670, 1101, 140.7],
     ['B100_rep1_d13', 771, 1425, 770, 1405, 753, 1408, 60.04938271604938],
     ['B100_rep1_d13', 560, 1373, 581, 1362, 581, 1368, 164.28571428571428],
     ['B100_rep1_d13', 784, 1526, 784, 1506, 771, 1518, 54.060344827586206],
     ['B100_rep1_d13', 714, 1512, 736, 1507, 736, 1513, 137.76923076923077],
     ['B100_rep1_d13', 798, 1557, 784, 1543, 796, 1539, 210.76404494382024],
     ['B100_rep1_d13', 916, 1423, 900, 1423, 892, 1421, 128.0],
     ['B100_rep1_d13', 789, 1480, 799, 1473, 787, 1464, 54.4367816091954],
     ['B100_rep1_d13', 971, 1115, 958, 1132, 950, 1125, 193.18584070796462],
     ['B100_rep1_d13', 776, 1355, 784, 1337, 771, 1332, 64.0]]



At this point the first 7 'columns' we're looking at here should make some intuitive sense for what they are representing. However, we still have one last variable left we're storing which is unclear in it's role.  This is a special variable we've created within acute using the volume generated between the plm, the SS, and the TS called the 'convexity-concavity ratio' or 'CC-ratio' for short.  What could this be used for? Let's take a look at our last mask again just to get a bit of context here.


```python
#Plot results
colorized_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
img_mask_plm = cv2.hconcat((colorized_mask, img_plms))

#Plot results
fig1=plt.figure(figsize=(21, 10))
fig1=plt.imshow(img_mask_plm, 'gray')
fig1=plt.xscale('linear')
fig1=plt.axis('off')
fig1=plt.title('Binary mask of plant and plms generated from this contour respectively')
plt.show(fig1)
```


![png](output_17_0.png)


As we look at our landmarks (white points) against our mask we used to generate them notice that we're retrieving both our leaf tips and our ligules (i.e. the joints where the leaves meet the 'stem')? Now remember that our 'CC-ratio' was computed using the volume of the space between our plm, SS, and TS? If we were to draw a triangle around a leaf tip and a ligule it seems like the average pixel color could differ pretty drastically right? If we go back up and look at our CC-ratio's we'll notice that they range between 0 and 255 (the range of standard pixel intensities) with each one representing an average pixel intensity of all pixels internal to this volume we've specified.  Thus, we could expect values closer to black (0) to be more common in our ligules and values closer to white (255) to be more common in our leaf tips.  Thus we can use this range as a score to specify convex regions of the contour as being closer to 255 and concave regions of the contour to be closer to 0.  Although it seems like we just did a bunch of extra work for no reason in generating this meta-data we'll get to see why this strategy was so important within our third and final exercise to learn the general operations of acute.  


```python

```


```python

```
