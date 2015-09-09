#!/usr/bin/env python
import argparse
import sys, os
import sqlite3 as sq
import plantcv as pcv
import math
from datetime import datetime as dt
import numpy as np
import re
import cv2
#import pandas as pd

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
  #try:
  #  out = open(args.outfile, 'w')
  #except IOError:
  #  print("IO error")
  
  # Make Directory For Output Images
  cwd=os.getcwd()
  i=dt.now()
  timenow=i.strftime('%m-%d-%Y_%H:%M:%S')
  newfolder="slice_figs_and_images_"+(str(timenow))
  tillering_img_path=(str(cwd)+'/tillering_images'+str(timenow)+'/')
  if not os.path.exists(tillering_img_path):
    os.makedirs(tillering_img_path)
  
  # Replace the row_factory result constructor with a dictionary constructor
  connect.row_factory = dict_factory
  # Change the text output format from unicode to UTF-8
  connect.text_factory=str
  
  # Database handler
  db = connect.cursor()
  db1= connect.cursor()
  db2= connect.cursor()
  db3= connect.cursor()
  t= connect.cursor()
  
  #Open file and print headers to file
 
  try:
    filename1=args.outfile
    signal_file1= os.open(filename1,os.O_RDWR|os.O_CREAT)
  except IOError:
    print("IO error")
 
  column_headers='date_int', 'datetime','barcode','image_path_0','image_path_90','image_path_180','image_path_270','estimated_width', 'estimated_width_std','raw_width_0','raw_width_90','raw_width_180','raw_width_270', 'normalize_width_0','normalized_width_90', 'normalized_width_180', 'normalized_width_270','raw_count_0','raw_count_90','raw_count_180','raw_count_270', 'normalized_count_0','normalized_count_90','normalized_count_180','normalized_count_270'  
  header_fin='\t'.join(map(str,column_headers))
  print header_fin
  os.write(signal_file1, header_fin)
  os.write(signal_file1, os.linesep)

  # Retrieve snapshot IDs from the database
  snapshots = []
  
  
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

