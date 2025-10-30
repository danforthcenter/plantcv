#!/usr/bin/env python
import sys
import argparse
from plantcv.parallel.sample_images import sample_images


def options():
    """Parse command line options.

    Args:

    Returns:
        argparse object.
    """
    parser = argparse.ArgumentParser(description='Create a Sample of images with PlantCV.')
    sampleargs = parser.add_argument_group("SAMPLE")
    sampleargs.add_argument("-s", "--source", help="Source directory of images or config file",
                            required=True)
    sampleargs.add_argument("-o", "--outdir", help="Output directory for the random sample to be saved in")
    sampleargs.add_argument("-n", "--number", help="Number of images to sample", default=100, type=int)
    sampleargs.set_defaults(func=run_sample_images)
    args = parser.parse_args()
    args.func(args)


def run_sample_images(args):
    """Sample images from a directory"""
    sample_images(source=args.source, dest_path=args.outdir, num=args.number)


def main():
    """Main program.

    Args:

    Returns:

    Raises:

    """
    options()
