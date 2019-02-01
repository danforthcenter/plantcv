# How to contribute

This document aims to give an overview of how to contribute to PlantCV.
We encourage third-party contributions in a variety of forms. There are
a few guidelines that we need contributors to follow so that we can
keep things working for all users.

There are many ways to contribute:

* Report bugs
* Request features
* Join the discussion of open issues, features, and bugs
* Contribute algorithms to the library
* Add unit tests
* Revise existing code
* Add or revise documentation

If you need any help, please contact us.

## Creating Issues

- Make sure you have a GitHub account.
- Search GitHub and Google to see if your issue has already been reported
    - [Create an issue in GitHub](https://github.com/danforthcenter/plantcv/issues), 
    assuming one does not already exist.
	- Clearly describe the issue including steps to reproduce when it is a bug.
	- Make sure you fill in the earliest version that you know has the issue.

## Contributing Text or Code

### Overview

When you add a significant **new feature**, please create an issue
first, to allow others to comment and give feedback. 

When you have created a new feature or non-trivial change to existing
code, create a 'pull request'.

**Branching and Pull Requests**: Although core developers have write 
permissions to the PlantCV repository, 
*please use the feature branch workflow* (below) in order to allow pull
requests, automated testing, and code review.

### Using Git at the Command Line

Introduce your self to *git*, make sure you use an email associated with
your GitHub account. This can also be done with the GitHub desktop application.

```
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com
```

Fork the PlantCV repository to add it to your GitHub account.

[Fork this repository](https://github.com/danforthcenter/plantcv#fork-destination-box)

Clone your fork of this repository

```
git clone https://github.com/<your username>/plantcv.git
```

Setup repository to be able to fetch from the master

```
git remote add upstream https://github.com/danforthcenter/plantcv.git
```

### Adding Features and Submitting Changes

Always work in a branch rather than directly on the master 
branch. Branches should focus on fixing or adding a single feature or
set of closely related features because this will make it easier to 
review and merge your contributions. Since multiple people work on the 
same repository, make sure to keep your master branch in sync
with the master of the danforthcenter/plantcv repository. The master
branch is the central repository for stable releases and the latest code.

Here is a simplified workflow on how add a new feature:

#### Get the latest version

Update your master branch with the main PlantCV repository (both locally and on GitHub)

```
git fetch upstream
git checkout master
git merge upstream/master
git push
```

#### Create a branch to do your work

A good practice is to call the branch in the form of `plantcv-<issue-number>`
followed by the title of the issue. This makes it easier to find out the
issue you are trying to solve and helps us to understand what is done in
the branch. Calling a branch my-work is confusing. Names of branch can
not have a space, and should be replaced with a hyphen.

```
git checkout -b plantcv-issuenumber-title-of-issue
```

#### Work and commit

Do you work, and commit as you see fit. Make your commit messages helpful.

```
# Stage files to commit (. for all, or specfic list of files)
git add .

# Commit staged files with descriptive message
git commit -m "Helpful message about updates."
```

#### Push your changes up to GitHub

Pushing will update your fork of the PlantCV repository. If this is the
first time pushing to GitHub you will need to use the extended command
below, other wise you can simply do a `git push`.

```
git push -u origin plantcv-issuenumber-title-of-issue
```

#### Pull Request

Once your new feature is ready, create a pull request from your fork/branch 
to the main PlantCV repository. Generating a pull request will notify
the maintainers of PlantCV. GitHub will report whether the merge can be
done automatically without conflict, or whether manual fixes are 
required. Travis-CI will also generate an automatic build report on 
whether or not the updates break the automated unit tests.

### Guidelines for adding new features

In general, new contributions to PlantCV should benefit multiple users
and extend the image processing or trait analysis power of PlantCV. 

What should/should not be added to PlantCV:

*  New validated image processing functions are highly encouraged for contribution.  
*  New validated trait extraction algorithms are highly encouraged for contribution.
*  Image processing workflow scripts that are specific for your project 
should **not** be added to PlantCV since these are (usually) not
generalized or updated to maintain compatibility with new versions.

If you are adding new image processing functions or trait extraction algorithms, make sure you read the section on 
testing and documenting your code below. We are very appreciative of all community contributions to PlantCV! 
We do hope that if you are contributing new methods to PlantCV, you are also contributing documentation and unit 
tests for your functions (described below), because you understand your code/functionality best. If you have questions 
or need help don't hesitate to ask [here](https://github.com/danforthcenter/plantcv/issues).

#### Testing and documenting your code

In addition to adding a new feature, test your code thoroughly:

PlantCV utilizes [Travis CI](https://travis-ci.org/), [Coveralls](https://coveralls.io/), and 
[Read the Docs](https://readthedocs.org/) to provide continuous integration of unit testing and documentation. 
Integration with Travis CI allows us to test whether new pull requests break or change the output of existing functions.
Coveralls tells us the percentage of PlantCV repository code that is covered by the unit tests (better the coverage the 
more likely we are to catch problematic pull requests). To include new functions in Travis CI tests (to make sure they 
aren't broken by future pull requests) we need a 'unit test' or set of 'unit tests' (if you need more than one test to 
cover function options).

Existing unit tests can be found in `tests/tests.py` as examples.
The data to support unit tests can be found in `tests/data/`

If you are updating existing code, make sure that the `test.py`
script passes on the function you modified. Testing locally can be done with pytest:

```
cd plantcv
py.test -v tests/tests.py
```

Add documentation for your new feature (see [Adding/editing Documentation](documentation.md) for more details). A new 
Markdown file should be added to the docs folder, and a reference to your new doc file should
be added to the `mkdocs.yml` file. You can test that your new documentation
can be built correctly locally using mkdocs from the root of your local
plantcv repository.

```
mkdocs build --theme readthedocs --site-dir _site
```

#### New function style guide

Include commenting whenever possible.

Start code with import of modules, for example:

```python
# Import external packages
import numpy as np
import cv2

# Import functions from within plantcv
from . import print_image
```

Here is a sample of a new function. Arguments should be defined.
Generally, functions should utilize the global `debug` parameter from the [params](params.md) class.
Users can set `pcv.params.debug `
to None (default), "print" (to file), or "plot" (to screen if using [Jupyter](jupyter.md) notebooks or X11).
Functions should also increment the `device` number, which is a counter for image processing steps that is autoincremented by functions that use `params`.
Note that the inputs and outputs are documented with Python docstrings.

```python

def new_function(img):
    """New function.
    
    Inputs:
    img        = description of img
    
    Returns:
    returnval1 = return value 1
    
    :param img: type
    :return returnval1: type
    """
    
    # Increment the device number by 1
    params.device += 1

    returnval1 = some_code_on_img(img)
    
    if params.debug == "print":
        print_image(img, (str(params.device) + '_new_function.jpg'))
    elif params.debug == 'plot':
        plot_image(img)

    returnval1
```

### Thanks

Parts of this contribution guide are based on the
[TERRA-REF Contribution Guide](https://github.com/terraref/computing-pipeline).
