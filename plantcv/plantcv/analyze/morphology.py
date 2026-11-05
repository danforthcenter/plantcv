
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.morphology.morph_class import morph
from plantcv.plantcv.morphology.analyze_stem import _analyze_stem
from plantcv.plantcv.morphology.segment_angle import _segment_angle
from plantcv.plantcv.morphology.segment_width import _segment_width
from plantcv.plantcv.morphology.fill_segments import _fill_segments
from plantcv.plantcv.morphology.segment_curvature import _segment_curvature
from plantcv.plantcv.morphology.segment_path_length import _segment_path_length
from plantcv.plantcv.morphology.segment_tangent_angle import _segment_tangent_angle
from plantcv.plantcv.morphology.segment_insertion_angle import _segment_insertion_length


def morphology(morph, size=20, stems=False, label=None):
    """Analyze morphology of a plant skeleton

    """
    if label is None:
        label = params.sample_label

    _segment_path_length(morph=morph, label=label)
    _segment_insertion_length(morph=morph, size=size, label=label)
    filled_segment_mask = _fill_segments(morph, stems=stems, label=label)
    _segment_width(morph, fill_segments, n_labels=len(np.unique(filled_segment_mask)) - 1, label=label)
    _segment_euclidean_length(morph, label=label)
    _segment_angle(morph, label=label)
    _analyze_stem(morph, label=label)
    _segment_curvature(morph, label=label)
    _segment_tangent_angle(morph=morph, size=size, label=label)

    # need to reconsider how to make a good debug image for this all.
    # will probably be pretty minimal? some of the helper functions could return points/annotations?
    # fill_segments with tip/branch points dotted would be pretty good?

    _debug(visual=filled_segment_mask
           filename=os.path.join(params.debug_outdir, str(params.device) + '_analyze_morphology.png'))

    # will return the debug image, per analyze.size
    return filled_segment_mask
