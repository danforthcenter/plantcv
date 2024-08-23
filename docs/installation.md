## Installing PlantCV on Mac and Linux

### Table of contents
1. [Step-by-step installation guide](#guide)
2. [Supported platforms and dependencies](#dependencies)
3. [Install via a package manager](#install)
    1. [Conda](#conda)
    2. [PyPI](#pypi)
4. [Installing PlantCV for contributors](#contributors)

### Step-by-step installation guide <a name="guide"></a>

<iframe src="https://scribehow.com/embed/Installing_PlantCV__MacOSLinux__awAP9Xm2SgWV4SMZadm9CQ" width="640" height="640" allowfullscreen frameborder="0"></iframe>


### Supported platforms and dependencies <a name="dependencies"></a>
- Linux 64-bit, x86 processors
- macOS x86 (Intel) and M (ARM) processors
- Windows 64-bit, x86 processors

PlantCV requires Python (tested with versions 3.9, 3.10, and 3.11) and these [Python packages](https://github.com/danforthcenter/plantcv/blob/main/pyproject.toml).
Additionally, we recommend installing [JupyterLab](https://jupyter.org/).

### Install via a package manager <a name="install"></a>

!!!note
    We recommend installing PlantCV in a virtual environment, which is a self-contained Python environment that includes
    PlantCV and its dependencies. Virtual environments are used to avoid conflicts between packages and can increase the
    reproducability of your work by isolating package versions for specific projects.

Stable releases of PlantCV are available through both the [Python Package Index (PyPI)](https://pypi.org/) and 
`conda` through the [conda-forge channel](https://conda-forge.org/).

#### Installing Conda <a name="conda"></a>
First install `conda` if you do not already have it. We recommend using the [Miniconda](https://conda.io/miniconda.html),
but the full [Anaconda](https://www.anaconda.com/download/) distribution will also work.

If you are new to conda environments, check out this [Getting Started with Conda Guide](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).

!!! note 
    Additional instructions for Windows users:

    Windows users will need to install a Linux terminal to install and use PlantCV. We recommend using Anaconda Prompt which comes with Anaconda and Miniconda. 
    
    Alternatively, Windows users can download [Git for Windows](https://gitforwindows.org/). This option requires users to add conda to their `.bashrc` file. See this helpful [guide](https://discuss.codecademy.com/t/setting-up-conda-in-git-bash/534473) for setting up conda in Git Bash. 

#### Installing PlantCV with conda

Open Terminal (Mac) or Anaconda Prompt (Windows) and run the following:

```bash
conda create -n plantcv -c conda-forge plantcv

```

Or with optional (but recommended) dependencies:

```bash
conda create -n plantcv -c conda-forge plantcv jupyterlab ipympl nodejs

```


#### PyPI <a name="pypi"></a>
Optionally, PlantCV can be installed from PyPi.

```bash
pip install plantcv

```

Or with optional (but recommended) dependencies:

```bash
pip install plantcv jupyterlab ipympl

```
