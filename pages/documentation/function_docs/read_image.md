---
layout: docs
title: Documentation
subtitle: Read Image
---

## Read Image

Reads image into numpy ndarray and splits the path and image filename. This is a wrapper of the OpenCV function [imread](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html).

<font color='blue'>**readimage(filename)**</font> 
    
- **Parameters:**   
  - filename- image file to be read (possibly including a path)

- **Context:**  
  - Reads in file to be processed  

- **Example use:**

  ```python
    import plantcv as pcv      
    pcv.readimage("home/malia/images/test-image.png")
  ```  
  
  - [Use In Tutorial]()  
   

