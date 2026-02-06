## Using PlantCV with Jupyter Notebooks

### About Jupyter

Jupyter Notebook is a web application that allows you to create
documents that contain code, outputs, and documentation. The code
in Jupyter Notebooks can be re-executed to refresh outputs after you
change a section of code. Jupyter Notebooks support many programming
languages. See [http://jupyter.org/](http://jupyter.org/).

### How to use PlantCV with Jupyter

Using PlantCV with Jupyter Notebooks allows users to develop analysis workflows 
with instant visualization of input and output images of each step. 
Jupyter Notebooks are a great way to develop an analysis workflow before running PlantCV workflows 
over many images.

**Step-by-step guide to using PlantCV in Jupyter Notebooks**

<iframe src="https://scribehow.com/embed/Using_PlantCV_with_Jupyter_Notebooks__Jnhb53WlTtqohKYR8_UUfA" width="640" height="640" allowfullscreen frameborder="0"></iframe>

---

### Example of PlantCV running in Jupyter

![Screenshot](img/documentation_images/jupyter/jupyter_screenshot.jpg)

PlantCV is automatically set up to run in Jupyter Notebook but you will need to install Jupyter in your 
environment if you have not already.
For example, with `conda`:

```bash
conda install nb_conda jupyterlab
```

Then you can launch Jupyter from the command line `jupyter lab` and create a notebook using
a kernel containing your PlantCV environment. 

First, we use [matplotlib](http://matplotlib.org/) to do the
in-notebook plotting. To make this work, add the following to the top
of your notebook:

```python
%matplotlib inline
```

Second, you can import the PlantCV library like normal:

```python
from plantcv import plantcv as pcv
```

Third (optionally), utilize PlantCV's [WorkflowInputs](parallel_workflow_inputs.md#jupyter-notebook-inputs) class to
organize and name workflow inputs for compatibility with running the workflow later in parallel.

PlantCV has a built-in debug mode that is set to `None` by 
default. Setting debug to `"print"` will cause PlantCV to print debug
images to files, which is the original debug method. In Jupyter, setting
debug to `"plot"` will cause PlantCV to plot debug images directly into
the notebook.

Bringing it all together, the first part of a notebook running PlantCV
would look like the following example:

```python
%matplotlib inline
from plantcv import plantcv as pcv
from plantcv.parallel import WorkflowInputs

# Set input variables
args = WorkflowInputs(images=["./input_color_img.jpg"],
                      names="image",
                      result="plantcv_results.csv",
                      debug="plot")

# Set variables
pcv.params.debug = args.debug

```

### Converting Jupyter Notebooks to PlantCV workflow scripts

Once a workflow has been developed, it needs to be converted into a pure
Python script if the goal is to use it on many images using the PlantCV
workflow [parallelization](pipeline_parallel.md) tools. To make a
Python script that is compatible with the `plantcv-run-workflow` program,
first use Jupyter to convert the notebook to Python. This can be done
through the web interface (File > Save and Export Notebook As... > Executable Script),
or on the command line:

```bash
jupyter nbconvert --to python notebook.ipynb
```

The resulting Python script will be named `notebook.py` in the example
above. Next, open the Python script with a text editor. Several
modifications to the script are needed. Modify the list of imported
packages as needed, but in particular, remove
`get_ipython().magic('matplotlib inline')`. Change `from plantcv.parallel import WorkflowInputs`
to `from plantcv.parallel import workflow_inputs`.

Change the code for managing inputs, for example:

```python
args = WorkflowInputs(images=["./input_color_img.jpg"],
                      names="image",
                      result="plantcv_results.csv",
                      debug="plot")
```

To:

```python
args = workflow_inputs()
```

See [workflow_inputs](parallel_workflow_inputs.md#parallel-workflow-inputs) for more details.

Make any other alterations as necessary after testing. Based on the
simple Jupyter Notebook example above, the fully modified version would
look like the following:

```python
from plantcv import plantcv as pcv
from plantcv.parallel import workflow_inputs

# Get command-line options
args = workflow_inputs()

# Set variables
pcv.params.debug = args.debug  # Replace the hard-coded debug with the debug flag

img, imgpath, imgname = pcv.readimage(filename=args.image)

# Put workflow 
# steps from 
# Jupyter here

# Print data that gets collected into the Outputs 
pcv.outputs.save_results(filename=args.result, outformat="json")
    
```
### Combining Jupyter Notebook Outputs for Data Analysis

In the case where creating a parallel workflow is not convenient (e.g. image sets where ROIs or other parameters must be adjusted between images), it is possible to run all images individually through Jupyter Notebook and then combine the JSON outputs into a larger JSON. The resulting file will look and function similarly to the result.json of a parallel workflow and can be used for downstream data analysis.

For all images whose data should be combined, the output JSONs should be moved to a new, separate folder. The files can then be combined using the process outlined on the [Process Results](parallel_process_results.md) page and plantcv-utils json2csv ([documentation](https://plantcv.readthedocs.io/en/stable/tools/#convert-output-json-data-files-to-csv-tables)).

