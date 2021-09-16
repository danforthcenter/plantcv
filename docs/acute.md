## Homology: Acute

Identify landmark positions within a contour for morphometric analysis

**plantcv.homology.acute**(*img, obj, mask, win, threshold*)

**returns**

homolog_pts = pseudo-landmarks selected from each landmark cluster

start_pts   = pseudo-landmark island starting position; useful in parsing homolog_pts in downstream analyses

stop_pts    = pseudo-landmark island end position ; useful in parsing homolog_pts in downstream analyses

ptvals      = average values of pixel intensity from the mask used to generate cont; 
useful in parsing homolog_pts in downstream analyses

chain       = raw angle scores for entire contour, used to visualize landmark clusters

- **Parameters:**
    - img - The original image, used for plotting purposes
    - obj - A contour of the plant object
    - mask - Binary mask used to generate contour array (necessary for ptvals)
    - win - The maximum cumulative pixel distance window for calculating angle score; 1 cm in pixels often works well
    - thresh - Angle score threshold to be applied for mapping out landmark coordinate clusters within each contour
- **Context:**
    - Used to identify pseudo-landmark positions along the contour of a plant for morphometric analysis 



**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/homology/acute.py)
