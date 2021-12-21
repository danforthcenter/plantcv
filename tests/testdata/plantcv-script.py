#!/usr/bin/env python

from plantcv import plantcv as pcv
import argparse


def options():
    parser = argparse.ArgumentParser(description="Test PlantCV workflow.")
    parser.add_argument("--image", help="Input image file.", required=True)
    parser.add_argument("--debug", help="Turn on debug, prints intermediate images.", default=None)
    parser.add_argument("--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("--result", help="result file.", required=False)
    parser.add_argument("--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("--other", help="Optional input.", required=False)
    args = parser.parse_args()
    return args


def main():
    args = options()
    _ = pcv.__version__

    shape_header = ['HEADER_SHAPES', 'area', 'hull-area', 'solidity', 'perimeter', 'width', 'height', 'longest_axis',
                    'center-of-mass-x', 'center-of-mass-y', 'hull_vertices', 'in_bounds', 'ellipse_center_x',
                    'ellipse_center_y', 'ellipse_major_axis', 'ellipse_minor_axis', 'ellipse_angle',
                    'ellipse_eccentricity']
    shape_data = ['SHAPES_DATA', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    shape_img = [['IMAGE', 'shapes', 'shape_image.png']]
    color_header = ['HEADER_HISTOGRAM', 'bin-number', 'bin-values', 'blue', 'green', 'red', 'lightness',
                    'green-magenta', 'blue-yellow', 'hue', 'saturation', 'value']
    color_data = ['HISTOGRAM_DATA', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    color_img = [['IMAGE', 'hist', 'pseudo_img.png']]
    boundary_header = ['HEADER_BOUNDARY1', 'height_above_bound', 'height_below_bound', 'above_bound_area',
                       'percent_above_bound_area', 'below_bound_area', 'percent_below_bound_area']
    boundary_data = ['BOUNDARY_DATA', 1, 1, 1, 1, 1, 1]
    boundary_img = ['IMAGE', 'boundary', 'boundary_img.png']

    # Output shape and color parallel_data
    result = open(args.result, "a")
    result.write('META\timage\t' + args.image + '\n')
    result.write('META\ttimestamp\t2014-10-22 17:49:35.187\n')
    result.write('META\tframe\t0\n')
    result.write('META\tlifter\th1\n')
    result.write('META\tgain\tg0\n')
    result.write('META\tmeasurementlabel\tC002ch_092214_biomass\n')
    result.write('META\tcartag\t2143\n')
    result.write('META\tid\t117770\n')
    result.write('META\texposure\te82\n')
    result.write('META\tzoom\tz1\n')
    result.write('META\tplantbarcode\tCa031AA010564\n')
    result.write('META\tcamera\tSV\n')
    result.write('META\ttreatment\tnone\n')
    result.write('META\timgtype\tVIS\n')
    result.write('META\tother\tnone\n')
    result.write('\t'.join(map(str, shape_header)) + "\n")
    result.write('\t'.join(map(str, shape_data)) + "\n")
    for row in shape_img:
        result.write('\t'.join(map(str, row)) + "\n")
    result.write('\t'.join(map(str, color_header)) + "\n")
    result.write('\t'.join(map(str, color_data)) + "\n")
    result.write('\t'.join(map(str, boundary_header)) + "\n")
    result.write('\t'.join(map(str, boundary_data)) + "\n")
    result.write('\t'.join(map(str, boundary_img)) + "\n")
    for row in color_img:
        result.write('\t'.join(map(str, row)) + "\n")
    result.close()


if __name__ == '__main__':
    main()
