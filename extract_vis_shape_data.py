#!/usr/bin/python
import argparse
import sys, os
import sqlite3 as sq
import plantcv as pcv

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
  parser.add_argument("-d", "--database", help="SQLite database file from plantcv.", required=True)
  parser.add_argument("-o", "--outfile", help="Output text file.", required=True)
  args = parser.parse_args()
  return args

### Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

### Top-view center of mass correction
def tv_centroid_correction(centroid_y):
  return centroid_y

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
  
  # Retrieve snapshot IDs from the database
  snapshots = []
  for row in (db.execute('SELECT DISTINCT(`snapshot_id`) FROM `snapshots`')):
    snapshots.append(row['snapshot_id'])
  
  # Retrieve snapshots and process data
  for snapshot in snapshots:
    image_count = 0
    centroid_y = 0
    for row in (db.execute('SELECT * FROM `snapshots` INNER JOIN `vis_shapes` ON `snapshots`.`image_id` = `vis_shapes`.`image_id` WHERE `snapshot_id` = %i' % snapshot)):
      if row['in_bounds'] == 'True':
        image_count += 1
        centroid_y += row['centroid_y']
    if image_count > 0:
      centroid_y_ave = centroid_y / image_count
      print('\t'.join(map(str,(row['image_path'], centroid_y_ave))))
  
   ## Measure plant height
  #for snapshot in snapshots:
  #  height = 0
  #  image_count = 0
  #  for row in (db.execute('SELECT * FROM `snapshots` INNER JOIN `boundary_data` ON `snapshots`.`image_id` = `boundary_data`.`image_id` WHERE `snapshot_id` = %i' % snapshot)):
  #    print(row['plant_id'])
    

if __name__ == '__main__':
  main()