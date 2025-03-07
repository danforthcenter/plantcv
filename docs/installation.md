## Installing PlantCV

!!!note
    This guide describes typical installations of PlantCV.
    PlantCV can be installed from source for developers or users who want to test the latest features.
    Please see our [Contributing Guide](#CONTRIBUTING.md) for more information.

### Table of contents
1. [Supported platforms and dependencies](#dependencies)
2. [Desktop installation step-by-step guide](#desktop)
3. [Server/command-line step-by-step guide](#cli)
4. [Detailed installation instructions](#detailed)
    1. [Conda](#conda)
    2. [PyPI](#pypi)

### Supported platforms and dependencies <a name="dependencies"></a>
- Linux 64-bit, x86 processors
- macOS x86 (Intel) and M (ARM) processors
- Windows 64-bit, x86 processors

### Desktop installation step-by-step guide <a name="desktop"></a>

<iframe src="https://scribehow.com/embed/Install_PlantCV_via_Jupyter_Lab_Desktop__cS9d6VcxRcuDPGZxDfQycw" width="100%" height="640" allowfullscreen frameborder="0"></iframe>

### Server/command-line step-by-step guide <a name="cli"></a>

<iframe src="https://scribehow.com/embed/Installing_PlantCV__MacOSLinux__awAP9Xm2SgWV4SMZadm9CQ" width="640" height="640" allowfullscreen frameborder="0"></iframe>

### Detailed installation instructions <a name="detailed"></a>

PlantCV requires Python (tested with versions 3.9, 3.10, and 3.11) and these [Python packages](https://github.com/danforthcenter/plantcv/blob/main/pyproject.toml).
Additionally, we recommend installing [JupyterLab](https://jupyter.org/).

!!!note
    We recommend installing PlantCV in a virtual environment, which is a self-contained Python environment that includes
    PlantCV and its dependencies. Virtual environments are used to avoid conflicts between packages and can increase the
    reproducability of your work by isolating package versions for specific projects.

Stable releases of PlantCV are available through both the [Python Package Index (PyPI)](https://pypi.org/) and 
`conda` through the [conda-forge channel](https://conda-forge.org/).

#### Installing Conda <a name="conda"></a>
First install `conda` if you do not already have it. We strongly recommend using [Miniforge](https://conda-forge.org/download/).

If you are new to conda environments, check out this [Getting Started with Conda Guide](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).

!!! note 
    Additional instructions for Windows users:

    Windows users will need to install a Linux terminal to install and use PlantCV. We recommend using Anaconda Prompt
    which comes with Miniforge.
    
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
