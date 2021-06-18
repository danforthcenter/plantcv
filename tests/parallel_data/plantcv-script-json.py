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

    pcv.outputs.save_results(filename=args.result)


if __name__ == '__main__':
    main()
