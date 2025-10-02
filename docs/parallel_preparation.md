## Why Parallelize?

PlantCV's Parallel module allows for running a PlantCV workflow on many images across many cores. If you have a high throughput image phenotyping facility or other hardware allowing you to take many photos then working one photo at a time through a Jupyter notebook may be prohibitively slow and would not leverage the benefits of PlantCV over non-scripting image analysis tools.

## Getting ready to parallelize

Before you can parallelize a workflow you need to make sure that it works on a single image. Generally we recommend prototyping a workflow in Jupyter notebooks so that you can run interactively. Most of the time a previous workflow of yours or one of our many [tutorials](https://plantcv.org/tutorials) will be a good place to start. Once your Jupyter notebook works on one image try it on a few more to make sure you've caught any obvious errors that could come up.

Running a parallel workflow will make some temporary files located wherever you are running the workflow in a directory called `checkpoint`, with nested directories named by timestamp. Normally you do not need to interact with those, but be aware that if you have a folder called "checkpoint" with `json` files in it that you may have unexpected problems if `checkpoint=True` in your configuration. By default the `cleanup=true` field of the parallel configuration will remove the `checkpoint` directory at the end of a successful parallel workflow.

### From Jupyter to Parallel

There are a few things to consider moving from prototyping in Jupyter to running a potentially computationally heavy parallel job.

Another helpful tool for building a workflow with the goal of running analyses in parallel is to use [`workflow_inputs`](parallel_workflow_inputs.md) to set things like file paths. There are many examples of this in the tutorials, but the general pattern working interactively in Jupyter would be:

```python
# in your .ipynb notebook
from plantcv import parallel as pcvpar
args = pcvpar.WorkflowInputs(
    images=["path/to/your/image.file"],
    names="image1",
    result="example_results.json",
    outdir=".",
    debug="plot"
    )
# using the args object to set preferences will make parallelization easier later
pcv.params.debug = args.debug
img, path, filename = pcv.readimage(filename=args.image1)
# ... the rest of your code
```
When you are ready to run in parallel whether you make a python script manually and run with [`WorkflowConfig`](parallel_config.md) or if you run the Jupyter notebook in parallel with [`jupyterconfig`](parallel_jupyterconfig.md) you would need to change the above to:

```python
# in your .py script
from plantcv import parallel as pcvpar
args = pcvpar.workflow_inputs()
# these lines can stay the same thanks to workflow_inputs()
pcv.params.debug = args.debug
img, path, filename = pcv.readimage(filename=args.image1)
# ... the rest of your code
```

This change will allow the workflow to read the variety of image paths and associated metadata that are used when running in parallel.

It is also a good idea to avoid making your code do extra work in parallel. Things like plotting debug images or saving intermediate data can be helpful in development but problematic in parallel. We recommend setting `plantcv.params.debug = None` when working in parallel and commenting out any code that explicitly draws plots/images. If you use `WorkflowInputs` in your Jupyter notebook then when you switch to `workflow_inputs` for use in parallel `args.debug` will default to `None`.

Finally, for converting from a `.ipynb` notebook to a `.py` script you can copy and paste from cells or use [`nbconvert`](https://nbconvert.readthedocs.io/en/latest/).

## Where to Parallelize

PlantCV Parallel uses `dask` to schedule jobs. By default all jobs are run on the machine where they are submitted (`config.cluster = "LocalCluster"`). That will run `config.cluster_config.n_workers` cores on the local machine. You can also distribute jobs across many machines if you have a computational cluster available to use, see the [`WorkflowConfig` docs](parallel_config.md) for details.
