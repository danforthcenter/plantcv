import os
import matplotlib
# If there is no display or a matplotlib backend already defined, use the non-GUI backend
if "DISPLAY" not in os.environ or "MPLBACKEND" not in os.environ:
    matplotlib.use("Agg")

from plantcv.learn.naive_bayes import naive_bayes
from plantcv.learn.naive_bayes import naive_bayes_multiclass
from plantcv.learn.train_kmeans import train_kmeans
from plantcv.learn.train_kmeans import patch_extract

__all__ = ["naive_bayes", "naive_bayes_multiclass", "train_kmeans", "patch_extract"]
