FROM ubuntu:16.04
MAINTAINER PlantCV <ddpsc.plantcv@gmail.com>

# Update package list and install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update && \
    apt-get -qq install -y --no-install-recommends build-essential ca-certificates libgtk2.0-0 sqlite3 wget && \
    apt-get -qq clean

# Install conda
RUN wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && rm /tmp/miniconda.sh

# Set PATH and PYTHONPATH environmental variables for conda
ENV PATH /opt/conda/bin:$PATH
ENV PYTHONPATH /opt/conda/lib/python2.7/site-packages:$PYTHONPATH

# Install Python and OpenCV with conda
RUN conda install --quiet --yes --channel menpo python=2.7 opencv=2.4.11

# Create a PlantCV working directory
RUN mkdir -p /tmp/plantcv
ADD . /tmp/plantcv
WORKDIR /tmp/plantcv

# Install PlantCV Python prerequisites and PlantCV
RUN pip install --quiet -r requirements.txt && python setup.py install
ADD plantcv-pipeline.py /usr/local/bin
ADD plantcv-train.py /usr/local/bin

# Create a directory to mount a host directory and remove PlantCV temp files
RUN mkdir -p /data && rm -fr /tmp/plantcv

# Set /home as the working directory
WORKDIR /home
