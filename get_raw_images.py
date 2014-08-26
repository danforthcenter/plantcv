#!/usr/bin/python
import argparse
import sys, os
import sqlite3 as sq
import plantcv as pcv
from shutil import copy

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
  parser.add_argument("-d", "--database", help="SQLite database file from plantcv.", required=True)
  parser.add_argument("-f", "--file", help="File containing plant IDs.", required=True)
  parser.add_argument("-o", "--outdir", help="Output directory.", required=True)
  parser.add_argument("--vis", help="Images are class VIS.", action='store_true')
  parser.add_argument("--nir", help="Images are class NIR.", action='store_true')
  parser.add_argument("--flu", help="Images are class FLU.", action='store_true')
  args = parser.parse_args()
  return args

### Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

### Main pipeline
def main():
  # Get options
  args = options()
  
  # Does the database exist?
  if not os.path.exists(args.database):
    pcv.fatal_error("The database file " + str(args.database) + " does not exist");
  
  # Open a connection
  try:
    connect=sq.connect(args.database)
  except sq.Error, e:
    print("Error %s:" % e.args[0])
    
  # Replace the row_factory result constructor with a dictionary constructor
  connect.row_factory = dict_factory
  # Change the text output format from unicode to UTF-8
  connect.text_factory=str
  
  # Database handler
  db = connect.cursor()
  
  # Open input file
  with open(args.file) as plant_ids:
    for plant_id in plant_ids:
      for row in (db.execute('SELECT * FROM `snapshots` WHERE `plant_id` = "%s"' % plant_id.rstrip('\n'))):
        if (args.vis):
          if (row['camera'] == 'vis_sv' or row['camera'] == 'vis_tv'):
            copy(row['image_path'], args.outdir + '/' + row['plant_id'] + '_' + row['camera'] + '_z' + str(row['zoom']) + '_' + str(row['frame']) + '_' + str(row['datetime']) + '.png')
            #print(args.outdir + '/' + row['plant_id'])
        elif (args.nir):
          if (row['camera'] == 'nir_sv' or row['camera'] == 'nir_tv'):
            copy(row['image_path'], args.outdir)
        elif (args.flu):
          if (row['camera'] == 'flu_tv'):
            images = row['image_path'].split(',')
            for image in images:
              copy(image, args.outdir)

if __name__ == '__main__':
  main()