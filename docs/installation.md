## Installation

### Table of contents
1. [Supported platforms and dependencies](#dependencies)
2. [Install via a package manager](#install)
    1. [Conda](#conda)
    2. [PyPI](#pypi)
3. [Installing PlantCV for contributors](#contributors)

### Supported platforms and dependencies <a name="dependencies"></a>
- Linux 64-bit, x86 processors
- macOS x86 (Intel) and M (ARM) processors
- Windows 64-bit, x86 processors

PlantCV requires Python (tested with versions 3.8, 3.9, and 3.10) and these [Python packages](https://github.com/danforthcenter/plantcv/blob/main/requirements.txt).
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

### Installing PlantCV for contributors <a name="contributors"></a>
Before getting started, please read our [contributor guidelines](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md).

You can build PlantCV from the source code if you are a developer or want the absolute latest version available.
As noted above, we recommend installing PlantCV in a virtual environment. We will outline how to do this using `conda`.
You will also need a [GitHub](https://github.com) account. You will need to
[clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the PlantCV
repository from GitHub before getting started.

To set up your environment, follow these steps in your command-line terminal:

```bash
# Enter the PlantCV directory
cd plantcv

# Create a conda environment named "plantcv" (or whatever you like) and automatically install the developer dependencies
conda env create -n plantcv -f environment.yml

# Activate the plantcv environment (you will have to do this each time you start a new session)
conda activate plantcv

# Install PlantCV in editable mode so that it updates as you work on new features/updates
pip install -e .

```
