## Parallel workflow inputs management

### Jupyter Notebook inputs

Manage workflow inputs in Jupyter for compatibility with parallel workflow execution.

*class* **plantcv.parallel.WorkflowInputs(*images, names, result, outdir, writeimg, debug, \*\*kwargs*)**

#### Attributes

**images**: (list, required): list of input images.

**names**: (str, required): string containing a comma-delimited list of keyword names for each input image.

**result**: (str, required): path/name for the output results file.

**outdir**: (str, required): path/name of the output directory.

**writeimg**: (bool, default = `False`): If `True`, images will be saved.

**debug**: (str, default = `None`): If `None`, debug is off. "plot" or "print" displays or saves intermediate images.

**\*\*kwargs**: (dict, optional): dictionary of additional user-defined workflow keyword arguments.

#### Example

```python
# In Jupyter
%matplotlib inline
from plantcv import plantcv as pcv
from plantcv.parallel import WorkflowInputs

# Define workflow inputs
args = WorkflowInputs(images=["rgb_image.jpg", "nir_image.jpg"],
                      names="rgb,nir",
                      result="results.json",
                      outdir=".",
                      writeimg=True,
                      debug="plot",
                      **{"myinput": "myvalue"})

# Example of how the inputs are mapped into args
print(args.__dict__)
# {'result': 'results.json', 'outdir': '.', 'writeimg': True, 'debug': 'plot', 'myinput': 'myvalue',
# 'rgb': 'rgb_image.jpg', 'nir': 'nir_image.jpg'}

# Workflow
pcv.params.debug = args.debug
rgb_img, rgbpath, rgbname = pcv.readimage(filename=args.rgb)
nir_img, nirpath, nirname = pcv.readimage(filename=args.nir)
# ...

```

### Parallel workflow inputs

The `WorkflowInputs` class is used to manage inputs in Jupyter where inputs are hardcoded for testing and workflow
development. After converting a notebook to a Python script for use with `plantcv-run-workflow`, `WorkflowInputs` is replaced
with the function `workflow_inputs`, which returns a very similar class based on the `argparse.Namespace` class.

**plantcv.parallel.workflow_inputs**(*\*other_args*)

**returns** an plantcv.parallel.workflow_inputs class object

* **Parameters**:
  * \*other_args - (list, optional): list of additional user-defined workflow inputs.
* **Context**:
    * Used to parse command-line inputs to the workflow. Inputs are constructed by `plantcv-run-workflow`.
* **Example use**:
    * [Converting from Jupyter to Python](jupyter.md)

#### Checkpointing

If a parallel workflow is run with checkpointing (`config.checkpoint = True`) then a checkpointing file is made by
`workflow_inputs` when the `workflow_inputs` class object is initialized in each job. That file has the same name
as the temp file of image metadata but with the `"_attempt"` suffix. When `workflow_inputs.result` attribute is
accessed the checkpointing file is renamed to have the `"_complete"` suffix. In a typical workflow the `result`
attribute is only accessed when results are being saved (`pcv.outputs.save_results(filename= args.result, ...)`).
If you are accessing the `results` attribute for any other reason we recommend instead using the `_results` attribute
so that the `_complete` suffix is only used for checkpointing once results have been saved. By default `workflow_config`
sets `cleanup = True`, which will remove the `checkpoint` directory if the job runs to completion. For standard
checkpointing focused on running part of a dataset that did not run before a job was killed, etc, the default value works
well. 

Checkpointing also allows for continuous monitoring or interim analysis of a growing image dataset with a single configuration
file and a single workflow. A checkpointed parallel configuration will automatically skip images that have already been run and
only run new images or those that were not completed in a previous attempt. For checkpointing to work in this way you
need to have `config.cleanup` set to `False`, otherwise the checkpointing files will be deleted at the end of a successful workflow
which would prevent a future re-run from knowing which images were already analyzed. Note that there are many ways that you might
set up continuous monitoring or interim analyses and it may make more sense in your use case to have several configuration files
with different filters in place.

#### Example

The example Jupyter notebook above when exported as an Executable Script would look like the following:

```python
#!/usr/bin/env python
# coding: utf-8

# In[6]:


# In Jupyter
get_ipython().run_line_magic('matplotlib', 'inline')
from plantcv import plantcv as pcv
from plantcv.parallel import WorkflowInputs


# In[7]:


# Define workflow inputs
args = WorkflowInputs(images=["rgb_image.jpg", "nir_image.jpg"],
                      names="rgb,nir",
                      result="results.json",
                      outdir=".",
                      writeimg=True,
                      debug="plot",
                      **{"myinput1": "myvalue1",
                         "myinput2": "myvalue2"})


# In[8]:


# Example of how the inputs are mapped into args
print(args.__dict__)


# In[9]:


# Workflow
pcv.params.debug = args.debug


# In[ ]:


rgb_img, rgbpath, rgbname = pcv.readimage(filename=args.rgb)


# In[ ]:


nir_img, nirpath, nirname = pcv.readimage(filename=args.nir)


# In[ ]:


# ...

```

Converting it to use `workflow_inputs` would look like the following (comments and spacing optionally removed for brevity):

```python
#!/usr/bin/env python
# coding: utf-8
from plantcv import plantcv as pcv
from plantcv.parallel import workflow_inputs

# Parse command-line arguments
args = workflow_inputs(*["myinput1", "myinput2"])

# Workflow
pcv.params.debug = args.debug

rgb_img, rgbpath, rgbname = pcv.readimage(filename=args.rgb)

nir_img, nirpath, nirname = pcv.readimage(filename=args.nir)

# ...
```
