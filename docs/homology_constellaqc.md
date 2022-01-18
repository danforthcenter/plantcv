## Homology: ConstellaQC

Quality-control checks for pseudo-landmark homology groupings

**plantcv.homology.constellaqc**(*denovo_groups, annotated_groups*)

**returns** dataframe of grouped pseudo-landmarks and a group ID counter

- **Parameters:**
    - denovo_groups - A pandas array representing homology groups predicted by Constella for plms
    - annotated_groups - A pandas array representing the true biological identities of plms
- **Context:**
    - Used to check the accuracy of pseudo-landmark homology groupings
- **Example use:**
    - [Use In Homology Tutorial](tutorials/homology_tutorial.md)


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

pcv.homology.constellaqc(denovo_groups=landmark_pandas, annotated_groups=landmark_feat_standards)

# Known Feature-Predicted Group Scoring Matrix:

#          1   2   3   4   5   6   7   8   9   10
# base      4   0   0   0   0   0   0   0   0   0
# leaf2     0   0   0   4   0   0   0   0   0   0
# leaf3     0   0   0   0   0   4   0   0   0   0
# leaf4     0   0   0   0   4   0   0   0   0   0
# leaf5     0   0   0   0   0   0   0   4   0   0
# leaf6     0   0   0   0   0   0   0   0   0   3
# ligule2   0   4   0   0   0   0   0   0   0   0
# ligule3   0   0   4   0   0   0   0   0   0   0
# ligule4   0   0   0   0   0   0   4   0   0   0
# ligule5   0   0   0   0   0   0   0   0   3   0
# 
# 
# Valid Call Rate:      100.0 %
# Splitting Call Rate:  0.0 %
# Clumping Call Rate:   0.0 %

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/homology/constellaqc.py)
