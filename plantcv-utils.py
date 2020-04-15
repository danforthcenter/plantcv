#!/usr/bin/env python

import sys
import argparse
import plantcv.utils


# Parse command-line arguments
###########################################
def options():
    """Parse command line options.
    """

    # Create an argument parser
    parser = argparse.ArgumentParser(description="A collection of utilities for PlantCV.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Create subcommand parsers
    subparsers = parser.add_subparsers()

    # Create the json2csv subcommand
    json2csv_cmd = subparsers.add_parser("json2csv", help="Convert PlantCV output JSON files to CSV.")
    json2csv_cmd.add_argument("-j", "--json", help="Input PlantCV JSON filename.", required=True)
    json2csv_cmd.add_argument("-c", "--csv", help="Output CSV filename prefix.", required=True)
    json2csv_cmd.set_defaults(func=run_json2csv)

    # Create the tabulate_bayes_classes subcommand
    json2csv_cmd = subparsers.add_parser("tabulate_bayes_classes", help="Convert pixel samples to a Bayes class table.")
    json2csv_cmd.add_argument("-i", "--infile", help="Input text file.", required=True)
    json2csv_cmd.add_argument("-o", "--outfile", help="Output tab-delimited table file.", required=True)
    json2csv_cmd.set_defaults(func=run_tabulate_bayes_classes)

    # Create the sample_images subcommand
    sample_images_cmd = subparsers.add_parser("sample_images", help="Creates a random sample of images.")
    sample_images_cmd.add_argument("-s", "--source", help="Source directory of images", required=True)
    sample_images_cmd.add_argument("-o", "--outdir", help="Output directory for the random sample to get saved",
                                   required=True)
    sample_images_cmd.add_argument("-n", "--number", help="The number of images to sample", default=100, type=int)
    sample_images_cmd.set_defaults(func=run_sample_images)

    # If no arguments are given, print the help menu
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        raise SystemExit()

    # Parse command-line options
    args = parser.parse_args()
    # Execute the selected method
    args.func(args)

###########################################


# run_json2csv
###########################################
def run_json2csv(args):
    plantcv.utils.json2csv(json_file=args.json, csv_file=args.csv)
###########################################


# run_json2csv
###########################################
def run_tabulate_bayes_classes(args):
    plantcv.utils.tabulate_bayes_classes(input_file=args.infile, output_file=args.outfile)
###########################################


# run_sample_images
###########################################
def run_sample_images(args):
    plantcv.utils.sample_images(source_path=args.source, dest_path=args.outdir, num=args.number)

###########################################


# Main
###########################################
def main():
    """Main program.
    """
    # Parse command-line options and run the selected method
    options()
###########################################


if __name__ == '__main__':
    main()
