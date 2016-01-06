#!/usr/bin/python
import argparse
import os
import sqlite3 as sq


# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
    parser.add_argument("-d", "--database", help="SQLite database file from plantcv.", required=True)
    parser.add_argument("-o", "--outfile", help="Output text file.", required=True)
    parser.add_argument("-t", "--tv", help="Does this experiment use top-view imaging?", action="store_true")
    parser.add_argument("-s", "--sv", help="If this experiment uses side-view imaging, list the angles used",
                        default=False)
    parser.add_argument("-D", "--debug", help="Turn on debugging mode", action="store_true")
    args = parser.parse_args()
    return args


# Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Main pipeline
def main():
    global connect, out

    # Get options
    args = options()

    # Does the database exist?
    if not os.path.exists(args.database):
        raise ("The database file " + str(args.database) + " does not exist")

    # Open a connection
    try:
        connect = sq.connect(args.database)
    except sq.Error, e:
        print("Error %s:" % e.args[0])

    # Open output file
    try:
        out = open(args.outfile, 'w')
    except IOError:
        print("IO error")

    # Replace the row_factory result constructor with a dictionary constructor
    connect.row_factory = dict_factory
    # Change the text output format from unicode to UTF-8
    connect.text_factory = str

    # Database handler
    db = connect.cursor()

    # Get database schema
    feature_names = ['zoom']
    for row in (db.execute("SELECT * FROM `features` LIMIT 1")):
        feature_names += row.keys()

    # Header
    output_header = ['plantbarcode', 'timestamp']
    if args.tv:
        tv_header = ['tv0_zoom']
        for feature in feature_names:
            tv_header += ['tv0_' + feature]
        output_header += tv_header
    if args.sv:
        angles = args.sv.split(',')
        for angle in angles:
            sv_header = ['sv' + angle + '_zoom']
            for feature in feature_names:
                sv_header += ['sv' + str(angle) + '_' + feature]
            output_header += sv_header

    out.write(','.join(map(str, output_header)) + '\n')

    # Retrieve snapshot IDs from the database
    snapshots = []
    for row in (db.execute('SELECT DISTINCT(`timestamp`) FROM `metadata` WHERE `imgtype` = "VIS"')):
        snapshots.append(row['timestamp'])
    if args.debug:
        print('Found ' + str(len(snapshots)) + ' snapshots')

    # Retrieve snapshots and process data
    for snapshot in snapshots:
        data = {'plantbarcode' : '', 'timestamp' : ''}
        for feature in feature_names:
            data[feature] = ''

        for row in (db.execute('SELECT * FROM `metadata` NATURAL JOIN `features` WHERE `timestamp` = "%s" AND `imgtype` = "VIS"' % snapshot)):
            data['plantbarcode'] = row['plantbarcode']
            data['timestamp'] = row['timestamp']
            row['camera'] = row['camera'].lower()

            if row['frame'] == 'none':
                row['frame'] = '0'

            for feature in feature_names:
                data[row['camera'] + row['frame'] + '_' + feature] = row[feature]

        output = []
        for field in output_header:
            output.append(data[field])
        out.write(','.join(map(str, output)) + '\n')

if __name__ == '__main__':
    main()
