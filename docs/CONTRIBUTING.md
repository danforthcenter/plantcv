# How to contribute

This document aims to give an overview of how to contribute to PlantCV.
We encourage contributions in a variety of forms. There are
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
	- Where applicable, provide the full workflow prior to the error and the image getting analyzed. 

## Contributing Text or Code

### Overview

When you add a significant **new feature**, please create an issue
first, to allow others to comment and give feedback. 

When you have created a new feature or other changes to existing
code, create a 'pull request'.

**Branching and Pull Requests**: All contributors to PlantCV code or documentation are required to use the 
*feature branch workflow* (below) in order to allow pull
requests, automated testing, and code review.

### Setting up a development environment

!!! note
    Before setting up a development environment, choose between one of two methods for working with the PlantCV
    repository. 1) Use the [fork method](https://guides.github.com/activities/forking/) to create a personal copy of
    PlantCV where you will make changes and synchronize them back to the main PlantCV repository; or 2) Send us a
    request to be added as a collaborator on the PlantCV repository so that you can work with it directly instead of
    having to manage a separate repository.

#### Clone the source code from GitHub

After choosing a method above for accessing PlantCV source code, create a clone of the source code GitHub repository
using one of the methods described in the 
[GitHub cloning a repository guide](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

#### Install PlantCV dependencies

We recommend using `conda` to set up a virtual environment for developing PlantCV. Instructions can be found in the
[installation documentation](installation.md#installation-from-the-source-code).

#### Create a branch to do your work

The PlantCV default branch is protected and does not allow direct modification. A better practice is to 
[create a branch](https://docs.github.com/en/free-pro-team@latest/desktop/contributing-and-collaborating-using-github-desktop/managing-branches)
to add modifications to. The name of the branch should be descriptive and can potentially contain a related issue 
number. This makes it easier to find out the issue you are trying to solve and helps us to understand what is done in
the branch. Calling a branch my-work is confusing. Names of branch can not have a space, and should be replaced with 
a hyphen.

#### Work and commit

Do your work and commit as you see fit to check your work into your branch. Descriptive commit messages and 
descriptions are helpful for understanding the purpose of changes.

#### Testing and documenting your code

In addition to adding a new feature, test your code thoroughly:

PlantCV utilizes [GitHub Actions](https://github.com/features/actions), [Codecov](https://codecov.io/), and 
[Read the Docs](https://readthedocs.org/) to provide continuous integration of unit testing and documentation. 
Integration with GitHub Actions allows us to test whether new pull requests break or change the output of existing 
functions. Codecov tells us the percentage of PlantCV repository code that is covered by the unit tests (the better
the coverage the more likely we are to catch problematic pull requests). To include new functions in GitHub Actions 
tests (to make sure they aren't broken by future pull requests) we need a 'unit test' or set of 'unit tests' (if you 
need more than one test to cover function options).

Existing unit tests can be found in `tests/tests.py` as examples.
The data to support unit tests can be found in the `tests/*data/` directories.

If you are updating existing code, make sure that the `test.py`
script passes on the function you modified. Testing locally can be done with pytest:

```bash
pytest tests/tests.py

# Or you can just run a subset of tests to save time
# This will run all tests with "analyze" in the test name 
pytest tests/tests.py -k analyze

```

Add documentation for your new feature (see [Adding/editing Documentation](documentation.md) for more details). A new 
Markdown file should be added to the docs folder, and a reference to your new doc file should
be added to the `mkdocs.yml` file. You can test that your new documentation can be built correctly locally using 
mkdocs from the root of your local plantcv repository.

```bash
mkdocs build --theme readthedocs --site-dir _site

```

#### Publish your branch to GitHub and create a Pull Request

[Publishing your branch](https://docs.github.com/en/free-pro-team@latest/desktop/contributing-and-collaborating-using-github-desktop/managing-branches#publishing-a-branch)
to GitHub will make it available for creating a pull request between the updates and the default branch of PlantCV.

After publishing your branch you can create a pull request to create a comparison between the branch and the default
branch of PlantCV. Generating a pull request will notify the maintainers of PlantCV. GitHub will report whether the
branch can be merged with the default branch without conflicts (clashes between two independent updates) or whether 
manual fixes are required. GitHub Actions will also generate an automatic build report on whether or not unit tests
pass under multiple version of Python and checks code coverage statistics. At least one code review by someone other
than the pull request author is required (think peer review but for code!). If updates to the pull request are needed,
new commits can be checked into the local clone of the PlantCV repository and synchronized to GitHub, the pull request
will automatically update when the branch is updated. Once tests pass, coverage is maintained or increased, and code
review is approved, the branch will be merged with the default branch and the updates are now part of the latest
version of PlantCV!

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
testing and documenting your code above. We are very appreciative of all community contributions to PlantCV! 
We do hope that if you are contributing new methods to PlantCV, you are also contributing documentation and unit 
tests for your functions (described below), because you understand your code/functionality best. If you have questions 
or need help don't hesitate to ask [here](https://github.com/danforthcenter/plantcv/issues).

#### New function style guide

Include commenting whenever possible.

In general functions should aim to be modular and accomplish single tasks with a minimum number of inputs and outputs.
There is not a clear cut rule on what is too much to lump together versus split apart but our general approach is to
create functions that apply a single transformation to the inputs and then build workflows by chaining together the
individual modules. However, if the objective is to take an input and always do x, y, and z steps then it may make sense
to include these all in one function rather than having the user combine them every time. When in doubt, please reach
out for input!

Start code with import of modules, for example:

```python
# Import external packages
import numpy as np
import cv2
import os

# Import functions from within plantcv
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
```

Here is a sample of a new function. Arguments should be defined.
Generally, functions should utilize the private function `_debug` to produce visualization results.
Users can set `pcv.params.debug`
to `None` (default), "print" (to file), or "plot" (to screen if using [Jupyter](jupyter.md) notebooks or X11).
Functions should also increment the `device` number, which is a counter for image processing steps that is 
autoincremented by functions that use `params`. Note that the inputs and outputs are documented with Python docstrings.

```python
# Import external packages
import numpy as np
import cv2
import os
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


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
    
    _debug(visual=returnval1, filename=os.path.join(params.debug_outdir, str(params.device) + '_new_function.jpg'))

    return returnval1

```

If you need to call other PlantCV functions from within your contributed function, be sure to disable debugging until 
you are ready to show your own debug images.

To do this, follow these four steps:
  1. Store the value of params.debug
  2. Temporarily set params.debug to None
  3. Call other PlantCV functions, and take any other steps
  4. Reset the debug mode to the stored value before printing/plotting your own debug image(s).

Here is a sample of a PlantCV function that calls on other PlantCV functions:

```python
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import example_plantcv_function
from plantcv.plantcv import another_plantcv_function


def new_function_calling_plantcv(img):
    """New function calling another plantcv function.
    
    Inputs:
    img       = description of img
    
    Returns:
    final_img = description of final img
    
    :param img: type
    :return final_img: type
    """

    # Increment the device number by 1
    params.device += 1

    # Store debug mode
    debug = params.debug
    # Temporarily disable debugging
    params.debug = None

    # No debug images will be shown for these functions
    modified_img = example_plantcv_function(img)
    final_img = another_plantcv_function(modified_img)

    # Reset debug mode
    params.debug = debug
    
    _debug(visual=final_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_new_function.jpg'))

    return final_img

```

### Thanks

Parts of this contribution guide are based on the
[TERRA-REF Contribution Guide](https://github.com/terraref/computing-pipeline).
