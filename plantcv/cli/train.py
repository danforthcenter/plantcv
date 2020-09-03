#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import argparse
import datetime
import plantcv.learn


# Parse command-line arguments
###########################################
def options():
    """Parse command line options.

    :return args: object -- parsed arguments
    :raises: IOError, KeyError
    """

    # Job start time
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    print("Starting run " + start_time + '\n', file=sys.stderr)

    # Create an argument parser
    parser = argparse.ArgumentParser(description="PlantCV machine learning training script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Create subcommand parsers
    subparsers = parser.add_subparsers()

    # Create the Naive Bayes subcommand
    nb_cmd = subparsers.add_parser("naive_bayes", help="Run the naive Bayes two-class training method.")
    nb_cmd.add_argument("-i", "--imgdir", help="Input directory containing images.", required=True)
    nb_cmd.add_argument("-b", "--maskdir", help="Input directory containing black/white masks.", required=True)
    nb_cmd.add_argument("-o", "--outfile", help="Trained classifier output filename.", required=True)
    nb_cmd.add_argument("-p", "--plots", help="Make output plots.", default=False, action="store_true")
    nb_cmd.set_defaults(func=run_naive_bayes)

    # Create the Naive Bayes Multiclass subcommand
    nbm_cmd = subparsers.add_parser("naive_bayes_multiclass",
                                    help="Run the naive Bayes two or more class training method.")
    nbm_cmd.add_argument("-f", "--file",
                         help="Input file containing a table of pixel RGB values sampled for each input class.",
                         required=True)
    nbm_cmd.add_argument("-o", "--outfile", help="Trained classifier output filename.", required=True)
    nbm_cmd.add_argument("-p", "--plots", help="Make output plots.", default=False, action="store_true")
    nbm_cmd.set_defaults(func=run_naive_bayes_multiclass)

    # If no arguments are given, print the help menu
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        raise SystemExit()

    # Parse command-line options
    args = parser.parse_args()
    # Execute the selected training method
    args.func(args)
###########################################


# Run the naive Bayes method
###########################################
def run_naive_bayes(args):
    if not os.path.exists(args.imgdir):
        raise IOError("Directory does not exist: {0}".format(args.imgdir))
    if not os.path.exists(args.maskdir):
        raise IOError("Directory does not exist: {0}".format(args.maskdir))
    print("Running the naive Bayes two-class training method...")
    plantcv.learn.naive_bayes(imgdir=args.imgdir, maskdir=args.maskdir, outfile=args.outfile, mkplots=args.plots)
###########################################


# Run the naive Bayes multiclass method
###########################################
def run_naive_bayes_multiclass(args):
    if not os.path.exists(args.file):
        raise IOError("File does not exist: {0}".format(args.file))
    print("Running the naive Bayes multiclass training method...")
    plantcv.learn.naive_bayes_multiclass(samples_file=args.file, outfile=args.outfile, mkplots=args.plots)
###########################################


# Main
###########################################
def main():
    """Main program.
    """
    # Parse command-line options and run training method
    options()
###########################################


if __name__ == '__main__':
    main()
