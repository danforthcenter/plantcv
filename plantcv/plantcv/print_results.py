# Print Numerical Data

from plantcv.plantcv import outputs


def print_results(filename):
    """Print result table

    Inputs:
    filename = filename

    :param filename: str
    :return:
    """
    result = open(filename, "a")
    if 'bound_horizontal' in outputs.measurements:
        bound_header = [
            'HEADER_BOUNDARY_H',
            'height_above_bound',
            'height_below_bound',
            'above_bound_area',
            'percent_above_bound_area',
            'below_bound_area',
            'percent_below_bound_area']
        bound_horizontal_dict = outputs.measurements['bound_horizontal']

        result.write('\t'.join(map(str, bound_header)) + '\n')
        result.write('BOUNDARY_H_DATA')

        for k, v in bound_horizontal_dict.items():
            result.write('\t' + str(v))
        result.write('\n')

    if 'bound_vertical' in outputs.measurements:
        bound_header = [
            'HEADER_BOUNDARY_V',
            'width_left_bound',
            'width_right_bound',
            'left_bound_area',
            'percent_left_bound_area',
            'right_bound_area',
            'percent_right_bound_area']
        bound_vertical_dict = outputs.measurements['bound_vertical']

        result.write('\t'.join(map(str, bound_header)) + '\n')
        result.write('BOUNDARY_V_DATA')

        for k, v in bound_vertical_dict.items():
            result.write('\t' + str(v))
        result.write('\n')

    if 'color_histogram' in outputs.measurements:
        hist_header = [
            'HEADER_COLOR_HISTOGRAM',
            'bin-number',
            'bin-values',
            'blue',
            'green',
            'red',
            'lightness',
            'green-magenta',
            'blue-yellow',
            'hue',
            'saturation',
            'value']
        color_dict = outputs.measurements['color_histogram']

        result.write('\t'.join(map(str, hist_header)) + '\n')
        result.write('COLOR_HISTOGRAM_DATA')

        for k, v in color_dict.items():
            result.write('\t' + str(v))
        result.write('\n')

    if 'nir_histogram' in outputs.measurements:
        nir_hist_header = [
            'HEADER_HISTOGRAM',
            'bin-number',
            'bin-values',
            'nir']
        nir_dict = outputs.measurements['nir_histogram']

        result.write('\t'.join(map(str, nir_hist_header)) + '\n')
        result.write('NIR_HISTOGRAM_DATA')

        for k, v in nir_dict.items():
            result.write('\t' + str(v))
        result.write('\n')

    if 'shapes' in outputs.measurements:
        shape_header = [
            'HEADER_SHAPES',
            'area',
            'hull-area',
            'solidity',
            'perimeter',
            'width',
            'height',
            'longest_axis',
            'center-of-mass-x',
            'center-of-mass-y',
            'hull_vertices',
            'in_bounds',
            'ellipse_center_x',
            'ellipse_center_y',
            'ellipse_major_axis',
            'ellipse_minor_axis',
            'ellipse_angle',
            'ellipse_eccentricity']
        shapes_dict = outputs.measurements['shapes']

        result.write('\t'.join(map(str, shape_header)) + '\n')
        result.write('SHAPES_DATA')

        for k, v in shapes_dict.items():
            result.write('\t' + str(v))
        result.write('\n')

    if 'fvfm' in outputs.measurements:
        fvfm_hist_header = [
            'HEADER_HISTOGRAM',
            'bin-number',
            'fvfm_bins',
            'fvfm_hist',
            'fvfm_hist_peak',
            'fvfm_median',
            'fdark_passed_qc']

        fvfm_dict = outputs.measurements['fvfm']

        result.write('\t'.join(map(str, fvfm_hist_header)) + '\n')
        result.write('FLU_DATA')

        for k, v in fvfm_dict.items():
            result.write('\t' + str(v))
        result.write('\n')

    if 'size_marker' in outputs.measurements:
        fmarker_header = [
        'HEADER_MARKER',
        'marker_area',
        'marker_major_axis_length',
        'marker_minor_axis_length',
        'marker_eccentricity']

        marker_dict = outputs.measurements['size_marker']

        result.write('\t'.join(map(str, fmarker_header)) + '\n')
        result.write('MARKER_DATA')

        for k, v in marker_dict.items():
            result.write('\t' + str(v))
        result.write('\n')

    if 'watershed' in outputs.measurements:
        watershed_header = [
            'HEADER_WATERSHED',
            'estimated_object_count']

        watershed_dict = outputs.measurements['watershed']

        result.write('\t'.join(map(str, watershed_header)) + '\n')
        result.write('WATERSHED_DATA')

        for k, v in watershed_dict.items():
            result.write('\t' + str(v))
        result.write('\n')

    result.close()
