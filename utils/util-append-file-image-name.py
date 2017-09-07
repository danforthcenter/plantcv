#!/usr/bin/env python

import argparse
import os
import shutil


# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Get file names to run FASTQC over")
    parser.add_argument("-d", "--directory", help="directory to run script over.")
    parser.add_argument("-o", "--outdir", help="out directory to move files to")
    args = parser.parse_args()
    return args


def append_img_name(directory, outdir):
    dirs = os.listdir(directory)

    dirname = directory
    dirsplit = dirname.split('/')
    experiment = (dirsplit[-1])

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for x in dirs:
        path = os.path.join(directory, x)
        if os.path.isdir(path):
            files = os.listdir(path)
            outdirpath = os.path.join(outdir, experiment, x)
            os.makedirs(outdirpath)
            for i in files:
                filepath = os.path.join(path, i)
                outfilepath = os.path.join(outdirpath, experiment + "_" + x + "_" + i)
                shutil.copyfile(filepath, outfilepath)
                print(filepath)
                print(outfilepath)


# Main pipeline
def main():
    # Get options
    args = options()

    append_img_name(args.directory, args.outdir)


if __name__ == '__main__':
    main()
