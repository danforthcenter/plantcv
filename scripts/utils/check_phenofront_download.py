#!/usr/bin/env python
from __future__ import print_function
import os
import argparse


# Parse command-line arguments
###########################################
def options():
    """Parse command line options.

    Args:

    Returns:
        argparse object.
    Raises:

    """

    parser = argparse.ArgumentParser(description="Checks a PhenoFront download for completeness.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--dir", help="Input PhenoFront download directory.", required=True)
    parser.add_argument("-f", "--format", help="Image format.", default="png")
    parser.add_argument("-o", "--outfile", help="Output file for missing images list.", default="missing_images.txt")
    args = parser.parse_args()

    return args


###########################################

# Main
###########################################
def main():
    """Main program.

    Args:

    Returns:

    Raises:
    """

    # Get options
    args = options()

    # Open the SnapshotInfo.csv file
    csvfile = open(args.dir + '/SnapshotInfo.csv', 'rU')

    # Read the first header line
    header = csvfile.readline()
    header = header.rstrip('\n')

    # Remove whitespace from the field name
    header = header.replace(" ", "")

    # Table column order
    cols = header.split(',')
    colnames = {}
    for i, col in enumerate(cols):
        colnames[col] = i

    total_imgs = 0
    downloaded_imgs = 0
    missing_imgs = []

    # Read through the CSV file
    for row in csvfile:
        row = row.rstrip('\n')
        data = row.split(',')
        img_list = data[colnames['tiles']]
        img_list = img_list[:-1]
        imgs = img_list.split(';')
        for img in imgs:
            if len(img) != 0:
                total_imgs += 1
                dirpath = args.dir + '/snapshot' + data[colnames['id']]
                filename = img + '.' + args.format
                if not os.path.exists(dirpath + '/' + filename):
                    missing_imgs.append(dirpath + '/' + filename)
                else:
                    downloaded_imgs += 1

    print("Total images in experiment: " + str(total_imgs) + '\n')
    print("Total downloaded images: " + str(downloaded_imgs) + '\n')

    # Missing files
    if len(missing_imgs) > 0:
        outfile = open(args.outfile, 'w')
        for img in missing_imgs:
            outfile.write(img + '\n')


if __name__ == '__main__':
    main()
