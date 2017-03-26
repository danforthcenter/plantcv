## Installation

### Minimum requirements

We have tested PlantCV on the following systems:

- Linux: CentOS 7 x86 64-bit (RedHat Enterprise Linux)
- Mac OSX 10.11
- Windows 8.1 Professional

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

`sudo yum install opencv opencv-devel opencv-python`

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

#### Ubuntu Linux

We tested [Ubuntu](http://www.ubuntu.com/) x86 64-bit 14.04 server edition.  
After installation, connect to the server with SSH or a local terminal and execute the following commands 
to install PlantCV.

Install software dependencies

`sudo apt-get install git libopencv-dev python-opencv sqlite3`

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

#### Mac OSX

Tested on OSX 10.11.

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

Tested on Windows 8.1.

Procedure modified from [here](http://docs.opencv.org/master/d5/de5/tutorial_py_setup_in_windows.html#gsc.tab=0).

Install Python 2.7.9+ (tested with 2.7.11) from [here](https://www.python.org).
Python 2.7.9 and later comes with the setuptools package managers (pip and easy_install) by default.

Add setuptools to your Path. Open PowerShell and run:

`[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")`

Install additional packages:

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

Download [OpenCV](https://github.com/itseez/opencv/releases) (tested 2.4.13)

- Unzip the package (by default it will extract to `C:\Users\<username>\Downloads\opencv`
- Copy `opencv\build\python\2.7\x86\cv2.pyd` to `C:\Python27\Lib\site-packages`
- Open the Python IDLE GUI or the console on the command line and test opencv:

```python
import numpy
import matplotlib
import cv2
print(cv2.__verion__)
```

If this returns '2.4.13' (or your relevant version) without error then Python and OpenCV are working

Install the [GitHub desktop client](https://desktop.github.com) for Windows

Clone the PlantCV repository with the desktop application

Add PlantCV to the system PYTHONPATH using PowerShell

`[Environment]::SetEnvironmentVariable("PYTHONPATH", "$env:PYTHONPATH;C:\Users\<username>\Documents\GitHub\plantcv\lib\", "User")`

Test plantcv using the Python IDLE GUI

`import plantcv`

If this returns no errors, everything should be working.

Optionally, and at any time, check out a specific version or alternate branch of PlantCV

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
