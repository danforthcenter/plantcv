## Evaluation of time-series linking result

This set of functions are designed to evaluate the time-series leaf tracking result by comparing to the ground-truth.

To start, get familiar with some notations and definitions:

**T**: total time

**N**: total number of unique leaves in ground truth

**n<sub>t</sub>**: number of leaves at time t

**li**: link info, a list of length (T-1)
- t-th element of li, i.e. li<sub>t</sub> represents how leaves at t (n<sub>t</sub> leaves) link to leaves at t+1 (n<sub>t+1</sub> leaves)
- length of li<sub>t</sub>: n<sub>t</sub>
- li<sub>t,i</sub>=j: the i-th leaf at time t is the j-th leaf at time t+1

**ti**: tracking info, a matrix (2d-array) of size (T,N)
- tk-th element of ti (ti<sub>t,k</sub>): (local) index of leaf k at time t if leaf k appears at time t, -1 others.
- Total number of non-negative elements in a t-th row: # of leaves at time t 
- Every column k: (local) indices for the leaf k at different timepoints(ts).

**N'**: total number of (unique) leaves in leaf tracking result

- *note: N=N' not necessary holds.*

**li'**: link info in tracking result

**ti'**: tracking info in tracking result

The performance of leaf tracking can be evaluated by 4 different scores:
1. linking score 
```
linking score = # correct matches / # total matches
```

2. unmatched leaf rate
```
if N' < N, unmatched leaf rate = (N-N')/N
otherwise, unmatched leaf rate = 0
```

3. fake new leaf rate
```
if N < N' <= 2N, fake new leaf rate = (N'-N)/N
if N'> 2N, fake new leaf rate = 1
otherwise, fake new leaf rate = 0
``` 
4. tracking score <br>
To define the tracking score, first define the confusion matrix **C** based on ti and ti'.
   - size: N&#215;N'
   - ij-th element C (C<sub>i,j</sub>): how many times for leaf i becomes leaf j when tracking.
   - row sum (*sum<sub>i</sub>*): total existence of leaf i in ground truth (i = 1,2,...,N)
   - column sum (*sum<sub>j</sub>*): total existence of leaf j in tracking result (j = 1,2,...,N')
   - tracking score for leaf i (*tracking-score<sub>i</sub>*):
        tracking-score<sub>i</sub>=C<sub>i,i</sub>/total existence of leaf i in ground truth
```
tracking score = summation tracking-score (for i = 1,...,N)/N
```     

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/time_series/evaluation.py)

