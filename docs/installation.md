## Installation

### Minimum requirements

We have tested PlantCV on the following systems:

- Linux: CentOS 7 x86 64-bit (RedHat Enterprise Linux)
- Linux: Ubuntu 12.04, 14.04, and 16.04
- Mac OSX 10.11
- Windows 10

A list of minimum tested software dependencies is listed below:

- Python 2.7
    - argparse 1.1
    - cv2 2.4
    - matplotlib 1.5
    - numpy 1.11
    - pandas 0.18
    - pytest 2.9
    - python-dateutil 2.6
    - scikit-image 0.12
    - scipy 0.18
    - setuptools 28.6
- OpenCV 2.4
- SQLite 3.7
- Git 1.8

### Installation tutorials

The tutorials below require that you have administrator privileges.
If you are not logged in as the root user you will need to execute the following commands with root authority by 
prepending all commands with the sudo command.
If you do not have administrator privileges you will need to contact your system administrator or manually install
the dependencies into your user directory.

#### RedHat Linux

We use [Centos](https://www.centos.org/) x86 64-bit minimal release 7.3 currently on our system. 
The minimal install is a bare-bones server installation with only necessary packages installed. 
More complete editions of CentOS, including those with a graphical user interface should work fine as well. 
After installation, connect to the server with SSH or a local terminal and execute the following commands 
to install PlantCV.

Install the developer tools (includes compilers and other tools)

`sudo yum groupinstall "Development tools"`

Install additional software dependencies

`sudo yum install opencv opencv-devel opencv-python python-setuptools`

Clone the PlantCV repository

`git clone https://github.com/danforthcenter/plantcv.git`

The default branch (master) is the latest release. If you want to check out a specific version:

```bash
# Switch to a stable release
cd plantcv

git checkout v1.1
```

Install PlantCV

`sudo python setup.py install`

Or to install to a local directory:

`python setup.py install --prefix /home/username`

If everything is working, the following should run without errors:

`python -c 'import plantcv'`

Or for more extensive tests:

```
cd plantcv
py.test -v tests/tests.py
```

#### Ubuntu Linux

##### Script-based installation

Clone the PlantCV repository:

    git clone https://github.com/danforthcenter/plantcv.git

Note that the following may not be merged in the main repository at this time. The fallback may be [this fork](https://github.com/ic/plantcv.git).

Run the setup script:

```bash
cd plantcv
bash scripts/setup.sh
```

The script guides you through the installation steps. Successful completion ends with a usage report.

The script has been tested on [Ubuntu](http://www.ubuntu.com/) x86_64-bit 16_04 server edition.  

##### Manual

We tested [Ubuntu](http://www.ubuntu.com/) x86 64-bit 14.04 server edition.  
After installation, connect to the server with SSH or a local terminal and execute the following commands 
to install PlantCV.

Install software dependencies

`sudo apt-get install git libopencv-dev python-opencv sqlite3 python-setuptools libpython2.7-dev python-pip`

Add the OpenCV distribution for Python to find it:

`export PYTHONPATH=/usr/lib/python2.7/dist-packages`

Clone the PlantCV repository into your home directory

`git clone https://github.com/danforthcenter/plantcv.git`

Install the minimum dependencies:

`pip install -r requirements.txt`

The default branch (master) is the latest release. If you want to check out a specific version:

```bash
# Switch to a stable release
cd plantcv

git checkout v1.1
```

Install PlantCV

`sudo python setup.py install`

Or to install to a local directory:

`python setup.py install --prefix /home/username`

If everything is working, the following should run without errors:

`python -c 'import plantcv'`

Or for more extensive tests:

```
cd plantcv
py.test -v tests/tests.py
```

#### Mac OSX

Tested on OSX 10.11.

##### With MacPorts

Clone the PlantCV repository:

    git clone https://github.com/danforthcenter/plantcv.git

Note that the following may not be merged in the main repository at this time. The fallback may be [this fork](https://github.com/ic/plantcv.git).

Run the setup script:

```bash
cd plantcv
bash scripts/setup.sh
```

The script should guide you through the installation steps. Successful completion ends with a usage report.

##### With Brew

Procedure modified from 
[here](https://jjyap.wordpress.com/2014/05/24/installing-opencv-2-4-9-on-mac-osx-with-python-support/).

Install Homebrew by following the instructions [here](http://brew.sh/).

Install OpenCV with Homebrew

```bash
brew tap homebrew/science

brew install opencv
```

Add OpenCV to your PYTHONPATH. Use your favorite editor to edit `~/.bash_profile` (or .bashrc or .profile) and 
add the following line:

`export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages`

Clone the PlantCV repository into your home directory

`git clone https://github.com/danforthcenter/plantcv.git`

The default branch (master) is the latest release. If you want to check out a specific version:

```bash
# Switch to a stable release
cd plantcv

git checkout v1.1
```

Install PlantCV

`sudo python setup.py install`

Or to install to a local directory:

`python setup.py install --prefix /home/username`

If everything is working, the following should run without errors:

`python -c 'import plantcv'`

Or for more extensive tests:

```
cd plantcv
py.test -v tests/tests.py
```

#### Python virtual environment

Install OpenCV as documented for your system.

Create a Python virtual environment (assumes OpenCV is already installed in the system).

```bash
virtualenv plantcv-venv --system-site-packages
```

Install PlantCV into the virtual environment.

```bash
cd plantcv-venv

# Activate the virtual environment
source bin/activate

# Clone PlantCV
git clone https://github.com/danforthcenter/plantcv.git

# Install PlantCV
cd plantcv
python setup.py install
```

#### Windows

Tested on Windows 10.

The easiest way to get PlantCV working on Windows is to use Anaconda. An alternate approach might be to use the new
Linux subsystem for Windows, but we have not tested that yet.

Install Anaconda (tested with 4.3.1) from [here](https://www.continuum.io/downloads#windows). Download and install
the Python 2.7 version that is appropriate for your system (we used the 64-bit installer).

Run the Anaconda Prompt application and update Anaconda:

```
conda update -q conda
```

Install prerequisite Python packages (most are already installed by default):

```
pip install argparse
pip install matplotlib
pip install numpy
pip install pandas
pip install pytest
pip install python-dateutil
pip install scikit-image
pip install scipy
```

Use Anaconda to install OpenCV and SQLite3:

```
conda install -c menpo opencv=2.4.11
conda install -c blaze sqlite3
```

Clone the PlantCV repository and install it in the Anaconda environment:

```
git clone https://github.com/danforthcenter/plantcv.git
cd plantcv
python setup.py install
```

If everything is working, the following should run without errors:

`python -c 'import plantcv'`

Or for more extensive tests:

```
cd plantcv
py.test -v tests/tests.py
```

#### Cloud9 IDE

[Cloud9](https://c9.io) is a development environment in the cloud that works with Chromebooks or other thin clients.
The IDE workspaces are powered by Docker Ubuntu containers within a web browser.

After signing up for an account create a new workspace and choose a Python template.

Install update

`sudo apt-get update`

Install software dependencies

`sudo apt-get install git libopencv-dev python-opencv python-numpy python-matplotlib sqlite3`

Clone the PlantCV repository into your home directory

`git clone https://github.com/danforthcenter/plantcv.git`

The default branch (master) is the latest release. If you want to check out a specific version:

```bash
# Switch to a stable release
cd plantcv

git checkout v1.1
```

Install PlantCV

`sudo python setup.py install`

After installation test with the following:

`python -c 'import plantcv'`

You will be given the following error:

`libdc1394 error: Failed to initialize libdc1394`

libdc1394 allows a program to interface with cameras that work on the ieee1394 standard(firewire).
Due to no option to enable USB access in the Cloud9 workspace this error will keep occuring when running a pipeline.
This error will have no effect on the output of your pipelines and can continue working despite the warning.

To temporarily remove the driver and error use:

`sudo ln /dev/null /dev/raw1394`

Test import again and you should see no more errors. Restarting workspace will require input to remove 
libdc1394 error again.

`python -c 'import plantcv'`
