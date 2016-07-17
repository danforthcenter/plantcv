## Installation
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
