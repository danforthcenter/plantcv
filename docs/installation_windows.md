## Installation

### Table of contents
1. [Supported platforms and dependencies](#dependencies)
2. [Install via a package manager](#install)
    1. [Conda](#conda)
    2. [PyPI](#pypi)
3. [Installing PlantCV for contributors](#contributors)


<iframe src="https://scribehow.com/page-embed/Installing_PlantCV__Windows__sZXdy8hTS7ariwVckTO2dA" width="640" height="640" allowfullscreen frameborder="0"></iframe>

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

#### Conda <a name="conda"></a>
First install `conda` if you do not already have it. We recommend using the [Miniconda](https://conda.io/miniconda.html),
but the full [Anaconda](https://www.anaconda.com/download/) distribution will also work.

```bash
conda create -n plantcv -c conda-forge plantcv

```

Or with optional (but recommended) dependencies:

```bash
conda create -n plantcv -c conda-forge plantcv jupyterlab ipympl nodejs

```

#### PyPI <a name="pypi"></a>

```bash
pip install plantcv

```

Or with optional (but recommended) dependencies:

```bash
pip install plantcv jupyterlab ipympl

```
