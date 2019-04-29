# Print Numerical Data

from plantcv.plantcv import outputs


def print_results(filename):
    """Print result table

    Inputs:
    filename = filename

    :param filename: str
    :return:
    """
    # Open a new text file
    result = open(filename, "a")

    # Write data from analyze_bound_horizontal if it was stored
    if 'bound_horizontal' in outputs.measurements:
        header = ['HEADER_BOUNDARY_H']
        data = ['BOUNDARY_DATA']
        for k, v in outputs.measurements['bound_horizontal'].items():
            header.append(k)
            data.append(v)
        result.write('\t'.join(map(str, header)) + '\n')
        result.write('\t'.join(map(str, data)) + '\n')

    # Write data from analyze_bound_vertical if it was stored
    if 'bound_vertical' in outputs.measurements:
        header = ['HEADER_BOUNDARY_V']
        data = ['BOUNDARY_DATA']
        for k, v in outputs.measurements['bound_vertical'].items():
            header.append(k)
            data.append(v)
        result.write('\t'.join(map(str, header)) + '\n')
        result.write('\t'.join(map(str, data)) + '\n')

    # Write data from analyze_color if it was stored
    if 'color_data' in outputs.measurements:
        if 'color_features' in outputs.measurements['color_data']:
            header = ['HEADER_COLOR_FEATURES']
            data = ['COLOR_FEATURES_DATA']
            for k, v in outputs.measurements['color_data']['color_features'].items():
                header.append(k)
                data.append(v)
            result.write('\t'.join(map(str, header)) + '\n')
            result.write('\t'.join(map(str, data)) + '\n')
        if 'histograms' in outputs.measurements['color_data']:
            for channel in outputs.measurements['color_data']['histograms']:
                header = ['HEADER_HISTOGRAM', 'channel_name']
                data = ['HISTOGRAM_DATA', channel]
                for k, v in outputs.measurements['color_data']['histograms'][channel].items():
                    header.append(k)
                    data.append(v)
                result.write('\t'.join(map(str, header)) + '\n')
                result.write('\t'.join(map(str, data)) + '\n')

    # Write data from analyze_nir_intensity if it was stored
    if 'nir_histogram' in outputs.measurements:
        header = ['HEADER_HISTOGRAM', 'channel_name']
        data = ['HISTOGRAM_DATA', 'nir']
        for k, v in outputs.measurements['nir_histogram'].items():
            header.append(k)
            data.append(v)
        result.write('\t'.join(map(str, header)) + '\n')
        result.write('\t'.join(map(str, data)) + '\n')

    # Write data from analyze_object if it was stored
    if 'shapes' in outputs.measurements:
        header = ['HEADER_SHAPES']
        data = ['SHAPES_DATA']
        for k, v in outputs.measurements['shapes'].items():
            header.append(k)
            data.append(v)
        result.write('\t'.join(map(str, header)) + '\n')
        result.write('\t'.join(map(str, data)) + '\n')

    # Write data from fluor_fvfm if it was stored
    if 'fvfm' in outputs.measurements:
        header = ['HEADER_HISTOGRAM']
        data = ['HISTOGRAM_DATA']
        for k, v in outputs.measurements['fvfm'].items():
            header.append(k)
            data.append(v)
        result.write('\t'.join(map(str, header)) + '\n')
        result.write('\t'.join(map(str, data)) + '\n')

    # Write data from landmark_reference, acute_vertex, scale_features if it was stored
    if 'landmark_reference' in outputs.measurements:
        header = ['HEADER_LANDMARK']
        data = ['LANDMARK_DATA']
        for k, v in outputs.measurements['landmark_reference'].items():
            header.append(k)
            data.append(v)
        result.write('\t'.join(map(str, header)) + '\n')
        result.write('\t'.join(map(str, data)) + '\n')

    # Write data from report_size_marker if it was stored
    if 'size_marker' in outputs.measurements:
        header = ['HEADER_MARKER']
        data = ['MARKER_DATA']
        for k, v in outputs.measurements['size_marker'].items():
            header.append(k)
            data.append(v)
        result.write('\t'.join(map(str, header)) + '\n')
        result.write('\t'.join(map(str, data)) + '\n')

    # Write data from watershed if it was stored
    if 'watershed' in outputs.measurements:
        header = ['HEADER_WATERSHED']
        data = ['WATERSHED_DATA']
        for k, v in outputs.measurements['watershed'].items():
            header.append(k)
            data.append(v)
        result.write('\t'.join(map(str, header)) + '\n')
        result.write('\t'.join(map(str, data)) + '\n')

    # Write data from morphology functions if it was stored
    if 'morphology_data' in outputs.measurements:
        if 'num_cycles' in outputs.measurements['morphology_data']:
            header = ['HEADER_CYCLE', 'num_cycles']
            data = ['CYCLE_DATA']
            v = outputs.measurements['morphology_data']['num_cycles']
            data.append(v)
            result.write('\t'.join(map(str, header)) + '\n')
            result.write('\t'.join(map(str, data)) + '\n')
        if 'segment_angles' in outputs.measurements['morphology_data']:
            header = ['HEADER_ANGLE']
            data = ['ANGLE_DATA']
            for k, v in enumerate(outputs.measurements['morphology_data']['segment_angles']):
                header.append(k)
                data.append(v)
            result.write('\t'.join(map(str, header)) + '\n')
            result.write('\t'.join(map(str, data)) + '\n')
        if 'segment_curvature' in outputs.measurements['morphology_data']:
            header = ['HEADER_CURVATURE']
            data = ['CURVATURE_DATA']
            for k, v in enumerate(outputs.measurements['morphology_data']['segment_curvature']):
                header.append(k)
                data.append(v)
            result.write('\t'.join(map(str, header)) + '\n')
            result.write('\t'.join(map(str, data)) + '\n')
        if 'segment_eu_lengths' in outputs.measurements['morphology_data']:
            header = ['HEADER_EU_LENGTH']
            data = ['EU_LENGTH_DATA']
            for k, v in enumerate(outputs.measurements['morphology_data']['segment_eu_lengths']):
                header.append(k)
                data.append(v)
            result.write('\t'.join(map(str, header)) + '\n')
            result.write('\t'.join(map(str, data)) + '\n')
        if 'segment_path_lengths' in outputs.measurements['morphology_data']:
            header = ['HEADER_PATH_LENGTH']
            data = ['PATH_LENGTH_DATA']
            for k, v in enumerate(outputs.measurements['morphology_data']['segment_path_lengths']):
                header.append(k)
                data.append(v)
            result.write('\t'.join(map(str, header)) + '\n')
            result.write('\t'.join(map(str, data)) + '\n')
        if 'segment_tan_angles' in outputs.measurements['morphology_data']:
            header = ['HEADER_TAN_ANGLE']
            data = ['TAN_ANGLE_DATA']
            for k, v in enumerate(outputs.measurements['morphology_data']['segment_tan_angles']):
                header.append(k)
                data.append(v)
            result.write('\t'.join(map(str, header)) + '\n')
            result.write('\t'.join(map(str, data)) + '\n')
        if 'segment_insertion_angles' in outputs.measurements['morphology_data']:
            header = ['HEADER_INSERTION_ANGLE']
            data = ['INSERTION_ANGLE_DATA']
            for k, v in enumerate(outputs.measurements['morphology_data']['segment_insertion_angles']):
                header.append(k)
                data.append(v)
            result.write('\t'.join(map(str, header)) + '\n')
            result.write('\t'.join(map(str, data)) + '\n')

    result.close()