###Take the width estimation measurement and apply it to the widths to get a better estimation of the number of tillers    
  for snaps in snapshots:

    data_all=db2.execute('select * from snapshots inner join tillering_data on snapshots.image_id=tillering_data.image_id inner join analysis_images on snapshots.image_id=analysis_images.image_id where camera="vis_sv" and type="tillers" and datetime=?', (snaps,)) 
    data_dict={}
    frame_data=[]
    for c, data1 in enumerate(data_all):
      
      date_int=((snaps-firstday)/86400)
      data_dict['date_int']=date_int
      
      datetime=data1['datetime']
      data_dict['datetime']=datetime
      
      barcode=data1['plant_id']
      data_dict['plant_id']=barcode
      
      data_dict['estimated_width_cm']=zoom_width_median
      data_dict['estimated_width_cm_std']=zoom_width_std
      
      frame=data1['frame']
      frame_data.append(frame)
    
    for angles in frame_data:
      data_by_frame=db2.execute('select * from snapshots inner join tillering_data on snapshots.image_id=tillering_data.image_id inner join analysis_images on snapshots.image_id=analysis_images.image_id where camera="vis_sv" and type="tillers" and datetime=? and frame=?', (snaps,angles,)) 

      for i, data2 in enumerate(data_by_frame):
        width_all=[]
        tiller_count=[]
        
        frame=data2['frame']
        img_path=data2['image_path']
        raw_count=data2['raw_tillering_count']
        raw_width_all = re.sub('[\[\] ]', '', data2['raw_tillering_width']).split(',')
        int_raw_width_all=[int(l) for l in raw_width_all]
        
        for x in int_raw_width_all:
          width=px_to_cm(x,data['zoom'])
          width_all.append(width)
        raw_count=len(width_all)
        
        #adjust tiller count so that 
        for x in width_all:
          tiller_width_est=zoom_width_median*1.75
          tiller_none=(float(zoom_width_median/2))
          #print tiller_none
          if x<=tiller_width_est and x>=tiller_none:
            count=1
            tiller_count.append(count)
          elif x<=tiller_none:
            count=0
            tiller_count.append(count)
          elif x>=tiller_width_est:
            count=int(x/tiller_width_est)
            tiller_count.append(count)
        #add tiller count to array
        tiller_count_total=sum(tiller_count)
        
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
      
        cv2.putText(img,text, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 3,(0,0,255),4)
        cv2.putText(img,text1, (x,y1), cv2.FONT_HERSHEY_SIMPLEX, 3,(0,0,255),4)
        name_img=str(tillering_img_path)+str(barcode)+'_'+'Frame_'+str(frame)+'_day'+str(date_int)+'_'+str(datetime) + '_tillering_img.png'
        pcv.print_image(img,name_img)
        
      # Put the data for each barcode into the hash
      if frame==0:
        data_dict['raw_width_0']=int_raw_width_all
        data_dict['raw_count_0']=raw_count
        data_dict['normalized_width_0']=width_all
        data_dict['normalized_count_0']=tiller_count_total
        data_dict['img_path_0']=name_img
        
      elif frame==90:
        data_dict['raw_width_90']=int_raw_width_all
        data_dict['raw_count_90']=raw_count
        data_dict['normalized_width_90']=width_all
        data_dict['normalized_count_90']=tiller_count_total
        data_dict['img_path_90']=name_img

      elif frame==180:
        data_dict['raw_width_180']=int_raw_width_all
        data_dict['raw_count_180']=raw_count
        data_dict['normalized_width_180']=width_all
        data_dict['normalized_count_180']=tiller_count_total
        data_dict['img_path_180']=name_img

      elif frame==270:
        data_dict['raw_width_270']=int_raw_width_all
        data_dict['raw_count_270']=raw_count
        data_dict['normalized_width_270']=width_all
        data_dict['normalized_count_270']=tiller_count_total
        data_dict['img_path_270']=name_img
        
    # if all angles don't exist fill in a None value.
    if data_dict.get('raw_width_0')==None:
      data_dict['raw_width_0']=None
      data_dict['raw_count_0']=None
      data_dict['normalized_width_0']=None
      data_dict['normalized_count_0']=None
      data_dict['img_path_0']=None
    if data_dict.get('raw_width_90')==None:
      data_dict['raw_width_90']=None
      data_dict['raw_count_90']=None
      data_dict['normalized_width_90']=None
      data_dict['normalized_count_90']=None
      data_dict['img_path_90']=None
    if data_dict.get('raw_width_180')==None:
      data_dict['raw_width_180']=None
      data_dict['raw_count_180']=None
      data_dict['normalized_width_180']=None
      data_dict['normalized_count_180']=None
      data_dict['img_path_180']=None
    if data_dict.get('raw_width_270')==None:
      data_dict['raw_width_270']=None
      data_dict['raw_count_270']=None
      data_dict['normalized_width_270']=None
      data_dict['normalized_count_270']=None
      data_dict['img_path_270']=None
    
    #print data_dict
    # Write out data to file
    list_data=data_dict['date_int'], data_dict['datetime'], data_dict['plant_id'], data_dict['img_path_0'], data_dict['img_path_90'], data_dict['img_path_180'], data_dict['img_path_270'], data_dict['estimated_width_cm'], data_dict['estimated_width_cm_std'], data_dict['raw_width_0'], data_dict['raw_width_90'], data_dict['raw_width_180'], data_dict['raw_width_270'], data_dict['normalized_width_0'], data_dict['normalized_width_90'], data_dict['normalized_width_180'], data_dict['normalized_width_270'], data_dict['raw_count_0'], data_dict['raw_count_90'], data_dict['raw_count_180'], data_dict['raw_count_270'], data_dict['normalized_count_0'], data_dict['normalized_count_90'], data_dict['normalized_count_180'], data_dict['normalized_count_270']
    data_line='\t'.join(map(str,list_data))
    print data_line
    os.write(signal_file1, data_line)
    os.write(signal_file1, os.linesep)
    
  os.close(signal_file1)

if __name__ == '__main__':
  main()
