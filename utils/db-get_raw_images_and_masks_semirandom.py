#!/usr/bin/env python
import argparse
import os
import sqlite3 as sq
import plantcv as pcv
import pandas as pd
from random import randrange
from shutil import copy


# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
    parser.add_argument("-d", "--database", help="SQLite database file from plantcv.")
    parser.add_argument("-r", "--random", help="number of random images you would like", type=int, default=50)
    parser.add_argument("-o", "--outdir", help="Output directory.", required=True)
    parser.add_argument("-t", "--imgtype", help="VIS, NIR, or None", default="VIS")
    args = parser.parse_args()
    return args


# Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Grab Random Image Ids From Database
def grab_random(database, random, outdir, imgtype):
    # Does the database exist?
    if not os.path.exists(database):
        pcv.fatal_error("The database file " + str(database) + " does not exist")

    # Open a connection
    try:
        db = sq.connect(database)
    except sq.Error as e:
        print("Error %s:" % e.args[0])
    else:
        if imgtype == "VIS":
            # Get the headers for metadata and headers for features these will be the headers of features table
            metaimages = pd.read_sql_query('SELECT * FROM metadata INNER JOIN analysis_images ON '
                                           'metadata.image_id=analysis_images.image_id where '
                                           'analysis_images.type=="mask" and metadata.imgtype=="VIS"', db)
        elif imgtype == "NIR":
            # Get the headers for metadata and headers for features these will be the headers of features table
            metaimages = pd.read_sql_query('SELECT * FROM metadata INNER JOIN analysis_images ON '
                                           'metadata.image_id=analysis_images.image_id where '
                                           'analysis_images.type=="mask" and metadata.imgtype=="NIR"', db)
        elif imgtype == "None":
            # Get the headers for metadata and headers for features these will be the headers of features table
            metaimages = pd.read_sql_query('SELECT * FROM metadata INNER JOIN analysis_images ON '
                                           'metadata.image_id=analysis_images.image_id where '
                                           'analysis_images.type=="mask" and metadata.imgtype=="none"', db)
        else:
            pcv.fatal_error("imgtype is not VIS, NIR or None")

        sorted = metaimages.sort_values(['timestamp'])

        nrowsorted = sorted.shape[0]

        chunksfactor = nrowsorted / float(random)

        random_index_list = []

        for i in range(2, random + 1, 1):
            x = int((i - 1) * chunksfactor)
            y = int(i * chunksfactor)
            randnum = randrange(x, y)
            random_index_list.append(randnum)

        maskdir = os.path.join(outdir, "training-mask-images")
        oridir = os.path.join(outdir, "training-ori-images")

        if not os.path.exists(maskdir):
            os.makedirs(maskdir)
        if not os.path.exists(oridir):
            os.makedirs(oridir)

        for x in random_index_list:
            selectmask = str(sorted.iloc[[x - 1]]['image_path'].item())
            selectori = str(sorted.iloc[[x - 1]]['image'].item())
            copy(selectmask, maskdir + "/")
            copy(selectori, oridir + "/")


# Main pipeline
def main():
    # Get options
    args = options()

    grab_random(args.database, args.random, args.outdir, args.imgtype)


if __name__ == '__main__':
    main()
