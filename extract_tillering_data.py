#!/usr/bin/python
import argparse
import sys, os
import sqlite3 as sq
import plantcv as pcv
import math
import numpy as np
import re
import cv2

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Extract and Normalize Tillering data from an SQLite database")
  parser.add_argument("-d", "--database", help="SQLite database file from plantcv.", required=True)
  parser.add_argument("-o", "--outfile", help="Output text file.", required=True)
  parser.add_argument("-p", "--height", help="Height of images in pixels", required=True, type=int)
  parser.add_argument("-t", "--tiller", help="Optional manual input of zoom-corrected tiller width in pixels", required=False, type=int)
  parser.add_argument("-te", "--tillerest",help="number of days that should be used for tiller estimation, requires an integer", required=False, type=int)
  parser.add_argument("-D", "--debug", help="Turn on debugging mode", action="store_true")
  args = parser.parse_args()
  return args

### Dictionary factory for SQLite query results
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

### Top-view center of mass correction
def tv_centroid_correction(area, centroid_height):
  correction_factor = 0.9015 * math.exp(0.0007 * centroid_height)
  area /= correction_factor
  return area

### Zoom correction
def zoom_correction(area, zoom):
  correction_factor = 0.9015 * math.exp(0.0007 * zoom)
  area /= correction_factor
  return area

### Length conversion
def px_to_cm(px, zoom):
  pxcm = (0.000002171 * (zoom ** 2)) + (0.002073 * zoom) + 14.27
  cm = px / pxcm
  return cm

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
  
  # Make Directory For Output Images
  print out
  #if not os.path.exists(tillering_img_path):
  #  os.makedirs()
  
  # Header
  out.write(','.join(map(str, ('plant_id', 'datetime', 'image_path', 'raw_tillering_count', 'raw_tillering_widths', 'zoom_corrected_tiller_widths','manual_input_single_tiller','estimated_single_tiller','new_tiller_count'))) + '\n')
  
  # Replace the row_factory result constructor with a dictionary constructor
  connect.row_factory = dict_factory
  # Change the text output format from unicode to UTF-8
  connect.text_factory=str
  
  # Database handler
  db = connect.cursor()
  db1= connect.cursor()
  db2= connect.cursor()
  t= connect.cursor()
  
  # Retrieve snapshot IDs from the database
  snapshots = []
  column_headers='date_int', 'datetime','barcode', 'frame','image_path', 'raw_tillering_widths', 'zoom_corrected_widths'
  
  # Find first day of dataset (tool works best with multiple days)
  for date in t.execute('select min(datetime) as first from snapshots'):
    firstday=date['first']
  
  #find unique datetimes (would find all angles)
  for row in (db.execute('SELECT DISTINCT(`datetime`) FROM `snapshots` WHERE `camera`="vis_sv"')):
    snapshots.append(row['datetime'])
  if (args.debug):
    print('Found ' + str(len(snapshots)) + ' snapshots')
  
###Average values from first day of experiment to estimate tillering width based on median value of tiller-width values from date-range
  zoom_width_est=[]
  for snaps in snapshots:
    data_db=db1.execute('select * from snapshots inner join tillering_data on snapshots.image_id=tillering_data.image_id inner join analysis_images on snapshots.image_id=analysis_images.image_id where camera="vis_sv" and type="tillers" and datetime=?', (snaps,))
    
    #number of days to use for tiller estimation (if 0 includes first day only)
    tiller_est_days=args.tillerest
    
    date_int=((snaps-firstday)/86400)
    if date_int<=tiller_est_days and args.tiller==None:
      for i, data in enumerate(data_db):
        raw_width = re.sub('[\[\] ]', '', data['raw_tillering_width']).split(',')
        int_raw_width=[int(l) for l in raw_width]
        
        for x in int_raw_width:
          width=px_to_cm(x,data['zoom'])
          zoom_width_est.append(width)
  
  zoom_width_median=np.median(zoom_width_est)
  zoom_width_std=np.std(zoom_width_est)
  print zoom_width_est
  print zoom_width_median
  print zoom_width_std

