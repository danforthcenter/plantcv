FROM jupyter/minimal-notebook
MAINTAINER PlantCV <ddpsc.plantcv@gmail.com>

USER root

RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Install PlantCV
RUN conda install --quiet --yes -c conda-forge \
    "matplotlib>=1.5" \
    "numpy>=1.11" \
    pandas \
    python-dateutil \
    "scipy<1.3" \
    "scikit-image<0.15" \
    plotnine \
    "opencv<4,>=3.4" && \
    conda clean --all -f -y

# Copy source files
COPY . /tmp

# Install PlantCV Python prerequisites and PlantCV
RUN cd /tmp && python setup.py install

USER $NB_UID
