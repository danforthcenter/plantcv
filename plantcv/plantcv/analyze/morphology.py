import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params
from plantcv.plantcv.morphology.morph_class import morph
from plantcv.plantcv.morphology.analyze_stem import _analyze_stem
from plantcv.plantcv.morphology.segment_angle import _segment_angle
from plantcv.plantcv.morphology.segment_width import _segment_width
from plantcv.plantcv.morphology.fill_segments import _fill_segments
from plantcv.plantcv.visualize.colorize_label_img import colorize_label_img
from plantcv.plantcv.morphology.segment_curvature import _segment_curvature
from plantcv.plantcv.morphology.segment_path_length import _segment_path_length
from plantcv.plantcv.morphology.segment_tangent_angle import _segment_tangent_angle
from plantcv.plantcv.morphology.segment_insertion_angle import _segment_insertion_angle
from plantcv.plantcv.morphology.segment_euclidean_length import _segment_euclidean_length


def morphology(morph_obj, size=20, stems=False, label=None):
    """Analyze morphology of a plant skeleton

    Parameters
    ----------
    morph : plantcv.plantcv.morphology.morph,
        morphology object to analyze
    size : int
        Size of ends used to calculate angles and tangent lines.
    stems : boolean,
        should stems be included in filling segments? Defaults to False.
    label : str, optional
        Label parameter, modifies the variable name of observations recorded (default = pcv.params.sample_label).

    Returns
    -------
    labeled_img : numpy.ndarray
        Segmented debugging image with angles labeled.

    """
    if label is None:
        label = params.sample_label

    _segment_path_length(morph=morph_obj, label=label)
    _segment_insertion_angle(morph=morph_obj, size=size, label=label)
    filled_segment_mask = _fill_segments(morph_obj, stems=stems, label=label)
    _segment_width(morph_obj, filled_segment_mask, n_labels=len(np.unique(filled_segment_mask)) - 1, label=label)
    _segment_euclidean_length(morph_obj, label=label)
    _segment_angle(morph_obj, label=label)
    _analyze_stem(morph_obj, label=label)
    _segment_curvature(morph_obj, label=label)
    _segment_tangent_angle(morph=morph_obj, size=size, label=label)

    # need to reconsider how to make a good debug image for this all.
    # will probably be pretty minimal? some of the helper functions could return points/annotations?
    # fill_segments with tip/branch points dotted would be pretty good?
    debug = params.debug
    params.debug = None
    filled_img = colorize_label_img(filled_segment_mask)
    params.debug = debug

    _debug(visual=filled_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_analyze_morphology.png'))

    # will return the debug image, per analyze.size
    return filled_segment_mask
