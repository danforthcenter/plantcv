# Print Numerical Data

from plantcv.plantcv import outputs


def print_results(filename, args):
    """Print result table

    Inputs:
    filename = filename
    args =

    :param filename: str
    :param header: list
    :param data: list
    :return:
    """
    result = open(args.result, "a")
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
