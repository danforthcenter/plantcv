#!/usr/bin/env python

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

    # Create the Kmeans subcommand
    nbm_cmd = subparsers.add_parser("kmeans", help="Run the Kmeans training method.")
    nbm_cmd.add_argument("-i", "--imgdir", help="Input directory containing images.", required=True)
    nbm_cmd.add_argument("-k", "--categories", help="Number of classification categories.", required=True,
                         type=int)
    nbm_cmd.add_argument("-o", "--out", help="Trained model output path and filename.", required=True)
    nbm_cmd.add_argument("-r", "--prefix", help="File prefix for training images.", required=False, default="")
    nbm_cmd.add_argument("-p", "--patch_size", help="Patch size.", required=False, type=int, default=10)
    nbm_cmd.add_argument("-s", "--sigma", help="Severity of Gaussian blur, sigma.", required=False, type=int,
                         default=5)
    nbm_cmd.add_argument("--sampling", help="Fraction of pixels sampled per image for patch extraction",
                         required=False, type=float)
    nbm_cmd.add_argument("--seed", help="Random seed for reproducibility", required=False, type=int,
                         default=1)
    nbm_cmd.add_argument("-n", "--num_imgs", help="Number of images in training directory to use.",
                         required=False, type=int, default=0)
    nbm_cmd.add_argument("--n_init", help="Number of Kmeans random initiations", required=False, type=int,
                         default=10)
    nbm_cmd.set_defaults(func=run_kmeans)

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
    """Run the naive Bayes two-class training method"""
    if not os.path.exists(args.imgdir):
        raise IOError(f"Directory does not exist: {args.imgdir}")
    if not os.path.exists(args.maskdir):
        raise IOError(f"Directory does not exist: {args.maskdir}")
    print("Running the naive Bayes two-class training method...")
    plantcv.learn.naive_bayes(imgdir=args.imgdir, maskdir=args.maskdir, outfile=args.outfile, mkplots=args.plots)
###########################################


# Run the naive Bayes multiclass method
###########################################
def run_naive_bayes_multiclass(args):
    """Run the naive Bayes multiclass training method"""
    if not os.path.exists(args.file):
        raise IOError(f"File does not exist: {args.file}")
    print("Running the naive Bayes multiclass training method...")
    plantcv.learn.naive_bayes_multiclass(samples_file=args.file, outfile=args.outfile, mkplots=args.plots)
###########################################


# Run the Kmeans training method
###########################################
def run_kmeans(args):
    """Run the Kmeans training method"""
    if not os.path.exists(args.imgdir):
        raise IOError(f"Directory does not exist: {args.imgdir}")
    print("Running the Kmeans training method...")
    plantcv.learn.train_kmeans(img_dir=args.imgdir, k=args.categories, out_path=args.out,
                               prefix=args.prefix, patch_size=args.patch_size, sigma=args.sigma,
                               sampling=args.sampling, seed=args.seed, num_imgs=args.num_imgs,
                               n_init=args.n_init)
###########################################


# Run the main program
###########################################
def main():
    """Main program."""
    # Parse command-line options and run training method
    options()
###########################################
