"""Find curvature measure of skeleton segments."""
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.morphology.segment_path_length import _segment_path_length
from plantcv.plantcv.morphology.segment_euclidean_length import _segment_euclidean_length


def _segment_curvature(morph, label=None):
    """Calculate segment curvature as defined by the ratio between geodesic and euclidean distance.
    Measurement of two-dimensional tortuosity.

    Inputs:
    morph = plantcv.plantcv.morphology.morph object,
        Morphology object to analyze
    label = str,
        Optional label parameter, modifies the variable name of
        observations recorded (default = pcv.params.sample_label).
    """
    objects = morph.leaves

    _segment_euclidean_length(morph, label="__seg_curvature_backend__")
    _segment_path_length(morph, label="__seg_curvature_backend__")
    eu_lengths = outputs.observations["__seg_curvature_backend__"]['segment_eu_length']['value']
    path_lengths = outputs.observations["__seg_curvature_backend__"]['segment_path_length']['value']
    outputs.observations.pop("__seg_curvature_backend__")

    curvature_measure = [float(x / y) for x, y in zip(path_lengths, eu_lengths)]

    segment_ids = list(range(len(objects)))

    outputs.add_observation(sample=label, variable='segment_curvature', trait='segment curvature',
                            method='plantcv.plantcv.analyze.morphology', scale='none', datatype=list,
                            value=curvature_measure, label=segment_ids)
