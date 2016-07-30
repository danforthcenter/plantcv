## Installation

### Minimum requirements

We have tested PlantCV on the following systems:

- Linux: CentOS 7 x86 64-bit (RedHat Enterprise Linux)
- Mac OSX 10.11
- Windows 8.1 Professional

A list of minimum tested software dependencies is listed below:

- Python 2.7.x
    - argparse 1.1.x
    - dateutil 1.5
    - matplotlib 1.2.x
    - numpy 1.7.x
    - cv2 2.4.x
- OpenCV 2.4.x
- SQLite 3.7.x
- Git 1.8.x

### Installation tutorials

The tutorials below require that you have administrator privileges. 
If you are not logged in as the root user you will need to execute the following commands with root authority by prepending all commands with the sudo command. 
If you do not have administrator privileges you will need to contact your system administrator.

#### RedHat Linux

We use [Centos](https://www.centos.org/) x86 64-bit minimal release 7.2 currently on our system. 
The minimal install is a bare-bones server installation with only necessary packages installed. 
More complete editions of CentOS, including those with a graphical user interface should work fine as well. 
After installation, connect to the server with SSH or a local terminal and execute the following commands to install PlantCV.

Install the developer tools (includes compilers and other tools)

`sudo yum groupinstall "Development tools"`

Install additional software dependencies

`sudo yum install opencv opencv-devel opencv-python numpy python-matplotlib`

Clone the PlantCV repository into your home directory

`git clone https://github.com/danforthcenter/plantcv.git`

Edit your BASH profile to include the PlantCV library. Use your favorite editor to edit `~/.bash_profile` (or .bashrc or .profile) and add the following line:

`export PYTHONPATH=$PYTHONPATH:$HOME/plantcv/lib`

Restart your session or resource your profile. If everything is working, the following should run without errors:

`python -c 'import plantcv'`

Optionally, and at any time, check out a specific version or alternate branch of PlantCV

```bash
# Switch to the development (latest) branch of PlantCV
cd plantcv

git checkout dev
```

#### Ubuntu Linux

We tested [Ubuntu](http://www.ubuntu.com/) x86 64-bit 12.04.5 server edition.  
After installation, connect to the server with SSH or a local terminal and execute the following commands to install PlantCV.

Install software dependencies

`sudo apt-get install git libopencv-dev python-opencv python-numpy python-matplotlib sqlite3`

Clone the PlantCV repository into your home directory

`git clone https://github.com/danforthcenter/plantcv.git`

Edit your BASH profile to include the PlantCV library. Use your favorite editor to edit `~/.profile` (or .bashrc or .bash_profile) and add the following line:

`export PYTHONPATH=$PYTHONPATH:$HOME/plantcv/lib`

Restart your session or resource your profile. If everything is working, the following should run without errors:

`python -c 'import plantcv'`

Optionally, and at any time, check out a specific version or alternate branch of PlantCV

```bash
# Switch to the development (latest) branch of PlantCV
cd plantcv

git checkout dev
```

#### Mac OSX

Tested on OSX 10.11.

Procedure modified from [here](https://jjyap.wordpress.com/2014/05/24/installing-opencv-2-4-9-on-mac-osx-with-python-support/).

Install Homebrew by following the instructions [here](http://brew.sh/).

Install OpenCV with Homebrew

```bash
brew tap homebrew/science

brew install opencv
```

Clone the PlantCV repository into your home directory

`git clone https://github.com/danforthcenter/plantcv.git`

Add OpenCV and PlantCV to your PYTHONPATH. Use your favorite editor to edit `~/.bash_profile` (or .bashrc or .profile) and add the following line:

`export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages:$HOME/plantcv/lib`

Restart your session or resource your profile. If everything is working, the following should run without errors:

`python -c 'import plantcv'`

Optionally, and at any time, check out a specific version or alternate branch of PlantCV

```bash
# Switch to the development (latest) branch of PlantCV
cd plantcv

git checkout dev
```

#### Windows

Tested on Windows 8.1.

Procedure modified from [here](http://docs.opencv.org/master/d5/de5/tutorial_py_setup_in_windows.html#gsc.tab=0).

Install Python 2.7.9+ (tested with 2.7.11) from [here](https://www.python.org).
Python 2.7.9 and later comes with the setuptools package managers (pip and easy_install) by default.

Add setuptools to your Path. Open PowerShell and run:

`[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")`

Install additional packages (need numpy >= 1.9, tested 1.11)

```bash
pip install numpy
pip install matplotlib
pip install argparse
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