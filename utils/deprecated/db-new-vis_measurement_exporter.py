#!/usr/bin/python
import argparse
import sys, os
import sqlite3 as sq
import math

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Extract VIS object shape data from an SQLite database")
  parser.add_argument("-d", "--database", help="SQLite database file from plantcv.", required=True)
  parser.add_argument("-o", "--outfile", help="Output text file.", required=True)
  #parser.add_argument("-p", "--height", help="Height of images in pixels", required=True, type=int)
  parser.add_argument("-D", "--debug", help="Turn on debugging mode", action="store_true")
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
    raise("The database file " + str(args.database) + " does not exist");
  
  # Open a connection
  try:
    connect=sq.connect(args.database)
  except sq.Error, e:
    print("Error %s:" % e.args[0])
  
  # Open output file
  try:
    out=open(args.outfile, 'w')
  except IOError:
    print("IO error")
  
  # Replace the row_factory result constructor with a dictionary constructor
  connect.row_factory = dict_factory
  # Change the text output format from unicode to UTF-8
  connect.text_factory=str
  
  # Database handler
  db = connect.cursor()
  
  # Get database schema
  #for row in (db.execute("SELECT * FROM `sqlite_master` WHERE type='table' AND name='metadata'")):
  #  print(row)
  
  # Header
  #out.write(','.join(map(str, ('plant_id', 'datetime', 'sv_zoom', 'tv_zoom', 'sv0_area', 'sv90_area', 'sv180_area', 'sv270_area', 'tv_area', 'solidity', 'perimeter', 'centroid_x', 'centroid_y',
  out.write(','.join(map(str, ('plant_id', 'datetime', 'sv_zoom', 'tv_zoom', 'sv0_area', 'sv90_area', 'sv180_area','sv270_area','tv_area', 'solidity', 'perimeter', 'centroid_x', 'centroid_y',
	                                 'longest_axis', 'extent_x', 'extent_y', 'height_above_bound', 'height_below_bound',
                                   'percent_above_bound_area', 'percent_below_bound_area', 'outlier', 'boundary_line'))) + '\n')
  
  # Retrieve snapshot IDs from the database
  snapshots = []
  for row in (db.execute('SELECT DISTINCT(`timestamp`) FROM `metadata` WHERE `imgtype` = "VIS"')):
    snapshots.append(row['timestamp'])
  if (args.debug):
    print('Found ' + str(len(snapshots)) + ' snapshots')
  # Retrieve snapshots and process data
  for snapshot in snapshots:
    sv_image_count = 0
    outlier = False
    plant_id = ''
    tv_area = 0
    sv0_area = 0
    sv90_area = 0
    sv180_area = 0
    sv270_area = 0
    solidity = 0
    perimeter = 0
    centroid_x = 0
    centroid_y = 0
    longest_axis = 0
    height_above_bound = 0
    height_below_bound = 0
    #above_bound_area = 0
    percent_above_bound_area = 0
    #below_bound_area = 0
    percent_below_bound_area = 0
    extent_x = 0
    extent_y = 0
    sv_zoom = 0
    tv_zoom = 0
    boundary_line_y = 0
    
    for row in (db.execute('SELECT * FROM `metadata` NATURAL JOIN `features` WHERE `timestamp` = "%s"' % snapshot)):
      plant_id = row['plantbarcode']
      if row['in_bounds'] == 'False':
        outlier = True
      if row['imgtype'] == 'VIS' and row['camera'] == 'SV':
        sv_zoom = row['zoom']
        sv_image_count += 1
        boundary_line_y = row['y-position']
        if row['frame'] =='0':
          sv0_area = float(row['area'])
        elif row['frame'] =='90':
          sv90_area = float(row['area'])
        elif row['frame'] =='180':
          sv180_area = float(row['area'])
        elif row['frame'] =='270':
          sv270_area = float(row['area'])
        solidity += float(row['solidity'])
        perimeter += float(row['perimeter'])
        centroid_x += float(row['center-of-mass-x'])
        centroid_y += float(row['center-of-mass-y'])
        longest_axis += int(row['longest_axis'])
        extent_x += int(row['width'])
        extent_y += int(row['height'])
        height_above_bound += int(row['height_above_bound'])
        height_below_bound += int(row['height_below_bound'])
        percent_above_bound_area += float(row['percent_above_bound_area'])
        percent_below_bound_area += float(row['percent_below_bound_area'])
      elif row['imgtype'] == 'VIS' and row['camera'] == 'TV':
        tv_zoom = row['zoom']
        tv_area = int(float(row['area']))
    if sv_image_count == 4 and tv_area > 0:
      if (args.debug):
        print('Snapshot ' + str(snapshot) + ' has 5 images')
      solidity /= sv_image_count
      perimeter /= sv_image_count
      centroid_x /= sv_image_count
      centroid_y /= sv_image_count
      longest_axis /= sv_image_count
      extent_x /= sv_image_count
      extent_y /= sv_image_count
      height_above_bound /= sv_image_count
      height_below_bound /= sv_image_count
      percent_above_bound_area /= sv_image_count
      percent_below_bound_area /= sv_image_count
      #surface_area += tv_centroid_correction(tv_area, centroid_height)
      out.write(','.join(map(str, (plant_id, snapshot, sv_zoom, tv_zoom, sv0_area, sv90_area, sv180_area, sv270_area, tv_area, solidity, perimeter, centroid_x, centroid_y, longest_axis,
                           extent_x, extent_y, height_above_bound, height_below_bound, percent_above_bound_area, percent_below_bound_area, outlier, boundary_line_y))) + '\n')
    else:
      if (args.debug):
        print('Something is wrong, snapshot ' + str(snapshot) + ' has ' + str(sv_image_count) + ' SV images and TV area is ' + str(tv_area))

if __name__ == '__main__':
  main()
