#!/usr/bin/env python
import argparse
import sys, os
import sqlite3 as sq
import plantcv as pcv
from shutil import copy
import datetime
import re

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
  parser.add_argument("-d", "--database", help="SQLite database file from plantcv.")
  #parser.add_argument("-c", "--csv", help="PhenoFront CSV file.")
  parser.add_argument("-o", "--outdir", help="Output directory.", required=True)
  #parser.add_argument("--vis", help="Images are class VIS.", action='store_true')
  #parser.add_argument("--nir", help="Images are class NIR.", action='store_true')
  #parser.add_argument("--flu", help="Images are class FLU.", action='store_true')
  parser.add_argument("-t", "--type", help="Image format type (png, jpg).", required=True)
  args = parser.parse_args()
  return args

### Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

### Database image lookup method
def db_lookup(database, outdir, type):
  # Does the database exist?
  if not os.path.exists(database):
    pcv.fatal_error("The database file " + str(database) + " does not exist");
  
  # Open a connection
  try:
    connect=sq.connect(database)
  except sq.Error, e:
    print("Error %s:" % e.args[0])
  
  # Replace the row_factory result constructor with a dictionary constructor
  connect.row_factory = dict_factory
  # Change the text output format from unicode to UTF-8
  connect.text_factory=str

   # Database handler
  db = connect.cursor()
  
  ids = {}
  for row in (db.execute('SELECT DISTINCT(`plant_id`) FROM `snapshots`')):
    ids[row['plant_id']] = 1
  
  for plant_id in ids:
    for row in (db.execute('SELECT MAX(`datetime`) as max FROM `snapshots` WHERE `plant_id` = "%s"' % plant_id)):
      ids[plant_id] = row['max']
  
  for plant_id, timestamp in ids.iteritems():
    plant_outdir = outdir + '/' + plant_id
    os.makedirs(plant_outdir)
    for row in (db.execute('SELECT * FROM `snapshots` WHERE `datetime` = {0}'.format(timestamp))):
      dt = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d_%H:%M:%S')
      if (row['camera'] == 'vis_sv' or row['camera'] == 'vis_tv'):
        img_name = plant_outdir + '/' + row['plant_id'] + '_' + row['camera'] + '_' + str(row['frame']) + '_z' + str(row['zoom']) + '_h' + str(row['lifter']) + '_' + dt + '.' + type
        copy(row['image_path'], img_name)
        print(img_name)
  
### CSV image lookup method
#def csv_lookup(csv, ids, outdir, type, vis=False, nir=False, flu=False):
#  # Regexs
#  vis_pattern = re.compile('^vis', re.IGNORECASE)
#  nir_pattern = re.compile('^nir', re.IGNORECASE)
#  flu_pattern = re.compile('^Flu', re.IGNORECASE)
#  
#  path, img = os.path.split(csv)
#  
#  # Open CSV file
#  with open(csv) as snapshots:
#    for row in snapshots:
#      snapshot = row.rstrip('\n')
#      data = snapshot.split(',')
#      date = data[4].split(' ')
#      if (data[2] in ids):
#        tiles = data[11].split(';')
#        for tile in tiles:
#          img_name = outdir + '/' + data[2] + '_' + tile + '_' + date[0] + '_' + date[1] + '.' + type
#          if (vis):
#            if (vis_pattern.match(tile)):
#              copy(path + '/snapshot' + data[1] + '/' + tile + '.' + type, img_name)
#          if (nir):
#            if (nir_pattern.match(tile)):
#              copy(path + '/snapshot' + data[1] + '/' + tile + '.' + type, img_name)
#          if (flu):
#            if (flu_pattern.match(tile)):
#              copy(path + '/snapshot' + data[1] + '/' + tile + '.' + type, img_name)

### Main pipeline
def main():
  # Get options
  args = options()
  
  if (args.database):
    db_lookup(args.database, args.outdir, args.type)
  #elif (args.csv):
  #  csv_lookup(args.csv, plant_ids, args.outdir, args.type, args.vis, args.nir, args.flu)
  

if __name__ == '__main__':
  main()
