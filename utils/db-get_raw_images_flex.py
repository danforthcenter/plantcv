#!/usr/bin/env python

import argparse
import numpy as np
import os
import sqlite3 as sq
import plantcv as pcv
from shutil import copy
import datetime


# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Get images from an SQLite database and some input information")
    parser.add_argument("-d", "--database", help="SQLite database file from plantcv.")
    parser.add_argument("-f", "--file", help="text file, tab seperated, containing plant IDs and other information.",
                        required=True)
    parser.add_argument("-o", "--outdir", help="Output directory.", required=False)
    parser.add_argument("--vis", help="Images are class VIS.", action='store_true')
    parser.add_argument("--nir", help="Images are class NIR.", action='store_true')
    parser.add_argument("--psii", help="Images are class PSII.", action='store_true')
    parser.add_argument("-v", "--verbose", help="Turn on verbose output.", action='store_true', default=False)
    args = parser.parse_args()
    return args


# Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
  

# Get images with more information
def dict_plant_info(infile):
    # Read table of query parameters from infile
    table = np.genfromtxt(infile, dtype='str', delimiter='\t')

    # Initialize queries
    query = []

    # Read the first row as a header
    header = table[0].tolist()

    # Remove the header row
    table = table[1:]

    # Get the dimensions of the table
    dims = table.shape()
    y = dims[0]
    # If there is only one column then x is not defined, so set x to 1
    x = 1
    if len(dims) == 2:
        x = dims[1]

    # Enumerate the number of columns
    columncount = list(range(0, x))
    # Split up the table
    split_table = np.vsplit(table, y)
    split_table = [l[0] for l in split_table]

    # For each row in the table prepare a query
    for row in split_table:
        where = []
        col = np.hsplit(row, x)
        col = [l[0] for l in col]
        for i, h in enumerate(columncount):
            where.append(str(header[i]) + '=' + "'" + str(col[i] + "'"))
        where_and = ' and '.join(map(str, where))
        query.append(where_and)
    return query


# Database image lookup method
def db_lookup(database, outdir, queries, vis=False, nir=False, psii=False, verbose=False):
    # Does the database exist?
    if not os.path.exists(database):
        pcv.fatal_error("The database file " + str(database) + " does not exist")
  
    # Open a connection
    try:
        connect = sq.connect(database)
    except sq.Error as e:
        IOError("Error %s:" % e.args[0])
    else:
        # Replace the row_factory result constructor with a dictionary constructor
        connect.row_factory = dict_factory
        # Change the text output format from unicode to UTF-8
        connect.text_factory = str

        # Database handler
        db = connect.cursor()

        for query in queries:
            query = 'select * from metadata where ' + str(query)
            if verbose:
                print(query)
            for row in (db.execute(query)):
                dt = datetime.datetime.fromtimestamp(row['datetime']).strftime('%Y-%m-%d-%H-%M-%S')
                if vis and row['imgtype'] == 'VIS':
                    img_name = os.path.join(outdir,
                                            row['plantbarcode'] + "_" + dt + "_" + os.path.basename(row['image']))
                    copy(row['image'], img_name)
                if nir and row['imgtype'] == 'NIR':
                    img_name = os.path.join(outdir,
                                            row['plantbarcode'] + "_" + dt + "_" + os.path.basename(row['image']))
                    copy(row['image'], img_name)
                if psii and row['imgtype'] == 'PSII':
                    images = row['image'].split(',')
                    for image in images:
                        img_name = os.path.join(outdir,
                                                row['plantbarcode'] + "_" + dt + "_" + os.path.basename(image))
                        copy(image, img_name)


# Main pipeline
def main():
    # Get options
    args = options()

    queries = dict_plant_info(args.file)
    db_lookup(args.database, args.outdir, queries, args.vis, args.nir, args.psii, args.verbose)
  

if __name__ == '__main__':
    main()