###Take the width estimation measurement and apply it to the widths to get a better estimation of the number of tillers    
  for snaps in snapshots:
    data_all=db2.execute('select * from snapshots inner join tillering_data on snapshots.image_id=tillering_data.image_id inner join analysis_images on snapshots.image_id=analysis_images.image_id where camera="vis_sv" and type="tillers" and datetime=?', (snaps,))
    average_angles=[]    
    for c, data1 in enumerate(data_all):
      width_all=[]
      tiller_count=[]
      datetime=data1['datetime']
      barcode=data1['plant_id']
      img_path=data1['image_path']
      raw_count=data1['raw_tillering_count']
      raw_width_all = re.sub('[\[\] ]', '', data1['raw_tillering_width']).split(',')
      int_raw_width_all=[int(l) for l in raw_width_all]
      
      for x in int_raw_width_all:
        width=px_to_cm(x,data['zoom'])
        width_all.append(width)
      print date_int
      print datetime
      print barcode
      print img_path
      print width_all
      print len(width_all)
      
      #adjust tiller count so that 
      for x in width_all:
        tiller_width_est=zoom_width_median+zoom_width_std
        if x<=(tiller_width_est):
          count=1
          tiller_count.append(count)
        elif x>=(tiller_width_est):
          count=int(x/tiller_width_est)
          tiller_count.append(count)
      #add tiller count to array
      tiller_count_total=sum(tiller_count)
      print tiller_count_total
      #add tiller count to an array so sides can be averaged
      average_angles.append(tiller_count_total)
      
      #change image so that tiller number is written on the image.
      #read in image
      tiller_img=cv2.imread(str(img_path))
      img=np.copy(tiller_img)
      ix,iy,iz=np.shape(img)
      x=ix/10
      y=iy/10
      y1=iy/7
      text=('Raw Tiller Count='+str(raw_count))
      text1=('Normalized Tiller Count='+str(tiller_count_total))

      if args.debug:
        cv2.putText(img,text, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 3,(0,0,255),4)
        cv2.putText(img,text1, (x,y1), cv2.FONT_HERSHEY_SIMPLEX, 3,(0,0,255),4)
        pcv.print_image(img, str(barcode)+'_'+str(datetime) + '_tillering_img.png')
     
      #tiller_img_shape=np.shape(tiller_img)
      #print tiller_img_shape
    
    tiller_angles_averaged=np.mean(average_angles)
    tiller_angles_std=np.std(average_angles)
    

      
        
          

        
     
  
  # Retrieve snapshots and process data
  #for snapshot in snapshots:
  #  sv_image_count = 0
  #  outlier = False
  #  plant_id = ''
  #  tillering_line=0
  #  raw_tillering_count=0
  #  raw_tillering_width=[]
  #  average_tillering_width=0
  #  median_tillering_width=0
  #  std_tillering_width=0
  #  print raw_tillering_width
  #  
    ## Measure plant height
    
    #image_count = 0
    #tillering_line = 0
    #for row in (db.execute('SELECT * FROM `snapshots` INNER JOIN `tillering_data` ON `snapshots`.`image_id` = `tillering_data`.`image_id` WHERE `datetime` = %i' % snapshot)):
    #  tillering_line = row['x_position']
    #  raw_tillering_count += row['raw_tillering_count']
    #  raw_tillering_width += row['height_below_bound']
    #  above_bound_area += zoom_correction(row['above_bound_area'], row['zoom'])
    #  percent_above_bound_area += row['percent_above_bound_area']
    #  below_bound_area += zoom_correction(row['below_bound_area'], row['zoom'])
    #  percent_below_bound_area += row['percent_below_bound_area']
    #
    #  image_count += 1
    #if image_count > 0:
    #  if (args.debug):
    #    print('Snapshot ' + str(snapshot) + ' has boundary data')
    #  height_above_bound /= image_count
    #  height_below_bound /= image_count
    #  above_bound_area /= image_count
    #  percent_above_bound_area /= image_count
    #  below_bound_area /= image_count
    #  percent_below_bound_area /= image_count
    #  # Adjusted center of mass y (height above boundary line to cmy)
    #  centroid_height = (args.height - boundary_line_y) - centroid_y
    #  if centroid_height < 0:
    #    centroid_height = 0
    #  
    #  # Zoom correct length-based traits
    #  centroid_height = px_to_cm(centroid_height, row['zoom'])
    #  perimeter = px_to_cm(perimeter, row['zoom'])
    #  longest_axis = px_to_cm(longest_axis, row['zoom'])
    #  height_above_bound = px_to_cm(height_above_bound, row['zoom'])
    #  height_below_bound = px_to_cm(height_below_bound, row['zoom'])
    #    
    #  #surface_area += tv_centroid_correction(tv_area, centroid_height)
    #  out.write(','.join(map(str, (plant_id, snapshot, sv_area, tv_area, centroid_height, solidity, perimeter, centroid_x, centroid_y, longest_axis,
    #                             height_above_bound, height_below_bound, above_bound_area, percent_above_bound_area, below_bound_area,
    #                             percent_below_bound_area, outlier, boundary_line_y))) + '\n')
    #else:
    #  if (args.debug):
    #    print('Something is wrong, snapshot ' + str(snapshot) + ' has ' + str(sv_image_count) + ' SV images and TV area is ' + str(tv_area))

if __name__ == '__main__':
  main()