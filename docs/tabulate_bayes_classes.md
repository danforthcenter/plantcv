## Tabulate Naive Bayes Classes

Tabulate pixel RGB values into a table for naive Bayes training.

**plantcv.tabulate_bayes_classes**(*input_file, output_file*)

**returns** none

- **Parameters:**
    - input_file   = Input text file of class names and RGB values
    - output_file  = Output file for storing the tab-delimited naive Bayes training data


- **Context:**
    - The input file should have class names preceded by the "#" character. RGB values can be pasted
    directly from ImageJ without reformatting. E.g.:

    ```python
    #plant
    96,154,72	95,153,72	91,155,71	91,160,70	90,155,67	92,152,66	92,157,70
    54,104,39	56,104,38	59,106,41	57,105,43	54,104,40	54,103,35	56,101,39	58,99,41	59,99,41
    #background
    114,127,121	117,135,125	120,137,131	132,145,138	142,154,148	151,166,158	160,182,172
    115,125,121	118,131,123	122,132,135	133,142,144	141,151,152	150,166,158	159,179,172
    ```


- **Example use:**

```python
from plantcv import plantcv as pcv      

i
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/utils/converters.py)
