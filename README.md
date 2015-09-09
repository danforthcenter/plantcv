# PlantCV

This is a general guide on how to cite and contribute to PlantCV (which we hope you will do).
Of course, this is not a comprehensive guide so if you have questions on contributions for PlantCV
the best thing to do is to put them [here](https://github.com/danforthcenter/plantcv/issues) so we can make sure your question gets answered.

Cheers!  
Malia, Max and Noah



##Table of Contents:
1.  [Introduction to PlantCV](#introduction)
1.  [Issues with PlantCV](#issueswithplantcv)  
2.  [PlantCV Contributor's Guide](#plantcvcontributorsguide)  
  *  [New Code to PlantCV](#newcode)  
  *  [Maintain PlantCV](#maintainplantcv)  
  *  [New Function Requests](#newfunctionrequesnts)  
  *  [Contribution Style Guide](#styleguide)

---
##<a id="introduction"></a>Introduction to PlantCV

PlantCV<sup>1</sup> is an imaging processing and trait extraction package and specific for plants
that is built upon open-source software platforms <a href="http://opencv.org/">OpenCV</a> <sup>2</sup>,
<a href="http://www.numpy.org/">NumPy</a> <sup>4</sup>, and <a href="http://matplotlib.org/">MatPlotLib</a> <sup>4</sup>.

If you use PlantCV please cite us.<sup>1</sup>

*  Installation instructions can be found [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/installation.html)

*  Further documentation for PlantCV functions and use can be found at the [PlantCV Website](http://plantcv.danforthcenter.org/pages/documentation/)

*  Test image sets can be found [here](http://plantcv.danforthcenter.org/pages/data.html), we recommend first testing with sets from the Danforth Center.

*  We recommend reading Reference 1, the first publication to detail PlantCV and provide examples of functionality.

Citations:

  1. Fahlgren N, Feldman M, Gehan MA, Wilson MS, Shyu C, Bryant DW,
     Hill ST, McEntee CJ, Warnasooriya SN, Kumar I, Ficor T,
     Turnipseed S, Gilbert KB, Brutnell TP, Carrington JC, Mockler TC,
     Baxter I.
     A versatile phenotyping system and analytics platform reveals
     diverse temporal responses to water availability in *Setaria*.
     Molecular Plant. 2015.
     http://doi.org/10.1016/j.molp.2015.06.005
  2. Bradski G (2000) The opencv library. Doctor Dobbs Journal 25(11):120-126.
  3. Oliphant TE (2007) Python for Scientific Computing. Computing in Science & Engineering, 9, 10-20.
  4. Hunter JD (2007) Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9, 90-95.

___

## <a id="issueswithplantcv"></a>Issues with PlantCV?

  * Please add any PlantCV suggestions/issues/bugs [here](https://github.com/danforthcenter/plantcv/issues).
  Please check to see if the issue is already open.  

---

## <a id="plantcvcontributorsguide"></a>PlantCV Contributor's Guide

___

This document aims to give an overview of how to contribute to PlantCV.

Contribute in three ways:  
  1.  Add new code  
  2.  Maintain and improve existing code: fix bugs, improving quality or speed of functions, add more detailed documentation  
  3.  [Open](https://github.com/danforthcenter/plantcv/issues) issues and add suggestions to improve PlantCV  

**The general structure to contribute code is to Fork the PlantCV repository, make or fix code, move altered code to a new branch, then to submit a pull request, details are below**

PlantCV is licensed under a GPL 2.0 share-alike license to promote open-development of plant image processing functions,
please see license for more information.

___
###<a id="newcode"></a> New Code to PlantCV

In general, new contributions to PlantCV should benefit multiple users and extend the image processing or trait analysis power of PlantCV.  

What should/should not be added to PlantCV:
  *  New validated image processing functions are highly encouraged for contribution.  
  *  New validated trait extraction algorithms are highly encouraged for contribution.  
  *  Image processing pipeline scripts that are specific for your images should **not** be added to PlantCV,
  unless they solve an image processing problem that you believe applies to more than one platform/user,
  if you have questions don't hesitate to ask [here](https://github.com/danforthcenter/plantcv/issues).

Steps to adding new code are below.  

####  Step 1. Open a new "New Function Proposal" forum or address an exisiting "New Function Request".

  *  If you are interested in adding a completely new function to PlantCV please first add an issue to PlantCV [here](https://github.com/danforthcenter/plantcv/issues) with the label "New Function Proposal".
  This allow others to comment on the proposed function and is a way of letting other people know you're working on it.  
  *  If someone has requested a new function in the issues forum and you would like to address it,
  please post a comment on the issue to let others know that you would like to work on it.  

#### Step 2. Fork the PlantCV repository.

  *  Make additions and changes in Forked repository

#### Step 3. Test and validate new functions

  1.  Please make sure you follow our [style guide](#styleguide).  
  2.  Please write your function so that it can be used on multiple image types (for example, no hardcoded image sizes, or paths).  
  3.  Please test your images on images of different sizes/sources if possible.
  4.  When appropriate, functions should have a debug step included, so that other users can test them in their pipelines.

#### 4. Add working function/changes to a new Github Branch.

  *  By adding the new code to a GitHub branch we can move modular portions of code to PlantCV-dev more easily.
  *  Each new function should in its own branch, but functions are highly related they can be in the same branch.

#### 5. Add working function/changes to PlantCV-dev

  *  Add working functions to [PlantCV-dev](https://github.com/danforthcenter/plantcv/tree/master/lib/plantcv/dev) by generating a Pull-Request
  *  Please include a readme file with some information on the function.
  *  Once in PlantCV-dev, the function will be accessible to all PlantCV users, but they will need to call the function specifically.

#### 6. Write documentation

  *  Only code with full documentation will move to PlantCV.
  *  A [markdown](https://guides.github.com/features/mastering-markdown/) file should be sent to core contributors, for the documation format please refer to [PlantCV Documentation](http://plantcv.danforthcenter.org/pages/documentation/)

#### 7. Move to PlantCV (main)

  *  Once full documentation is available and core users have tested functions in PlantCV-dev to make sure that there are no conflicts or breaks we will move function to PlantCV

___
### <a id="maintainplantcv"></a> Maintain PlantCV

  *  To make changes to existing code please follow [new code instructions](#newcode)
  
___
### <a id="newfunctionrequests"></a> New Function Requests

  *  We highly encourage New Function Requests please put them [here](https://github.com/danforthcenter/plantcv/issues)

___
###<a id="styleguide"></a> Contribution Style Guide

  *  Include commenting whenever possible.
  *  Start code with import of modules, for example:
  
  ```python
    import numpy as np
    import cv2
    from . import print_image
  
  ```  

  *  Then follow that import with the fuction definition, here's our fill function:  
  
  ```python
  
  def fill(img, mask, size, device, debug=False):
  # Identifies objects and fills objects that are less than size
  # img = image object, grayscale. img will be returned after filling
  # mask = image object, grayscale. This image will be used to identify contours
  # size = minimum object area size in pixels (integer)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  ix,iy= np.shape(img)
  size1=ix,iy
  background=np.zeros(size1, dtype=np.uint8)
  
  # Find contours
  contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  #cv2.drawContours(background,contours,-1, (255,0,0),5, lineType=8,hierarchy=hierarchy)
  #print_image(background, str(device) + '_fillcheck'+ '.png')
  
  # Loop through contours, fill contours less than or equal to size in area
  for c,cnt in enumerate(contours):
    #if hierarchy[0][c][0]==-1:
      m = cv2.moments(cnt)
      area = m['m00']
      if area<=size:
        #cv2.fillPoly(img, pts = cnt, color=(0,0,0))
        cv2.drawContours(img,contours,c, (0,0,0),-1, lineType=8,hierarchy=hierarchy)
  if debug:
    print_image(img, (str(device) + '_fill' + str(size) + '.png'))

  return device, img
  
  ```

 *  Notice that a debug step to print the resulting image out is included. For image processing, or output image steps, a debug step should be an option.
 
 
