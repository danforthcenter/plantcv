#!/usr/bin/env python

import argparse
import os
import sqlite3 as sq
from plantcv import plantcv as pcv
from shutil import copy
import datetime


# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Extract a random number of images from a PlantCV dataset.")
    parser.add_argument("-d", "--database", help="SQLite database file from plantcv.")
    parser.add_argument("-r", "--random", help="number of random images you would like", type=int, required=False)
    parser.add_argument("-i", "--imgtype", help="Imgtype (VIS, NIR, PSII, etc.).", required=True)
    parser.add_argument("-s", "--camera", help="Camera (SV, TV, etc.)", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory.", required=True)
    parser.add_argument("-v", "--verbose", help="Turn on verbose output.", action='store_true', default=False)
    args = parser.parse_args()
    return args


# Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Grab Random Image Ids From Database
def grab_random(database, random, imgtype, camera, outdir, verbose):
    # Does the database exist?
    if not os.path.exists(database):
        pcv.fatal_error("The database file " + str(database) + " does not exist")

    # Open a connection
    try:
        connect = sq.connect(database)
    except sq.Error as e:
        print("Error %s:" % e.args[0])
    else:
        # Replace the row_factory result constructor with a dictionary constructor
        connect.row_factory = dict_factory
        # Change the text output format from unicode to UTF-8
        connect.text_factory = str

        # Database handler
        db = connect.cursor()
        imageid_list = []
        num = random
        if verbose:
            print(num)
        list_random = db.execute('select * from metadata where imgtype=? and camera=? order by random() limit ?',
                                 (imgtype, camera, num,))
        for i, x in enumerate(list_random):
            imgid = x['image_id']
            imageid_list.append(imgid)

        if verbose:
            print(imageid_list)

        for imgid in imageid_list:
            get_image = db.execute('select * from metadata where image_id=?', (imgid,))
            for row in get_image:
                dt = datetime.datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S.%f").strftime('%Y-%m-%d-%H-%M-%S')
                img_name = os.path.join(outdir,
                                        row['plantbarcode'] + "_" + dt + "_" + os.path.basename(row['image']))
                copy(row['image'], img_name)
                if verbose:
                    print("copying")
                    print(img_name)


# Main pipeline
def main():
    # Get options
    args = options()

    grab_random(args.database, args.random, args.imgtype, args.camera, args.outdir, args.verbose)


if __name__ == '__main__':
    main()
