#!/usr/bin/python
import argparse
import sys, os
import sqlite3 as sq
import plantcv as pcv

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Extract VIS color data from an SQLite database")
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
  
  # Open output file
  try:
    out = open(args.outfile, 'w')
  except IOError:
    print("IO error")
    
  # Replace the row_factory result constructor with a dictionary constructor
  #connect.row_factory = dict_factory
  # Change the text output format from unicode to UTF-8
  connect.text_factory=str
  
  # Database handler
  db = connect.cursor()
  
  # Retrieve snapshots and process data
  db.execute('SELECT * FROM `snapshots` INNER JOIN `vis_colors` ON `snapshots`.`image_id` = `vis_colors`.`image_id`')
  names = list(map(lambda x: x[0], db.description))
  # Remove color channel names (hard-coded 9 channels)
  channels = []
  for i in range(1, 10):
    channels.append(names.pop())
  bins = 0
  channels.reverse()
  for row in db.fetchall():
    if bins == 0:
      bins = row[-10]
      for channel in channels:
        for b in range(0,bins):
          names.append(str(channel) + str(b))
      out.write(','.join(map(str,names)) + '\n')
    out.write(','.join(map(str, row)) + '\n')
  

if __name__ == '__main__':
  main()
