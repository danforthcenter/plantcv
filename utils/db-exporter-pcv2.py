#!/usr/bin/env python

import argparse
import os
import sqlite3 as sq
import pandas as pd
import numpy as np
import time


# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
    parser.add_argument("-d", "--database", help="SQLite database file from plantcv.", required=True)
    parser.add_argument("-o", "--outfile", help="Output text file.", required=True)
    parser.add_argument("-f", "--filter", help="process type, 'filter', or 'raw'", default='raw')
    parser.add_argument("-i", "--imgtype", help="Type of image either 'VIS', 'NIR', or 'BOTH', or 'NONE' ",
                        default='BOTH')
    parser.add_argument("-a", "--angles", help="Total number of angles (TV and SV)", default=5)
    parser.add_argument("-s", "--signal", help="if true outputs signal data as well", default=False)
    parser.add_argument("-n", "--signalnorm", help="if true normalizes signal data to area of object", default=False)
    parser.add_argument("-v", "--signalavg", help="if true also output averaged sv and seperated tv files",
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


def main():
    t0 = time.time()
    print("starting time...")

    # Get options
    args = options()

    # Does the database exist?
    if not os.path.exists(args.database):
        raise ("The database file " + str(args.database) + " does not exist")

    # Open a connection
    try:
        db = sq.connect(args.database)
    except sq.Error as e:
        print("Error %s:" % e.args[0])
    else:
        # Get the headers for metadata and headers for features these will be the headers of features table
        metadata = pd.read_sql_query('SELECT * FROM metadata', db)
        features = pd.read_sql_query('SELECT * FROM features', db)
        mheader = []
        fheader = []
        totalangles = int(args.angles)

        for colname in metadata:
            mheader.append(colname)
        for colname in features:
            fheader.append(colname)

        # Get the headers for signal table
        cmetadata = pd.read_sql_query('SELECT * FROM metadata', db)
        cfeatures = pd.read_sql_query('SELECT features.image_id, features.area FROM features', db)
        csignal = pd.read_sql_query('SELECT * from signal', db)

        signalheader = []

        for colname in cmetadata:
            signalheader.append(colname)
        for colname in cfeatures:
            signalheader.append(colname)
        for colname in csignal:
            signalheader.append(colname)

        ######################################################################################

        # Get the unfiltered signal data

        if args.signal:
            if args.imgtype == 'BOTH':
                signal1 = pd.read_sql_query('SELECT metadata.*, features.image_id, features.area, signal.* FROM '
                                            'metadata INNER JOIN features ON metadata.image_id=features.image_id '
                                            'INNER JOIN signal ON metadata.image_id=signal.image_id WHERE '
                                            'imgtype="VIS"', db)
                signal2 = pd.read_sql_query('SELECT metadata.*, features.image_id, features.area, signal.* FROM '
                                            'metadata INNER JOIN features ON metadata.image_id=features.image_id '
                                            'INNER JOIN signal ON metadata.image_id=signal.image_id WHERE '
                                            'imgtype="NIR"', db)
                sx1, sy1 = signal1.shape
                sx2, sy2 = signal2.shape
            else:
                signal1 = pd.read_sql_query('SELECT metadata.*, features.image_id, features.area, signal.* FROM '
                                            'metadata INNER JOIN features ON metadata.image_id=features.image_id '
                                            'INNER JOIN signal ON metadata.image_id=signal.image_id', db)
                sx1, sy1 = signal1.shape
                sx2 = None

            ######################################################################################

            # Get the unfiltered data
        if args.imgtype == 'BOTH':
            table1 = pd.read_sql_query('SELECT * FROM metadata INNER JOIN features ON '
                                       'metadata.image_id=features.image_id WHERE imgtype="VIS"', db)
            table2 = pd.read_sql_query('SELECT * FROM metadata INNER JOIN features ON '
                                       'metadata.image_id=features.image_id WHERE imgtype="NIR"', db)
            ix1, iy1 = table1.shape
            ix2, iy2 = table2.shape

        # Join metadata and features
        elif args.imgtype == 'NONE':
            table = pd.read_sql_query('SELECT * FROM metadata INNER JOIN features ON '
                                      'metadata.image_id=features.image_id', db)
            ix, iy = table.shape

        else:
            # Join metadata and features, and select imgtype
            table = pd.read_sql_query('SELECT * FROM metadata INNER JOIN features ON '
                                      'metadata.image_id=features.image_id WHERE imgtype=?', db,
                                      params=(str(args.imgtype),))
            ix, iy = table.shape

            ######################################################################################

        # Filter data by number of angles

        if args.filter == 'filter':

            vissnapshots = []
            nirsnapshots = []
            snapshots = []

            finalvis = []
            finalnir = []
            finalsnapshots = []

            removedvis = []
            removednir = []
            removedsnapshots = []

            if args.imgtype == 'BOTH':

                # get all the unique timestamps for VIS
                time1 = pd.read_sql_query('SELECT DISTINCT(`timestamp`) FROM `metadata` WHERE `imgtype` = "VIS"', db)
                vissnapshots.append(time1['timestamp'])

                # get all the unique timestamps for NIR
                time2 = pd.read_sql_query('SELECT DISTINCT(`timestamp`) FROM `metadata` WHERE `imgtype` = "NIR"', db)
                nirsnapshots.append(time2['timestamp'])

                # get the timestamps with all angles
                for snap in vissnapshots[0]:
                    # print("checking angles for "+str(snap))
                    visrow = pd.read_sql_query(
                        'SELECT * from metadata INNER JOIN features on metadata.image_id=features.image_id '
                        'WHERE imgtype="VIS" and timestamp=?', db, params=(str(snap),))
                    vangles = (len(visrow))

                    if totalangles == int(vangles):
                        fintimestamp = snap
                        finalvis.append(fintimestamp)
                    else:
                        fintimestamp = snap
                        removedvis.append(fintimestamp)

                print("removing " + str(len(removedvis)) + " timestamps from vis measurements")
                for remove in removedvis:
                    table1 = table1[table1['timestamp'] != remove]

                if args.signal:
                    print("removing " + str(len(removedvis)) + " timestamps from signal")
                    for remove in removedvis:
                        signal1 = signal1[signal1['timestamp'] != remove]

                # get the timestamps with all angles
                for snap in nirsnapshots[0]:
                    print("checking angles for " + str(snap))
                    nirrow = pd.read_sql_query(
                        'SELECT * from metadata INNER JOIN features on metadata.image_id=features.image_id '
                        'WHERE imgtype="NIR" and timestamp=?', db, params=(str(snap),))
                    nangles = (len(nirrow))

                    if totalangles == int(nangles):
                        fintimestamp = snap
                        finalnir.append(fintimestamp)
                    else:
                        fintimestamp = snap
                        removednir.append(fintimestamp)
                        print(len(removednir))

                print("removing " + str(len(removednir)) + " timestamps from nir measurements")
                for remove in removednir:
                    table2 = table2[table2['timestamp'] != remove]

                if args.signal:
                    print("removing " + str(len(removednir)) + " timestamps from nir signal")
                    for remove in removednir:
                        signal2 = signal2[signal2['timestamp'] != remove]

                if args.debug:
                    print(str(len(removedvis)) + " vis timestamps removed")
                    print(str(len(removednir)) + " nir timestamps removed")

            elif args.imgtype == "NONE":
                time1 = pd.read_sql_query('SELECT DISTINCT(`timestamp`) FROM `metadata`', db)
                snapshots.append(time1['timestamp'])

                # get the timestamps with all angles
                for snap in snapshots[0]:
                    print("checking angles for " + str(snap))
                    visrow = pd.read_sql_query(
                        'SELECT * from metadata INNER JOIN features on metadata.image_id=features.image_id '
                        'WHERE timestamp=?', db, params=(str(snap),))
                    vangles = (len(visrow))

                    if totalangles == int(vangles):
                        fintimestamp = snap
                        finalsnapshots.append(fintimestamp)
                    else:
                        fintimestamp = snap
                        removedsnapshots.append(fintimestamp)
                        print(len(removedsnapshots))

                print("removing " + str(len(removedsnapshots)) + " snapshots")
                for remove in removedsnapshots:
                    print(remove)
                    table = table[table['timestamp'] != remove]

                if args.signal:
                    print("removing " + str(len(removedsnapshots)) + " timestamps from signal")
                    for remove in removedsnapshots:
                        signal1 = signal1[signal1['timestamp'] != remove]

                if args.debug:
                    print(str(len(removedsnapshots)) + " snapshots removed")

            else:

                time1 = pd.read_sql_query('SELECT DISTINCT(`timestamp`) FROM `metadata` WHERE imgtype=?', db,
                                          params=(str(args.imgtype),))
                snapshots.append(time1['timestamp'])

                # get the timestamps with all angles
                for snap in snapshots[0]:
                    print("checking angles for " + str(snap))
                    visrow = pd.read_sql_query(
                        'SELECT * from metadata INNER JOIN features on metadata.image_id=features.image_id '
                        'WHERE timestamp=?', db, params=(str(snap),))
                    vangles = (len(visrow))

                    if totalangles == int(vangles):
                        fintimestamp = snap
                        finalsnapshots.append(fintimestamp)
                    else:
                        fintimestamp = snap
                        removedsnapshots.append(fintimestamp)
                        print(len(removedsnapshots))

                print("removing " + str(len(removedsnapshots)) + " " + str(args.imgtype) + " snapshots")
                for remove in removedsnapshots:
                    table = table[table['timestamp'] != remove]

                if args.signal:
                    print("removing " + str(len(removedsnapshots)) + " timestamps from signal")
                    for remove in removedsnapshots:
                        signal1 = signal1[signal1['timestamp'] != remove]

                if args.debug:
                    print(str(len(removedsnapshots)) + " snapshots removed")

                ######################################################################################

                # No filtering if raw is selected

        elif args.filter == 'raw':

            if args.imgtype == 'BOTH':
                table1 = table1
                table2 = table2
            else:
                table = table

            ######################################################################################

            # Write the features data out

        if args.imgtype == 'BOTH':
            if ix1 == 0:
                pass

            if ix1 != 0:
                finalfeatures = []
                # Select the features that are not completely empty
                for x in fheader:
                    if x == 'in_bounds' or x == 'image_id':
                        finalfeatures.append(x)
                        mheader.append(x)
                    elif x != 'in_bounds':
                        table1[str(x)] = table1[str(x)].astype(float)
                        sumcol = (table1[str(x)].sum())
                        if sumcol != 0.0:
                            finalfeatures.append(x)
                            mheader.append(x)
                # Subset table with the features that are not completely empty
                table1 = table1[mheader]
                if args.filter == 'filter':
                    visout = str(args.outfile) + "-vis-filtered.csv"
                else:
                    visout = str(args.outfile) + "-vis-notfiltered.csv"
                table1.to_csv(str(visout), mode='a')

            if ix2 == 0:
                pass

            if ix2 != 0:
                finalfeatures = []
                # Select the features that are not completely empty
                for x in fheader:
                    if x == 'in_bounds' or x == 'image_id':
                        finalfeatures.append(x)
                        mheader.append(x)
                    elif x != 'in_bounds':
                        table2[str(x)] = table2[str(x)].astype(float)
                        sumcol = (table2[str(x)].sum())
                        if sumcol != 0.0:
                            finalfeatures.append(x)
                            mheader.append(x)
                # Subset table with the features that are not completely empty
                table2 = table2[mheader]
                if args.filter == 'filter':
                    nirout = str(args.outfile) + "-nir-filtered.csv"
                else:
                    nirout = str(args.outfile) + "-nir-notfiltered.csv"
                table2.to_csv(str(nirout), mode='a')

        else:
            if ix == 0:
                pass
            else:
                finalfeatures = []
                # Select the features that are not completely empty
                for x in fheader:
                    if x == 'in_bounds' or x == 'image_id':
                        finalfeatures.append(x)
                        mheader.append(x)
                    elif x != 'in_bounds':
                        table[str(x)] = table[str(x)].astype(float)
                        sumcol = (table[str(x)].sum())
                        if sumcol != 0.0:
                            finalfeatures.append(x)
                            mheader.append(x)
                # Subset table with the features that are not completely empty
                table = table[mheader]
                if args.filter == 'filter':
                    tablename = str(args.outfile) + "-data-filtered.csv"
                else:
                    tablename = str(args.outfile) + "-data-notfiltered.csv"
                # Write table to csv file
                table.to_csv(str(tablename), mode='a')

            #######################################################################################

        if args.signal:
            if sx1 != 0:
                print("starting on signal data")
                # get the channel column
                channel1 = signal1['channel_name'].astype('str')
                # get number of bins
                bins = signal1['bin-number'].astype(int)
                # get unique channels
                uniquechannel = np.unique(channel1)
                uniquebin = np.unique(bins)
                binheader = []
                # get signal data and make into sep columns make new headers based on bins and channels
                for x in range(0, uniquebin):
                    bin = 'bin_' + str(x)
                    binheader.append(bin)
                signalsplit = signal1['values'].apply(lambda x: pd.Series(x.split(',')))
                signalsplit.columns = binheader

                # drop the values column so that you can replace it with the seperated columns
                signaldata = signal1
                signal1 = signal1.drop('values', axis=1)
                image_id = signal1['image_id'].take([0], axis=1)
                signalbase = signal1.drop('image_id', axis=1)
                signalbase = signalbase.join(image_id)
                signalbase = signalbase.drop('channel_name', axis=1)
                signalbase = signalbase.drop_duplicates('image_id')

                headers = signalbase.columns.values
                signalall = signalbase

                # get just the signal data and join it with the channel column
                signalsplit = signalsplit.join(signal1['channel_name'])

                # rename the bin columns so they can be associated with the color names
                for channel in uniquechannel:
                    subset = signalsplit[signalsplit['channel_name'] == str(channel)]
                    subset = subset.drop('channel_name', axis=1)
                    names = subset.columns.values
                    newnames = [n.replace('bin', str(channel)) for n in names]
                    headers = np.concatenate((headers, newnames), axis=0)
                    signalall.reset_index(drop=True, inplace=True)
                    subset.reset_index(drop=True, inplace=True)
                    signalall = pd.concat([signalall, subset], axis=1)
                signalall.columns = headers
                signalnormbase = signalall
                normsignalheaders = signalnormbase.filter(regex='\d', axis=1).columns.values
                if args.filter == 'filter':
                    filename = str(args.outfile) + "_signal-filtered.csv"
                else:
                    filename = str(args.outfile) + "_signal-notfiltered.csv"
                signalall.to_csv(filename, mode='w')

                if args.signalnorm:
                    print("normalizing signal data")
                    normsignal = []
                    area = signalnormbase['area'].astype(float)
                    area = area.as_matrix()
                    for bin in normsignalheaders:
                        datacol = signalnormbase[str(bin)].astype(float)
                        datacol = datacol.as_matrix()
                        normcol = np.divide(datacol, area)
                        normcol *= 100
                        normsignal.append(normcol)
                    normsignal = np.transpose(normsignal)
                    normsignal = pd.DataFrame(normsignal, columns=normsignalheaders)
                    signalnormbase1 = signalnormbase.filter(regex='^((?!\d).)*$', axis=1)
                    signalnormbase2 = pd.concat([signalnormbase1, normsignal], axis=1)
                    headers1 = signalnormbase.columns.values
                    signalnormbase2.columns = headers1

                    if args.filter == 'filter':
                        filename = str(args.outfile) + "_signal-filtered-normalized.csv"
                    else:
                        filename = str(args.outfile) + "_signal-notfiltered-normalized.csv"
                    signalnormbase2.to_csv(filename, mode='w')

                    if args.signalavg:
                        print("averaging normalized signal data")
                        avgnormsignal = signalnormbase2
                        avgnormsv = avgnormsignal[avgnormsignal['camera'] == 'SV']
                        svx, svy = np.shape(avgnormsv)
                        avgnormtv = avgnormsignal[avgnormsignal['camera'] == 'TV']
                        tvx, tvy = np.shape(avgnormtv)
                        avgnormnone = avgnormsignal[avgnormsignal['camera'] == 'NONE']
                        nonex, noney = np.shape(avgnormnone)

                        if svx != 0:
                            svbase = avgnormsv.filter(regex='^((?!_).)*$', axis=1)
                            svbase = svbase.join(avgnormsv['image_id'])
                            svbase = svbase.drop_duplicates('timestamp')
                            svbase.reset_index(drop=True, inplace=True)

                            avgnormsvdata = avgnormsv.filter(regex='_', axis=1)
                            avgnormsvdata = avgnormsvdata.join(avgnormsv['timestamp'])
                            avgnormsvdata = avgnormsvdata.groupby(['timestamp']).mean()
                            avgnormsvdata.reset_index(drop=True, inplace=True)
                            svbase = pd.concat([svbase, avgnormsvdata], axis=1)

                            if args.filter == 'filter':
                                filename = str(args.outfile) + "_signal-sv-filtered-normalized-averaged.csv"
                            else:
                                filename = str(args.outfile) + "_signal-sv-notfiltered-normalized-averaged.csv"
                            svbase.to_csv(filename, mode='w')

                        if tvx != 0:
                            tvbase = avgnormtv.filter(regex='^((?!_).)*$', axis=1)
                            tvbase = tvbase.join(avgnormtv['image_id'])
                            tvbase = tvbase.drop_duplicates('timestamp')
                            tvbase.reset_index(drop=True, inplace=True)

                            avgnormtvdata = avgnormtv.filter(regex='_', axis=1)
                            avgnormtvdata = avgnormtvdata.join(avgnormtv['timestamp'])
                            avgnormtvdata = avgnormtvdata.groupby(['timestamp']).mean()
                            avgnormtvdata.reset_index(drop=True, inplace=True)
                            tvbase = pd.concat([tvbase, avgnormtvdata], axis=1)

                            if args.filter == 'filter':
                                filename = str(args.outfile) + "_signal-tv-filtered-normalized-averaged.csv"
                            else:
                                filename = str(args.outfile) + "_signal-tv-notfiltered-normalized-averaged.csv"
                            tvbase.to_csv(filename, mode='w')

                        if nonex != 0:
                            nonebase = avgnormnone.filter(regex='^((?!_).)*$', axis=1)
                            nonebase = nonebase.join(avgnormnone['image_id'])
                            nonebase = nonebase.drop_duplicates('timestamp')
                            nonebase.reset_index(drop=True, inplace=True)

                            avgnormnonedata = avgnormnone.filter(regex='_', axis=1)
                            avgnormnonedata = avgnormnonedata.join(avgnormnone['timestamp'])
                            avgnormnonedata = avgnormnonedata.groupby(['timestamp']).mean()
                            datacolumns = avgnormnonedata.columns.values
                            avgnormnonedata.reset_index(drop=True, inplace=True)
                            avgnormnonedata.columns = datacolumns
                            nonebase = pd.concat([nonebase, avgnormnonedata], axis=1)

                            if args.filter == 'filter':
                                filename = str(args.outfile) + "_signal-filtered-normalized-averaged.csv"
                            else:
                                filename = str(args.outfile) + "_signal-notfiltered-normalized-averaged.csv"
                            nonebase.to_csv(filename, mode='w')

                if args.signalavg:
                    print("averaging signal data")
                    avgbase = signaldata
                    chanelname = signalsplit['channel_name']
                    signalsplit1 = signalsplit.drop('channel_name', axis=1)
                    signalsplit1 = signalsplit1.astype(float)
                    signalsplit1 = signalsplit1.join(chanelname)
                    signalsplit1 = signalsplit1.join(signaldata['camera'])
                    signalsplit1 = signalsplit1.join(signaldata['timestamp'])

                    svsubset = signalsplit1[signalsplit1['camera'] == 'SV']
                    svx, svy = np.shape(svsubset)

                    svbase = avgbase[avgbase['camera'] == 'SV']
                    svbase = svbase.drop('values', axis=1)
                    image_id = svbase['image_id'].take([0], axis=1)
                    svbase = svbase.drop('image_id', axis=1)
                    svbase = svbase.join(image_id)
                    svbase = svbase.drop('channel_name', axis=1)
                    svbase = svbase.drop_duplicates('timestamp')
                    svbase.reset_index(drop=True, inplace=True)

                    tvsubset = signalsplit1[signalsplit1['camera'] == 'TV']
                    tvx, tvy = np.shape(tvsubset)

                    tvbase = avgbase[avgbase['camera'] == 'TV']
                    tvbase = tvbase.drop('values', axis=1)
                    image_id = tvbase['image_id'].take([0], axis=1)
                    tvbase = tvbase.drop('image_id', axis=1)
                    tvbase = tvbase.join(image_id)
                    tvbase = tvbase.drop('channel_name', axis=1)
                    tvbase = tvbase.drop_duplicates('timestamp')
                    tvbase.reset_index(drop=True, inplace=True)

                    nonesubset = signalsplit1[signalsplit1['camera'] == 'NONE']
                    nonex, noney = np.shape(nonesubset)

                    nonebase = avgbase[avgbase['camera'] == 'NONE']
                    nonebase = nonebase.drop('values', axis=1)
                    image_id = nonebase['image_id'].take([0], axis=1)
                    nonebase = nonebase.drop('image_id', axis=1)
                    nonebase = nonebase.join(image_id)
                    nonebase = nonebase.drop('channel_name', axis=1)
                    nonebase = nonebase.drop_duplicates('timestamp')
                    nonebase.reset_index(drop=True, inplace=True)

                    for channel in uniquechannel:
                        if svx != 0:
                            subset = svsubset[svsubset['channel_name'] == str(channel)]
                            subset = subset.drop('camera', axis=1)
                            subset = subset.drop('channel_name', axis=1)
                            subset = subset.groupby(['timestamp']).mean()
                            names = subset.columns.values
                            newnames = [n.replace('bin', str(channel)) for n in names]
                            subset.columns = newnames
                            subset.reset_index(drop=True, inplace=True)
                            svbase.reset_index(drop=True, inplace=True)
                            svbase = pd.concat([svbase, subset], axis=1)

                        if tvx != 0:
                            subset1 = tvsubset[tvsubset['channel_name'] == str(channel)]
                            subset1 = subset1.drop('camera', axis=1)
                            subset1 = subset1.drop('channel_name', axis=1)
                            subset1 = subset1.groupby(['timestamp']).mean()
                            names = subset1.columns.values
                            newnames = [n.replace('bin', str(channel)) for n in names]
                            subset1.columns = newnames
                            subset1.reset_index(drop=True, inplace=True)
                            tvbase.reset_index(drop=True, inplace=True)
                            tvbase = pd.concat([tvbase, subset1], axis=1)

                        if nonex != 0:
                            subset2 = nonesubset[nonesubset['channel_name'] == str(channel)]
                            subset2 = subset2.drop('camera', axis=1)
                            subset2 = subset2.drop('channel_name', axis=1)
                            subset2 = subset2.groupby(['timestamp']).mean()
                            names = subset2.columns.values
                            newnames = [n.replace('bin', str(channel)) for n in names]
                            subset2.columns = newnames
                            subset2.reset_index(drop=True, inplace=True)
                            nonebase.reset_index(drop=True, inplace=True)
                            nonebase = pd.concat([nonebase, subset2], axis=1)

                    if svx != 0:
                        if args.filter == 'filter':
                            filename = str(args.outfile) + "-signal-sv-filtered-averaged.csv"
                        else:
                            filename = str(args.outfile) + "-signal-sv-notfiltered-averaged.csv"
                        svbase.to_csv(filename, mode='w')

                    if tvx != 0:
                        if args.filter == 'filter':
                            filename = str(args.outfile) + "-signal-tv-filtered-averaged.csv"
                        else:
                            filename = str(args.outfile) + "-signal-tv-notfiltered-averaged.csv"
                        tvbase.to_csv(filename, mode='w')

                    if nonex != 0:
                        if args.filter == 'filter':
                            filename = str(args.outfile) + "-signal-filtered-averaged.csv"
                        else:
                            filename = str(args.outfile) + "-signal-notfiltered-averaged.csv"
                        nonebase.to_csv(filename, mode='w')

            if sx2 != None:
                print("analyzing signal 2 data")
                # get the channel column
                channel1 = signal2['channel_name'].astype('str')
                # get number of bins
                bins = signal2['bin-number'].astype(int)
                # get unique channels
                uniquechannel = np.unique(channel1)
                uniquebin = np.unique(bins)
                binheader = []
                # get signal data and make into sep columns make new headers based on bins and channels
                for x in range(0, uniquebin):
                    bin = 'bin_' + str(x)
                    binheader.append(bin)
                signalsplit = signal2['values'].apply(lambda x: pd.Series(x.split(',')))
                signalsplit.columns = binheader

                # drop the values column so that you can replace it with the seperated columns
                signaldata = signal2
                signal2 = signal2.drop('values', axis=1)
                image_id = signal2['image_id'].take([0], axis=1)
                signalbase = signal2.drop('image_id', axis=1)
                signalbase = signalbase.join(image_id)
                signalbase = signalbase.drop('channel_name', axis=1)
                signalbase = signalbase.drop_duplicates('image_id')

                headers = signalbase.columns.values
                signalall = signalbase

                # get just the signal data and join it with the channel column
                signalsplit = signalsplit.join(signal2['channel_name'])

                # rename the bin columns so they can be associated with the color names
                for channel in uniquechannel:
                    subset = signalsplit[signalsplit['channel_name'] == str(channel)]
                    subset = subset.drop('channel_name', axis=1)
                    names = subset.columns.values
                    newnames = [n.replace('bin', str(channel)) for n in names]
                    headers = np.concatenate((headers, newnames), axis=0)
                    signalall.reset_index(drop=True, inplace=True)
                    subset.reset_index(drop=True, inplace=True)
                    signalall = pd.concat([signalall, subset], axis=1)
                signalall.columns = headers
                signalnormbase = signalall
                normsignalheaders = signalnormbase.filter(regex='\d', axis=1).columns.values
                if args.filter == 'filter':
                    filename = str(args.outfile) + "-nir-filtered.csv"
                else:
                    filename = str(args.outfile) + "-nir-notfiltered.csv"
                signalall.to_csv(filename, mode='w')

                if args.signalnorm:
                    print("normalizing signal2 data")
                    normsignal = []
                    area = signalnormbase['area'].astype(float)
                    area = area.as_matrix()
                    for bin in normsignalheaders:
                        datacol = signalnormbase[str(bin)].astype(float)
                        datacol = datacol.as_matrix()
                        normcol = np.divide(datacol, area)
                        normcol *= 100
                        normsignal.append(normcol)
                    normsignal = np.transpose(normsignal)
                    normsignal = pd.DataFrame(normsignal, columns=normsignalheaders)
                    signalnormbase1 = signalnormbase.filter(regex='^((?!\d).)*$', axis=1)
                    signalnormbase2 = pd.concat([signalnormbase1, normsignal], axis=1)
                    headers1 = signalnormbase.columns.values
                    signalnormbase2.columns = headers1

                    if args.filter == 'filter':
                        filename = str(args.outfile) + "-nir-filtered-normalized.csv"
                    else:
                        filename = str(args.outfile) + "-nir-notfiltered-normalized.csv"
                    signalnormbase2.to_csv(filename, mode='w')

                    if args.signalavg:
                        print("averaging normalized signal 2 data")
                        avgnormsignal = signalnormbase2
                        avgnormsv = avgnormsignal[avgnormsignal['camera'] == 'SV']
                        svx, svy = np.shape(avgnormsv)
                        avgnormtv = avgnormsignal[avgnormsignal['camera'] == 'TV']
                        tvx, tvy = np.shape(avgnormtv)
                        avgnormnone = avgnormsignal[avgnormsignal['camera'] == 'NONE']
                        nonex, noney = np.shape(avgnormnone)

                        if svx != 0:
                            svbase = avgnormsv.filter(regex='^((?!_).)*$', axis=1)
                            svbase = svbase.join(avgnormsv['image_id'])
                            svbase = svbase.drop_duplicates('timestamp')
                            svbase.reset_index(drop=True, inplace=True)

                            avgnormsvdata = avgnormsv.filter(regex='_', axis=1)
                            avgnormsvdata = avgnormsvdata.join(avgnormsv['timestamp'])
                            avgnormsvdata = avgnormsvdata.groupby(['timestamp']).mean()
                            avgnormsvdata.reset_index(drop=True, inplace=True)
                            svbase = pd.concat([svbase, avgnormsvdata], axis=1)

                            if args.filter == 'filter':
                                filename = str(args.outfile) + "-nir-sv-filtered-normalized-averaged.csv"
                            else:
                                filename = str(args.outfile) + "-nir-sv-notfiltered-normalized-averaged.csv"
                            svbase.to_csv(filename, mode='w')

                        if tvx != 0:
                            tvbase = avgnormtv.filter(regex='^((?!_).)*$', axis=1)
                            tvbase = tvbase.join(avgnormtv['image_id'])
                            tvbase = tvbase.drop_duplicates('timestamp')
                            tvbase.reset_index(drop=True, inplace=True)

                            avgnormtvdata = avgnormtv.filter(regex='_', axis=1)
                            avgnormtvdata = avgnormtvdata.join(avgnormtv['timestamp'])
                            avgnormtvdata = avgnormtvdata.groupby(['timestamp']).mean()
                            avgnormtvdata.reset_index(drop=True, inplace=True)
                            tvbase = pd.concat([tvbase, avgnormtvdata], axis=1)

                            if args.filter == 'filter':
                                filename = str(args.outfile) + "-nir-tv-filtered-normalized-averaged.csv"
                            else:
                                filename = str(args.outfile) + "-nir-tv-notfiltered-normalized-averaged.csv"
                            tvbase.to_csv(filename, mode='w')

                        if nonex != 0:
                            nonebase = avgnormnone.filter(regex='^((?!_).)*$', axis=1)
                            nonebase = nonebase.join(avgnormnone['image_id'])
                            nonebase = nonebase.drop_duplicates('timestamp')
                            nonebase.reset_index(drop=True, inplace=True)

                            avgnormnonedata = avgnormnone.filter(regex='_', axis=1)
                            avgnormnonedata = avgnormnonedata.join(avgnormnone['timestamp'])
                            avgnormnonedata = avgnormnonedata.groupby(['timestamp']).mean()
                            datacolumns = avgnormnonedata.columns.values
                            avgnormnonedata.reset_index(drop=True, inplace=True)
                            avgnormnonedata.columns = datacolumns
                            nonebase = pd.concat([nonebase, avgnormnonedata], axis=1)

                            if args.filter == 'filter':
                                filename = str(args.outfile) + "-nir-filtered-normalized-averaged.csv"
                            else:
                                filename = str(args.outfile) + "-nir-notfiltered-normalized-averaged.csv"
                            nonebase.to_csv(filename, mode='w')

                if args.signalavg:
                    print("averaging signal2 data")
                    avgbase = signaldata
                    chanelname = signalsplit['channel_name']
                    signalsplit1 = signalsplit.drop('channel_name', axis=1)
                    signalsplit1 = signalsplit1.astype(float)
                    signalsplit1 = signalsplit1.join(chanelname)
                    signalsplit1 = signalsplit1.join(signaldata['camera'])
                    signalsplit1 = signalsplit1.join(signaldata['timestamp'])

                    svsubset = signalsplit1[signalsplit1['camera'] == 'SV']
                    svx, svy = np.shape(svsubset)

                    svbase = avgbase[avgbase['camera'] == 'SV']
                    svbase = svbase.drop('values', axis=1)
                    image_id = svbase['image_id'].take([0], axis=1)
                    svbase = svbase.drop('image_id', axis=1)
                    svbase = svbase.join(image_id)
                    svbase = svbase.drop('channel_name', axis=1)
                    svbase = svbase.drop_duplicates('timestamp')
                    svbase.reset_index(drop=True, inplace=True)

                    tvsubset = signalsplit1[signalsplit1['camera'] == 'TV']
                    tvx, tvy = np.shape(tvsubset)

                    tvbase = avgbase[avgbase['camera'] == 'TV']
                    tvbase = tvbase.drop('values', axis=1)
                    image_id = tvbase['image_id'].take([0], axis=1)
                    tvbase = tvbase.drop('image_id', axis=1)
                    tvbase = tvbase.join(image_id)
                    tvbase = tvbase.drop('channel_name', axis=1)
                    tvbase = tvbase.drop_duplicates('timestamp')
                    tvbase.reset_index(drop=True, inplace=True)

                    nonesubset = signalsplit1[signalsplit1['camera'] == 'NONE']
                    nonex, noney = np.shape(nonesubset)

                    nonebase = avgbase[avgbase['camera'] == 'NONE']
                    nonebase = nonebase.drop('values', axis=1)
                    image_id = nonebase['image_id'].take([0], axis=1)
                    nonebase = nonebase.drop('image_id', axis=1)
                    nonebase = nonebase.join(image_id)
                    nonebase = nonebase.drop('channel_name', axis=1)
                    nonebase = nonebase.drop_duplicates('timestamp')
                    nonebase.reset_index(drop=True, inplace=True)

                    for channel in uniquechannel:
                        if svx != 0:
                            subset = svsubset[svsubset['channel_name'] == str(channel)]
                            subset = subset.drop('camera', axis=1)
                            subset = subset.drop('channel_name', axis=1)
                            subset = subset.groupby(['timestamp']).mean()
                            names = subset.columns.values
                            newnames = [n.replace('bin', str(channel)) for n in names]
                            subset.columns = newnames
                            subset.reset_index(drop=True, inplace=True)
                            svbase.reset_index(drop=True, inplace=True)
                            svbase = pd.concat([svbase, subset], axis=1)

                        if tvx != 0:
                            subset1 = tvsubset[tvsubset['channel_name'] == str(channel)]
                            subset1 = subset1.drop('camera', axis=1)
                            subset1 = subset1.drop('channel_name', axis=1)
                            subset1 = subset1.groupby(['timestamp']).mean()
                            names = subset1.columns.values
                            newnames = [n.replace('bin', str(channel)) for n in names]
                            subset1.columns = newnames
                            subset1.reset_index(drop=True, inplace=True)
                            tvbase.reset_index(drop=True, inplace=True)
                            tvbase = pd.concat([tvbase, subset1], axis=1)

                        if nonex != 0:
                            subset2 = nonesubset[nonesubset['channel_name'] == str(channel)]
                            subset2 = subset2.drop('camera', axis=1)
                            subset2 = subset2.drop('channel_name', axis=1)
                            subset2 = subset2.groupby(['timestamp']).mean()
                            names = subset2.columns.values
                            newnames = [n.replace('bin', str(channel)) for n in names]
                            subset2.columns = newnames
                            subset2.reset_index(drop=True, inplace=True)
                            nonebase.reset_index(drop=True, inplace=True)
                            nonebase = pd.concat([nonebase, subset2], axis=1)

                    if svx != 0:
                        if args.filter == 'filter':
                            filename = str(args.outfile) + "-nir-sv-filtered-averaged.csv"
                        else:
                            filename = str(args.outfile) + "-nir-sv-notfiltered-averaged.csv"
                        svbase.to_csv(filename, mode='w')

                    if tvx != 0:
                        if args.filter == 'filter':
                            filename = str(args.outfile) + "-nir-tv-filtered-averaged.csv"
                        else:
                            filename = str(args.outfile) + "-nir-tv-notfiltered-averaged.csv"
                        tvbase.to_csv(filename, mode='w')

                    if nonex != 0:
                        if args.filter == 'filter':
                            filename = str(args.outfile) + "-nir-filtered-averaged.csv"
                        else:
                            filename = str(args.outfile) + "-nir-notfiltered-averaged.csv"
                        nonebase.to_csv(filename, mode='w')

                    #######################################################################################

        t1 = time.time()
        total = t1 - t0
        print(str(total) + " total time elapsed")


#######################################################################################

if __name__ == '__main__':
    main()
