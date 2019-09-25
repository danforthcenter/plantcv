FROM discoenv/jupyter-lab:beta

MAINTAINER PlantCV <ddpsc.plantcv@gmail.com>

USER root

RUN apt-get update \
    && apt-get install -y libx264-dev \
    && apt-get clean \
    && rm -rf /usr/lib/apt/lists/* \
    && fix-permissions $CONDA_DIR

USER jovyan

# install plantcv
RUN conda update -n base conda \
    && conda install jupyterlab=0.35.4 nb_conda \
    && conda create -n plantcv -c bioconda plantcv nb_conda \
    && conda clean -tipsy \
    && fix-permissions $CONDA_DIR

ENTRYPOINT ["jupyter"]
CMD ["lab", "--no-browser"]
