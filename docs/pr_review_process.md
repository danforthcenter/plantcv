# Pull Request Review Process

### Pull Request Author Guidelines

1. PRs (Pull Requests) should be modular and as targeted as possible.
2. PRs for new features should focus on a minimum viable product. Embellishments can be added in additional PRs.
3. PRs should not contain unrelated changes as much as possible. Open a new PR for unrelated changes.
4. Commits for PRs should be succinct but descriptive. Try to avoid trivial “update file.py” type commit messages.
5. When a PR is ready for review, apply the “ready to review” label. At this point, additional changes should only be made if necessary or as part of the review. Let the team know it’s ready so someone can volunteer to review it.

### Overview

!!! note
    The steps below do not necessarily need to be followed precisely in this order. Not all PRs will require all steps and some will not require an in-depth review at all (e.g., minor documentation updates).

### Step 0: Set up a local PlantCV environment for the branch being reviewed

1. Read through the steps of the [contributing guide](CONTRIBUTING.md).
2. Email plantcv@danforthcenter.org to get added as a contributor.
3. [Install PlantCV from the source code](installation.md#installation-from-the-source-code)
4. Activate the plantcv environment, then change the current directory to the location where plantcv is installed.  Then, run `git checkout <pull-request-branch>` to navigate to the branch to be reviewed.

### Step 1: Familiarize yourself with the PR

Before starting the review it is convenient to understand the type of update and/or the intended functionality.  

1. Inspect the files changed. 
2. Read the updated documentation. To compile the documentation locally, run: `mkdocs serve --theme readthedocs` in a local terminal with an activated PlantCV environment (Testing the documentation is done in step 4). 

### Step 2: Prepare materials for the review

1. Maintain a shared team directory for reviews (data and notebooks) in the PlantCV Google Drive. Email plantcv@danforthcenter.org from a Gmail account to have the team share access to this Google Drive.
2. Find appropriate sample data (either already in the shared directory or new data), ideally not data used by the PR author.
3. Update your local development environment to use the PR branch.
4. Create a new Jupyter notebook named `pr<num>_<short description>.ipynb`

### Step 3: Review the PR functionality

Read the PR documentation and use your intuition to run relevant parts of PlantCV to test the PR code. For example, test upstream and downstream functionality to ensure the new function works well with other steps in a workflow. Try more than one data type if a function works on both RGB and grayscale. Potential findings to report to the PR author and/or to propose fixes for:

1. **Errors**: the code does not work as written or does not function as intended (on new data for example).
2. **Process**: in using the code, you think the process can be simplified or made clearer (e.g., fewer inputs, renamed arguments, etc.).
3. **Documentation**: both the documentation and docstrings should match the code in terms of syntax and process.

Iterate as needed.

### Step 4: Review the tests

1. Do all tests pass?
    1. Running relevant tests locally: `py.test --cov=plantcv -k test_name_or_keywords` in a local terminal with an activated PlantCV environment. If you get an error, make sure pytest-cov is installed in your environment (e.g. `conda install pytest-cov`)
2. Does coverage remain at 100%?
3. Do any new or modified tests accurately test the PR code?

Propose updates as needed.

### Step 5: Test the documentation

Reviewing the documentation code is important, but compiling the documentation locally ensures that the resulting pages are rendered correctly. The easiest way to view the documentation live on your local machine is to run: `mkdocs serve --theme readthedocs` in a local terminal with an activated PlantCV environment

Some common oversights that are hard to see in the code but easy to detect in the compiled documentation:

1. New pages are not added to the table of contents `plantcv/mkdocs.yml` (mkdocs will display a warning when you run the command above).
2. Typos in page or image filenames (mkdocs will often display a warning, or the image may appear as a broken link).
3. Typos in formatting markup lead to incorrectly displayed styling (e.g., not closing bold or italics, not having a blank line before a bulleted or numbered list, etc.).
4. Changes to function input/output signatures or new functions should be added to updating.md.
5. Link out to source code at the end of a documentation page.

### Step 6: Review the code

Once the PR is working as intended, review the code itself for potential improvements. Some common types of improvements to suggest:

1. **Uniform style (linting)**: Most IDEs, including PyCharm and VScode, will indicate when the code does not match the community style guides laid out in PEP8. The command-line tool `flake8` can also be used if an IDE that supports these checks cannot be used. A report from deepsource.io is also generated automatically for each PR.
2. **Code simplification**: Any reorganization that makes the code more succinct, readable, maintainable, etc. In particular, complex, nested logical blocks and for loops increase code complexity (and testing demand). The deepsource.io report may also included automated suggestions for code simplification. 
3. **Algorithmic improvement**: Could potentially be an alternate approach that is significantly faster or more user-friendly.
4. **Scope**: Check any new code and test data in the `plantcv/tests` module (no need to fix out-of-scope linting issues).
5. **Documentation**: The documentation is more flexible, but try to avoid very long lines. Markdown will automatically connect consecutive lines that do not have a blank line between them. Crop down images in documentation. In general, resizing such that the image width is equal to 400px will result in a documentation page that is still mobile friendly.
6. **Unnecessary New Test Data**: If new test data was added, check if an existing test data could be used to save memory.

Communicate via GitHub with PR author(s) and directly contribute changes to the PR branch as appropriate until it is ready to merge.

### Step 7: Approve the PR

Once you and the PR author have refined the PR and it is ready to merge, the PR can be approved. It’s important that the PR not be approved until it is actually ready to merge. Please add the name of the Jupyter notebook used for review, in the shared directory (but not a link to it) to the PR approval.