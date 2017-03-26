#!/usr/bin/env python
from __future__ import division
import sys, traceback
import os
import re
import sqlite3 as sq
import distutils.core
import cv2
import numpy as np
import argparse
import string
from datetime import datetime

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Sitching and Ordering Image Slices")
  parser.add_argument("-d", "--database", help="Database to query.", required=True)
  parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
  #parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
  args = parser.parse_args()
  return args

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def color_export(sqlitedb,outdir,signal_type='vis', camera='SV',channels='rgb',average_angles='on'):
  #sqlitedb = sqlite database to query (path to db)
  #outdir = path to outdirectory
  #signal_type='VIS','NIR' or 'FLU'
  #camera = either 'SV', or 'TV'
  #channels = signal,'rgb', 'lab','hsv','nir', or 'flu'
  #average_angles = if on side angles for a plant are averaged
  #spacer = either 'on' or 'off', adds a white line between day breaks
  #makefig = either 'yes' or 'no', adds labels to days and a title
  #cat_treat = either 'yes','no',or 'all', if yes concatenates figures by treatment, if all all slice plots are put together, this only works properly if plots are roughly similar in size
  
  # Makes folder in specified directory for the slice figures and images
  i=datetime.now()
  timenow=i.strftime('%m-%d-%Y_%H:%M:%S')
  newfolder="color_data_"+(str(timenow))
   
  os.mkdir((str(outdir)+newfolder))
  outdir_name=str(outdir)+str(newfolder)+"/"
  
  # Connect to sqlite database
  connect=sq.connect(sqlitedb)
  connect.row_factory = dict_factory
  connect.text_factory=str
  c = connect.cursor()
  h = connect.cursor()
  m = connect.cursor()
  
  # Find first day of experiment, this is needed to calculate the days in integer values instead of epoch time
  for date in c.execute('select min(timestamp) as first from metadata'):
    firstday=date['first']
  # Query database to get plant ids
  signal=c.execute('select * from metadata inner join signal on metadata.image_id =signal.image_id where camera=? and imgtype=? order by plantbarcode asc',(camera,signal_type,))
  
  barcode_array=[]
  group_id=[]
  just_id=[]
  
  # find unique ids so that angles can be averaged
  
  for i, group in enumerate(signal):
    bins=int(group['bin-number'])
    plant_id=group['plantbarcode']
    barcode_array.append(plant_id,)
  barcode_unique=np.unique(barcode_array)
  
  # slices can be made from color histogram data or from fluor/nir signal histogram data stored in the database
  if channels=='rgb':
    channel1='blue'
    channel2='green'
    channel3='red'
  elif channels=='lab':
    channel1='lightness'
    channel2='green-magenta'
    channel3='blue-yellow'
  elif channels=='hsv':
    channel1='hue'
    channel2='saturation'
    channel3='value'
  elif channels=='nir':
    channel1='nir'
    channel2='nir'
    channel3='nir'
  else:
    channel1='flu'
    channel2='flu'
    channel3='flu'
  
  # Make first lines of empty arrays the header titles
  
  ch1_headers=[]
  ch2_headers=[]
  ch3_headers=[]
  bin_nums=np.transpose((np.arange(0,bins, step=1)))
  ch1_headers.append('barcode')
  ch2_headers.append('barcode')
  ch3_headers.append('barcode')
  ch1_headers.append('frame')
  ch2_headers.append('frame')
  ch3_headers.append('frame')
  ch1_headers.append('date_time')
  ch2_headers.append('date_time')
  ch3_headers.append('date_time')
         
  if signal_type=='VIS':
    for i,bn in enumerate(bin_nums):
      b=(str(channel1)+"_bin_"+str(bn))
      g=(str(channel2)+"_bin_"+str(bn))
      r=(str(channel3)+"_bin_"+str(bn))
      ch1_headers.append(b)
      ch2_headers.append(g)
      ch3_headers.append(r)
  elif signal_type=='NIR':
    for i,bn in enumerate(bin_nums):
      b="nir_bin_"+str(bn)
      ch1_headers.append(b)
  elif signal_type=='FLU':
    for i,bn in enumerate(bin_nums):
      b="fluor_bin_"+str(bn)
      ch1_headers.append(b)
  
  # Initialize the txt files which are compatible with input into R
  
  if signal_type=='VIS':
    header1_fin=','.join(map(str,ch1_headers))
    header2_fin=','.join(map(str,ch2_headers))
    header3_fin=','.join(map(str,ch3_headers))
    filename1=str(outdir)+newfolder+"/"+str(signal_type)+"_signal_"+str(channel1)+"_"+str(timenow)+".txt"
    filename2=str(outdir)+newfolder+"/"+str(signal_type)+"_signal_"+str(channel2)+"_"+str(timenow)+".txt"
    filename3=str(outdir)+newfolder+"/"+str(signal_type)+"_signal_"+str(channel3)+"_"+str(timenow)+".txt"
    signal_file1= os.open(filename1,os.O_RDWR|os.O_CREAT)
    signal_file2= os.open(filename2,os.O_RDWR|os.O_CREAT)
    signal_file3= os.open(filename3,os.O_RDWR|os.O_CREAT)
    os.write(signal_file1, header1_fin)
    os.write(signal_file2, header2_fin)
    os.write(signal_file3, header3_fin)
    os.write(signal_file1, os.linesep)
    os.write(signal_file2, os.linesep)
    os.write(signal_file3, os.linesep)
  else:
    header1_fin=','.join(map(str,ch1_headers))
    filename1=str(outdir)+newfolder+"/"+str(signal_type)+"_signal_"+str(channel1)+"_"+str(timenow)+".txt"
    signal_file1= os.open(filename1,os.O_RDWR|os.O_CREAT)
    os.write(signal_file1, header1_fin)
    os.write(signal_file1, os.linesep)
  
  # For each plant id find the unique timestamp, this will be used to group snapshot angles
  
  for barcode_label in barcode_unique: 
    time_array=[]
    database=h.execute('select * from metadata inner join signal on metadata.image_id=signal.image_id where plantbarcode= ? and imgtype=? and camera=? order by timestamp asc', (barcode_label,signal_type,camera,))
    
    for i,t in enumerate(database):
      date=(t['timestamp'])
      time_array.append(date,)
    unique_time=np.unique(time_array)
  
  # For each unique time grab the histogram data and either use each individual angle or averaged angles
    
    for time in unique_time:
      dim1_all=[]
      database_time1=h.execute('select * from metadata inner join signal on metadata.image_id=signal.image_id inner join features on metadata.image_id=features.image_id where plantbarcode=? and imgtype=? and camera=? and timestamp=? and channel_name=?',(barcode_label, signal_type,camera,str(time),channel1,))
      for i, data in enumerate(database_time1):
        dim1=np.matrix(data['values'])
        norm_area=float(data['area'])
        dim1_norm1=[]
                
        dim1_norm1=(dim1/norm_area)*100 
        dim1_all.append(dim1_norm1)
                
        if average_angles=='off':
          ch1=[]
          frame=data['frame']
          date_time=data['timestamp']
          
          ch1.append(barcode_label)
          ch1.append(frame)
          ch1.append(date_time)
          
          dim1_t=np.transpose(dim1_norm1)
          
          for i,c in enumerate(dim1_t):
            b=float(c)
            ch1.append(b)
                  
          ch1_join=','.join(map(str,ch1))
          os.write(signal_file1, ch1_join)
          os.write(signal_file1, os.linesep)
      if average_angles=='on':
        ch1=[]
        frame='all_avg'
        date_time=data['timestamp']
        
        ix,iy,iz=np.shape(dim1_all)
        if ix==4:
          ch1_avg=np.transpose(np.average(dim1_all,axis=0))
                           
          ch1.append(barcode_label)
          ch1.append(frame)
          ch1.append(date_time)
        
          for i,c in enumerate(ch1_avg):
            b=float(c)
            ch1.append(b)
            
          ch1_join=','.join(map(str,ch1))
          os.write(signal_file1, ch1_join)
          os.write(signal_file1, os.linesep)
          
  for barcode_label in barcode_unique: 
    time_array=[]
    database=h.execute('select * from metadata inner join signal on metadata.image_id=signal.image_id where plantbarcode= ? and imgtype=? and camera=? order by timestamp asc', (barcode_label,signal_type,camera,))
    
    for i,t in enumerate(database):
      date=(t['timestamp'])
      time_array.append(date,)
    unique_time=np.unique(time_array)
  
  # For each unique time grab the histogram data and either use each individual angle or averaged angles
    for time in unique_time:
      dim2_all=[]
      database_time2=h.execute('select * from metadata inner join signal on metadata.image_id=signal.image_id inner join features on metadata.image_id=features.image_id where plantbarcode=? and imgtype=? and camera=? and timestamp=? and channel_name=?',(barcode_label, signal_type,camera,str(time),channel2,))
      for i, data in enumerate(database_time2):
        dim2=np.matrix(data['values'])
        norm_area=float(data['area'])
        
        dim2_norm1=[]
        
        dim2_norm1=(dim2/norm_area)*100 
        dim2_all.append(dim2_norm1)
                          
        if average_angles=='off':
          ch2=[]
          frame=data['frame']
          date_time=data['timestamp']
          
          ch2.append(barcode_label)
          ch2.append(frame)
          ch2.append(date_time)
          
          dim2_t=np.transpose(dim2_norm1)
          
          for i,c in enumerate(dim2_t):
            b=float(c)
            ch2.append(b)
                  
          ch2_join=','.join(map(str,ch2))
          os.write(signal_file2, ch2_join)
          os.write(signal_file2, os.linesep)
      if average_angles=='on':
        ch2=[]
        frame='all_avg'
        date_time=data['timestamp']
        
        ix,iy,iz=np.shape(dim2_all)
        
        if ix==4:
          ch2_avg=np.transpose(np.average(dim2_all,axis=0))
                           
          ch2.append(barcode_label)
          ch2.append(frame)
          ch2.append(date_time)
        
          for i,c in enumerate(ch2_avg):
            b=float(c)
            ch2.append(b)
            
          ch2_join=','.join(map(str,ch2))
          os.write(signal_file2, ch2_join)
          os.write(signal_file2, os.linesep)
  
  for barcode_label in barcode_unique: 
    time_array=[]
    database=h.execute('select * from metadata inner join signal on metadata.image_id=signal.image_id where plantbarcode= ? and imgtype=? and camera=? order by timestamp asc', (barcode_label,signal_type,camera,))
    
    for i,t in enumerate(database):
      date=(t['timestamp'])
      time_array.append(date,)
    unique_time=np.unique(time_array)
    
    for time in unique_time:
      dim3_all=[]
      database_time3=h.execute('select * from metadata inner join signal on metadata.image_id=signal.image_id inner join features on metadata.image_id=features.image_id where plantbarcode=? and imgtype=? and camera=? and timestamp=? and channel_name=?',(barcode_label, signal_type,camera,str(time),channel3,))
      for i, data in enumerate(database_time3):
        dim3=np.matrix(data['values'])
        norm_area=float(data['area'])        
              
        dim3_norm1=[]
        
        dim3_norm1=(dim3/norm_area)*100 
        dim3_all.append(dim3_norm1)
          
        if average_angles=='off':
          ch3=[]
          frame=data['frame']
          date_time=data['timestamp']
          
          ch3.append(barcode_label)
          ch3.append(frame)
          ch3.append(date_time)
          
          dim3_t=np.transpose(dim3_norm1)
          
          for i,c in enumerate(dim3_t):
            b=float(c)
            ch3.append(b)
                  
          ch3_join=','.join(map(str,ch3))
          os.write(signal_file3, ch3_join)
          os.write(signal_file3, os.linesep)
      if average_angles=='on':
        ch3=[]
        frame='all_avg'
        date_time=data['timestamp']
        
        ix,iy,iz=np.shape(dim3_all)
        
        if ix==2:
          ch3_avg=np.transpose(np.average(dim3_all,axis=0))
                           
          ch3.append(barcode_label)
          ch3.append(frame)
          ch3.append(date_time)
        
          for i,c in enumerate(ch3_avg):
            b=float(c)
            ch3.append(b)
            
          ch3_join=','.join(map(str,ch3))
          os.write(signal_file3, ch3_join)
          os.write(signal_file3, os.linesep)        

  os.close(signal_file1)
  os.close(signal_file2)
  os.close(signal_file3)     
  
  return outdir_name

### Main pipeline
def main():
  # Get options
  args = options()

  img_file_dir =color_export(args.database,args.outdir,'VIS','SV','hsv','on')


if __name__ == '__main__':
  main()
        