## Installation

### Minimum requirements

PlantCV has been tested on the following systems:

- Linux: CentOS 7 (RedHat Enterprise Linux)
- Linux: Ubuntu 12.04+
- Linux: Raspbian "Jessie"
- Mac OSX 10.11 and macOS 10.12+
- Windows 10
- Cloud9 IDE

#### Required dependencies

- Python (tested with versions 3.6, 3.7, and 3.8)
    - cv2 (a.k.a. OpenCV or opencv-python on PyPI; requires at least 3.4 and <4)
    - dask
    - dask-jobqueue 
    - matplotlib
    - numpy
    - pandas
    - plotnine
    - python-dateutil
    - scikit-image
    - scikit-learn
    - scipy

#### Optional but recommended

- conda (Anaconda or Miniconda)
- jupyter
- pytest (only if installing from source code and running tests)

### Install via a package manager

Stable releases of PlantCV are available through both the [Python Package Index (PyPI)](https://pypi.org/) and 
`conda` through the [conda-forge channel](https://conda-forge.org/). We plan on releasing new versions of PlantCV 
into both platforms on at a monthly basis.

#### PyPI

To install from PyPI run the following in any type of virtual environment, as an administrator, or add the `--user` 
flag if needed.

```bash
pip install plantcv

```

#### Conda

To install using `conda` first install [Anaconda](https://www.anaconda.com/download/) or 
[Miniconda](https://conda.io/miniconda.html) if you have not already. If needed, add the following channels to your
`conda` configuration.

```bash
conda config --add channels conda-forge

```

Then create an environment and install PlantCV.

```bash
conda create -n plantcv plantcv

```

Or install PlantCV in your current environment.

```bash
conda install plantcv

```

#### Using PlantCV containers

**Platforms**: Linux, macOS, Windows

PlantCV currently supports the Docker container system but support for Singularity and other container systems are on
our to-do list. [Docker](https://www.docker.com/) is a company/platform that provides operating-system-level
virtualization (containers). See [Wikipedia](https://en.wikipedia.org/wiki/Operating-system-level_virtualization) for 
more background. Containers are a useful way to package and isolate applications (and their dependencies) into a 
portable, lightweight virtualized environment. A PlantCV Docker container is available through 
[Docker Hub](https://hub.docker.com/r/danforthcenter/plantcv/). To use the PlantCV container you will need docker
[installed on your local system](https://docs.docker.com/engine/installation/). If you have docker, you can use PlantCV
as in the following examples:

```bash
# Pull the latest image of PlantCV from Docker Hub
docker pull danforthcenter/plantcv

# A simple command to demonstrate it works (nothing returned if import is successful)
docker run danforthcenter/plantcv python -c 'from plantcv import plantcv as pcv; print(pcv.__version__)'

```

The PlantCV container is built on top of the 
[Jupyter minimal-notebook container](https://hub.docker.com/r/jupyter/minimal-notebook). To analyze data with the 
PlantCV Docker container you will need to map a local folder that contains your inputs into
the container filesystem. We use the same working directory as documented by 
[Jupyter Docker Stacks](https://github.com/jupyter/docker-stacks). An easy way to run PlantCV in a container with
Jupyter notebook support is to map your current directory into the container:

```bash
docker run --rm -p 8888:8888 -v "$PWD":/home/jovyan/work danforthcenter/plantcv

```

Then point your browser to the URL that is printed to your terminal. Any data/notebooks saved to the `work` directory
will persist on your local filesystem after the container is shut down.

You can also run PlantCV on the command-line without Jupyter notebooks. For the sake of this example, assume that 
your working directory contains a PlantCV script called `test-script.py` and an image called `test-image.png`. 
The `test-script.py` in this case would be a script like the one described in the [VIS tutorial](tutorials/vis_tutorial.md).

```bash
# Analyzing data using the PlantCV docker image
docker run --rm -v "$PWD":/home/jovyan/work danforthcenter/plantcv python ./work/test-script.py \
-i ./work/test-image.png -o ./work -r ./work/plantcv-results.txt

```

### Installation from the source code

You can build PlantCV from the source on GitHub if you are a developer or want the absolute latest version available.

#### Conda-based installation procedure

**Platforms**: Linux, macOS, Windows

There are a variety of options for installing PlantCV depending on your use case. If you have experience with system
administration you can install PlantCV and the dependencies using system package management tools and administrator
privileges (feel free to [ask](https://github.com/danforthcenter/plantcv/issues) if you get stuck).

For most users we recommend installation using `conda`, a cross-platform package management system. Both the 
[Anaconda](https://www.anaconda.com/download/) or [Miniconda](https://conda.io/miniconda.html) implementations of 
`conda` can be used. Here is an overview of the process:

1. Download and install the version of `conda` that is appropriate for your system. 
2. Clone or download PlantCV from GitHub. Feel free to use [GitHub Desktop](https://desktop.github.com/) or 
command-line `git`. Git will allow you to pull updates from GitHub, but if you prefer not to use git you can download
a zip file of the package from [GitHub](https://github.com/danforthcenter/plantcv).
3. Create a Python environment for PlantCV that includes the Python dependencies.
4. Install PlantCV.

Once you have `conda` and `git` or GitHub Desktop installed, clone the PlantCV repository, open a command-line terminal 
application (on Windows there are other options but for this tutorial we will use the Anaconda Prompt application). In
the example below we use an environment configuration file that is included with PlantCV.

```bash
# Clone PlantCV if you did not use the GitHub Desktop application
git clone https://github.com/danforthcenter/plantcv.git

# Enter the PlantCV directory (if you cloned with GitHub Desktop your path may be different than below)
cd plantcv

# Create a conda environment named "plantcv" (or whatever you like) and automatically install the dependencies
conda env create -n plantcv -f environment.yml

# Activate the plantcv environment (you will have to do this each time you start a new session)
conda activate plantcv

# Install PlantCV in editable mode so that it updates as you work on new features/updates
pip install -e .

```

If you have a broken environment, you can remove it and repeat the above steps.

```bash
# Remove the environment 
conda env remove -n plantcv

```

#### Script-based installation

**Platforms**: Ubuntu, macOS

Clone the PlantCV repository:

```bash
git clone https://github.com/danforthcenter/plantcv.git
```

Run the setup script:

```bash
cd plantcv
bash scripts/setup.sh

```

The script guides you through the installation steps. Successful completion ends with a usage report.

The script has been tested on [Ubuntu](http://www.ubuntu.com/) x86_64-bit 16_04 server edition, OSX 10.11, and
macOS 10.12.

### Installation on other systems

#### Cloud9 IDE

[Cloud9](https://c9.io) is a development environment in the cloud that works with Chromebooks or other thin clients.
The IDE workspaces are powered by Docker Ubuntu containers within a web browser.

After signing up for an account create a new workspace and choose a Python template.

Install update

```bash
sudo apt-get update
```

Install software dependencies

```bash
sudo apt-get install git libopencv-dev python-opencv python-numpy python-matplotlib sqlite3
```

Clone the PlantCV repository into your home directory

```bash
git clone https://github.com/danforthcenter/plantcv.git
```

The default branch (master) is the latest release. If you want to check out a specific version:

```bash
# Switch to a stable release
cd plantcv

git checkout v1.1
```

Install PlantCV

```bash
sudo python setup.py install
```

After installation test with the following:

```bash
python -c 'import plantcv'
```

You will be given the following error:

`libdc1394 error: Failed to initialize libdc1394`

libdc1394 allows a program to interface with cameras that work on the ieee1394 standard(firewire).
Due to no option to enable USB access in the Cloud9 workspace this error will keep occuring when running a workflow.
This error will have no effect on the output of your workflows and can continue working despite the warning.

To temporarily remove the driver and error use:

```bash
sudo ln /dev/null /dev/raw1394
```

Test import again and you should see no more errors. Restarting workspace will require input to remove 
libdc1394 error again.

```bash
python -c 'import plantcv'
```
