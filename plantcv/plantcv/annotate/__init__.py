from plantcv.plantcv.annotate.detect_discs import detect_discs
from plantcv.plantcv.annotate.get_centroids import get_centroids
from plantcv.plantcv.annotate.classes import Points, ClickCount
from plantcv.plantcv.annotate.clickcount_correct import clickcount_correct
from plantcv.plantcv.annotate.clickcount_label import clickcount_label

# add new functions to end of lists
__all__ = ["detect_discs", "get_centroids", "Points", "ClickCount", "clickcount_correct", "clickcount_label"]
