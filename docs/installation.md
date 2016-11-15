## Installation
<<<<<<< HEAD

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
    - setuptools
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

Clone the PlantCV repository

`git clone https://github.com/danforthcenter/plantcv.git`

Optionally, check out a specific version or alternate branch of PlantCV

```bash
# Switch to the development (latest) branch of PlantCV
cd plantcv

git checkout dev
```

Install PlantCV

`sudo python setup.py install`

Or to install to a local directory:

`python setup.py install --prefix /home/username`

If everything is working, the following should run without errors:

`python -c 'import plantcv'`

#### Ubuntu Linux

We tested [Ubuntu](http://www.ubuntu.com/) x86 64-bit 12.04.5 server edition.  
After installation, connect to the server with SSH or a local terminal and execute the following commands to install PlantCV.

Install software dependencies

`sudo apt-get install git libopencv-dev python-opencv python-numpy python-matplotlib sqlite3`

Clone the PlantCV repository into your home directory

`git clone https://github.com/danforthcenter/plantcv.git`

Optionally, check out a specific version or alternate branch of PlantCV

```bash
# Switch to the development (latest) branch of PlantCV
cd plantcv

git checkout dev
```

Install PlantCV

`sudo python setup.py install`

Or to install to a local directory:

`python setup.py install --prefix /home/username`

If everything is working, the following should run without errors:

`python -c 'import plantcv'`

#### Mac OSX

Tested on OSX 10.11.

Procedure modified from [here](https://jjyap.wordpress.com/2014/05/24/installing-opencv-2-4-9-on-mac-osx-with-python-support/).

Install Homebrew by following the instructions [here](http://brew.sh/).

Install OpenCV with Homebrew

```bash
brew tap homebrew/science

brew install opencv
```

Add OpenCV to your PYTHONPATH. Use your favorite editor to edit `~/.bash_profile` (or .bashrc or .profile) and add the following line:

`export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages`

Clone the PlantCV repository into your home directory

`git clone https://github.com/danforthcenter/plantcv.git`

Optionally, check out a specific version or alternate branch of PlantCV

```bash
# Switch to the development (latest) branch of PlantCV
cd plantcv

git checkout dev
```

Install PlantCV

`sudo python setup.py install`

Or to install to a local directory:

`python setup.py install --prefix /home/username`

If everything is working, the following should run without errors:

`python -c 'import plantcv'`

If everything is working, the following should run without errors:

`python -c 'import plantcv'`

#### Python virtual environment

Install OpenCV as documented for your system.

Create a Python virtual environment.

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

Switch to the development (latest) branch of PlantCV

`cd plantcv`

`git checkout dev`

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

Test import again and you should see no more errors. Restarting workspace will require input to remove libdc1394 error again.

`python -c 'import plantcv'`

=======
### Minimum requirements
We have tested PlantCV on CentOS 6 (RedHat Enterprise Linux) and Ubuntu 14 (Debian Linux), x86 64-bit versions only. A list of minimum tested software dependencies is listed below:

- GCC 4.4.x
- CMake 2.6
- GTK+2.x (with headers)
- pkg-config 0.23
- libjpeg (with headers)
- libpng (with headers)
- libtiff (with headers)
- libjasper (with headers)
- Python 2.6.x (with headers)
- Python Numpy 1.4.x
- Python Matplotlib 0.99.x
- Python Argparse 1.2.x
- Perl 5.10.x (with threading)
- PyGTK 2.x
- Perl DBI 1.6
- Perl DBD::SQLite 1.27
- Perl CPAN 1.9
- Perl Config::Tiny 2.x
- Perl Capture::Tiny 0.20
- SQLite3 3.6.x
- Git 1.7.x
- OpenCV 2.4.8

### Installation tutorials
The tutorials below require that you have administrator privileges. If you are not logged in as the root user you will need to execute the following commands with root athority by prepending all commands with the sudo command. If you do not have administrator privileges you will need to contact your system administrator.

#### RedHat Linux
We use [Centos](https://www.centos.org/) x86 64-bit minimal release 6.5 currently on our system. The minimal install is a bare-bones server installation with only necessary packages installed. More complete editions of CentOS, including those with a graphical user interface should work fine as well. After installation, connect to the server with SSH or a local terminal and execute the following commands to install PlantCV.

```bash
# Update the system
yum update

# Install developer tools (includes compilers and other tools)
yum groupinstall "Development tools"

# Install software dependencies
yum install cmake gtk2-devel libjpeg-devel libpng-devel libtiff-devel libjasper-devel tbb-devel opencv opencv-devel opencv-python python-devel numpy python-matplotlib pygtk2 perl-DBI perl-DBD-SQLite perl-CPAN

# Install additional Python packages
easy_install argparse

# Install additional Perl packages
# Note: if this is your first time using CPAN on your system you may be asked some initial setup questions
# Note: respond yes to all required dependencies
perl -MCPAN -e 'install Config::Tiny'
perl -MCPAN -e 'install Capture::Tiny'

# Install OpenCV
# Here we demonstrate using Git but you can alternatively download the package from SourceForge. This tutorial assumes you clone OpenCV to /home
git clone https://github.com/Itseez/opencv.git
cd opencv

# Checkout release 2.4.8 (highest version tested)
git checkout 2.4.8

# Compile OpenCV. Here we set the install directory to /home/lib/opencv. Either use the default install location (if you have administrator privileges) or install to a directory that is appropriate for your system
# Due to compile issues on CentOS we have disabled FFMPEG and OPENCL support
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/home/lib/opencv -D WITH_FFMPEG=OFF -D WITH_TBB=ON -D WITH_OPENCL=OFF -D WITH_1394=OFF /home/opencv/
make
make install

# Install PlantCV
# This tutorial assumes you clone PlantCV to /home
git clone https://github.com/danforthcenter/plantcv.git

# Edit your BASH profile to include the OpenCV and PlantCV libraries. Use your favorite editor to edit .bash_profile and add the following line:
export PYTHONPATH=$PYTHONPATH:$HOME/lib/opencv/lib/python2.6/site-packages:$HOME/plantcv/lib

# Reload your BASH profile
source .bash_profile
```

#### Ubuntu Linux
We tested [Ubuntu](http://www.ubuntu.com/) x86 64-bit server release 14.04 LTS. Other editions, including those with a graphical user interface should work fine as well. After installation, connect to the server with SSH or a local terminal and execute the following commands to install PlantCV.

```bash
# Update the system
apt-get update

# Install software dependencies
apt-get install build-essential unzip cmake libgtk2.0-dev python-dev python-numpy python-gtk2 python-matplotlib libavcodec-dev libavformat-dev libswscale-dev libdc1394-22 libjpeg-dev libpng-dev libjasper-dev libtiff-dev libtbb-dev sqlite3

# Install additional Perl packages
# Note: if this is your first time using CPAN on your system you may be asked some initial setup questions
perl -MCPAN -e 'install DBI'
perl -MCPAN -e 'install DBD::SQLite'
perl -MCPAN -e 'install Config::Tiny'
perl -MCPAN -e 'install Capture::Tiny'

# Install OpenCV
# Here we demonstrate using Git but you can alternatively download the package from SourceForge. This tutorial assumes you clone OpenCV to /home
git clone https://github.com/Itseez/opencv.git
cd opencv

# Checkout release 2.4.8 (highest version tested)
git checkout 2.4.8

# Compile OpenCV. Here we set the install directory to /home/lib/opencv. Either use the default install location (if you have administrator privileges) or install to a directory that is appropriate for your system
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/home/lib/opencv -D WITH_TBB=ON /home/opencv/
make
make install

# Install PlantCV
# This tutorial assumes you clone PlantCV to /home
git clone https://github.com/danforthcenter/plantcv.git

# Edit your BASH profile to include the OpenCV and PlantCV libraries. Use your favorite editor to edit .profile and add the following line:
export PYTHONPATH=$PYTHONPATH:$HOME/lib/opencv/lib/python2.7/dist-packages:$HOME/plantcv/lib

# Reload your BASH profile
source .profile
```
>>>>>>> master
