## Check a Naive Bayes Multiclass Samples File

[naive_bayes_multiclass](naive_bayes_multiclass.md) automatically runs this check on the input samples file before
training starts. If the file has any problems, training aborts and problems are printed with a line
number so you know exactly what to fix.
You can also call this function directly, for example while building a samples file by hand.

Problems are grouped into categories, and each category is capped at `max_errors` example messages so that one
pervasive problem (e.g. the wrong delimiter) does not mask a rarer problem elsewhere in the file. The
categories are:

- **Delimiter problems** - the header only has 1 column, which usually means the file isn't tab-delimited.
- **Header problems** - an empty or duplicate class label in the header row.
- **Wrong column count** - a data row's number of tab-delimited columns doesn't match the header.
- **Invalid RGB values** - a cell isn't exactly 3 comma-separated values, or a value isn't an integer between 0
  and 255.
- **Classes with no samples** - a class in the header never received a single valid sampled pixel.

**plantcv.learn.check_samples_file**(*samples_file, max_errors=20*)

**returns** valid

- **Parameters:**
    - samples_file - (str): Path to a text file containing a table of RGB values sampled for each feature class.
    - max_errors    - (int): Maximum number of example messages to print per problem category (default 20).
- **Context:**
    - Used to diagnose formatting problems in a `naive_bayes_multiclass` samples file before training.

```python
from plantcv.learn import check_samples_file

valid = check_samples_file("sampled_rgb_points.txt")
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/learn/naive_bayes.py)
