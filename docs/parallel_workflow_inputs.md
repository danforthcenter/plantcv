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
with the function `workflow_inputs`.

**plantcv.parallel.workflow_inputs**(*\*other_args*)

**returns** an argparse.Namespace object containing the inputs.

* **Parameters**:
  * \*other_args - (list, optional): list of additional user-defined workflow inputs.
* **Context**:
    * Used to parse command-line inputs to the workflow. Inputs are constructed by `plantcv-run-workflow`.
* **Example use**:
    * [Converting from Jupyter to Python](jupyter.md)

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
