## Summary of Output Measurements and Units

1. Analyze Object Function:  
    - Object Area - object area, pixels (units)  
    - Convex-Hull Area - area of convex-hull, pixels (units)  
    - Solidity - Ratio, object area divided by convex hull area.  
    - Object Perimeter Length - pixels (units)  
    - Object Width (extent x) - pixels (units)  
    - Object Height (extent y) - pixels (units)  
    - Longest Axis - pixels (units)  
    - Center of Mass-X - x-coordinate, pixels (units)  
    - Center of Mass-Y - y-coordinate, pixels (units)  
    - Hull Vertices - number of convex-hull vertices  
    - In Bounds - True or False (if False the object is touching top of image)  
    - Object Bounding Ellipse Center-X - x-coordinate, pixels (units)  
    - Object Bounding Ellipse Center-Y - y-coordinate, pixels (units)  
    - Object Bounding Ellipse Major Axis - length of major axis of bounding ellipse, pixels (units)  
    - Object Bounding Ellipse Minor Axis - length of minor axis of bounding ellipse, pixels (units)  
    - Object Bounding Ellipse Angle - rotation of ellipse in degrees  
    - Object Bounding Ellipse Eccentricity - ratio, 'roundness' of object (a perfect circle is 0, ellipse is greater than 0 but less than 1)  
 
---

2. Analyze Color Function:  
    - Red Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Green Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Blue Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Hue Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Saturation Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Value Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Lightness Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Green-Magenta Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Blue-Yellow Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  

----  
  
3. Analyze Bound Function:  
    - Y-Position - Height of the bound line used for measurement (height from bottom of image), pixels (units)  
    - Height-Above-Bound - Extent-y of object above bound line, pixels (units)  
    - Height-Below-Bound - Extent-y of object below bound line, pixels (units)  
    - Area-Above-Bound - area of object above bound line, pixels (units)  
    - Area-Below-Bound - area of object below bound line, pixels (units)  
    - Percent-Above-Bound - percentage of total area above the bound line  
    - Percent-Below-Bound - percentage of total area below the bound line  

---  
  
4. Analyze NIR Intensity Function:  
    - Bins - bin values based on number of bins set by user  
    - Signal Histogram - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)     
    
---    
    
5. PSII-FV/FM Function:  
    - Bin-number - number of bins set by user  
    - FV/FM Bins - bin values based on number of bins set by user  
    - FV/FM Histogram - histogram of FV/FM ratio values for object  
    - FV/FM Histogram Peak - bin value of histogram peak (greatest number of pixels)  
    - FV/FM Median - bin value of histogram median  
    - F-Dark Passed QC - Check (True or False) to determine if Fdark image does not have pixel intensity values above 2000. 
  
---  
  
6. Report Size Marker Function:  
    - Marker-Area - area of marker, pixels (units)
    - Marker Bounding Ellipse Major Axis - length of major axis of bounding ellipse, pixels (units)  
    - Marker Bounding Ellipse Minor Axis - length of minor axis of bounding ellipse, pixels (units)  
    - Marker Bounding Ellipse Eccentricity - ratio, 'roundness' of object (a perfect circle is 0, ellipse is greater than 0 but less than 1)  
   
---  
  
7. Watershed Segmentation Function:  
    - Estimated-Object-Count - number of objects (e.g. estimated leaf count)  
    