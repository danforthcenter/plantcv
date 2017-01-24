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

def color_export(sqlitedb,outdir,signal_type='vis', camera_label='vis_sv',channels='rgb',average_angles='on'):
  #sqlitedb = sqlite database to query (path to db)
  #outdir = path to outdirectory
  #camera_type='vis','nir' or 'fluor'
  #camera_label = either 'vis_tv','vis_sv',or 'fluor_tv'
  #channels = signal,'rgb' 'lab' or 'hsv'
  #average_angles = if on side angles for a plant are averaged
  #spacer = either 'on' or 'off', adds a white line between day breaks
  #makefig = either 'yes' or 'no', adds labels to days and a title
  #cat_treat = either 'yes','no',or 'all', if yes concatenates figures by treatment, if all all slice plots are put together, this only works properly if plots are roughly similar in size
  
  # Makes folder in specified directory for the slice figures and images
  i=datetime.now()
  timenow=i.strftime('%m-%d-%Y_%H:%M:%S')
  newfolder="slice_figs_and_images_"+(str(timenow))
  
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
  for date in c.execute('select min(datetime) as first from snapshots'):
    firstday=date['first']
  
  # Query database to get plant ids
  if signal_type=='vis':
    signal=c.execute('select * from snapshots inner join vis_colors on snapshots.image_id =vis_colors.image_id order by plant_id asc')
  elif signal_type=='nir':
    signal=c.execute('select * from snapshots inner join nir_signal on snapshots.image_id =nir_signal.image_id order by plant_id asc')
  elif signal_type=='fluor':
    signal=c.execute('select * from snapshots inner join flu_signal on snapshots.image_id =flu_signal.image_id order by plant_id asc')
  
  barcode_array=[]
  group_id=[]
  just_id=[]
  ch1_total_array=[]
  ch2_total_array=[]
  ch3_total_array=[]
  
  # find unique ids so that angles can be averaged
  
  for i, group in enumerate(signal):
    bins=int(group['bins'])
    plant_id=group['plant_id']
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
  else:
    channel1='signal'
    channel2='signal'
    channel3='signal'
  
  # Make first lines of empty arrays the header titles
  
  ch1_headers=[]
  ch2_headers=[]
  ch3_headers=[]
  bin_nums=np.transpose((np.arange(0,bins, step=1)))
  ch1_headers.append('day')
  ch2_headers.append('day')
  ch3_headers.append('day')
  ch1_headers.append('barcode')
  ch2_headers.append('barcode')
  ch3_headers.append('barcode')
  ch1_headers.append('frame')
  ch2_headers.append('frame')
  ch3_headers.append('frame')
  ch1_headers.append('date_time')
  ch2_headers.append('date_time')
  ch3_headers.append('date_time')

        
  if signal_type=='vis':
    for i,bn in enumerate(bin_nums):
      b=(str(channel1)+"_bin_"+str(bn))
      g=(str(channel2)+"_bin_"+str(bn))
      r=(str(channel3)+"_bin_"+str(bn))
      ch1_headers.append(b)
      ch2_headers.append(g)
      ch3_headers.append(r)
  elif signal_type=='nir':
    for i,bn in enumerate(bin_nums):
      b="nir_bin_"+str(bn)
      ch1_headers.append(b)
  elif signal_type=='fluor':
    for i,bn in enumerate(bin_nums):
      b="fluor_bin_"+str(bn)
      ch1_headers.append(b)
  
  # Initialize the txt files which are compatible with imput into R
  
  if signal_type=='vis':
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
    if signal_type=='vis':
      database=h.execute('select * from snapshots inner join vis_colors on snapshots.image_id=vis_colors.image_id where plant_id= ? and camera=? order by datetime asc', (barcode_label,camera_label,))
    elif signal_type=='nir':
      database=h.execute('select * from snapshots inner join nir_signal on snapshots.image_id=nir_signal.image_id where plant_id= ? and camera=? order by datetime asc', (barcode_label,camera_label,))
    elif signal_type=='flu':
      database=h.execute('select * from snapshots inner join flu_signal on snapshots.image_id=flu_signal.image_id where plant_id= ? and camera=? order by datetime asc', (barcode_label,camera_label,))
    
    for i,t in enumerate(database):
      date=(t['datetime'])          
      time_array.append(date,)
    unique_time=np.unique(time_array)
  
  # For each unique time grab the histogram data and either use each individual angle or averaged angles
    
    for time in unique_time:
      dim1_all=[]
      dim2_all=[]
      dim3_all=[]
      date_int=((time-firstday)/86400) 
      if signal_type=='vis':
        database_time=h.execute('select * from snapshots inner join vis_colors on snapshots.image_id=vis_colors.image_id inner join vis_shapes on snapshots.image_id=vis_shapes.image_id where plant_id=? and camera=? and datetime=?',(barcode_label, camera_label,str(time),))
      elif signal_type=='nir':
        database_time=h.execute('select * from snapshots inner join nir_signal on snapshots.image_id=nir_signal.image_id where plant_id=? and camera=? and datetime=?',(barcode_label, camera_label,str(time),))
      elif signal_type=='flu':
        database_time=h.execute('select * from snapshots inner join flu_signal on snapshots.image_id=flu_signal.image_id where plant_id=? and camera=? and datetime=?',(barcode_label, camera_label,str(time),))
      for i, data in enumerate(database_time):
        dim1=np.matrix(data[channel1])
        dim2=np.matrix(data[channel2])
        dim3=np.matrix(data[channel3])
        norm_area=data['area']        
              
        dim1_norm1=[]
        dim2_norm1=[]
        dim3_norm1=[]
        
        for i,x in enumerate(dim1):
          norm_x=(x/norm_area)*100
          dim1_norm1.append(norm_x)
        for i,x in enumerate(dim2):
          norm_x=(x/norm_area)*100
          dim2_norm1.append(norm_x)         
        for i,x in enumerate(dim3):
          norm_x=(x/norm_area)*100
          dim3_norm1.append(norm_x)

        
        dim1_all.append(dim1_norm1)
        dim2_all.append(dim2_norm1)
        dim3_all.append(dim3_norm1)
        
        if average_angles=='off':
          ch1=[]
          ch2=[]
          ch3=[]
          frame=data['frame']
          date_time=data['datetime']
          
          ch1.append(date_int)
          ch2.append(date_int)
          ch3.append(date_int)
          ch1.append(barcode_label)
          ch2.append(barcode_label)
          ch3.append(barcode_label)
          ch1.append(frame)
          ch2.append(frame)
          ch3.append(frame)
          ch1.append(date_time)
          ch2.append(date_time)
          ch3.append(date_time)
          
          dim1_t=np.transpose(dim1_norm1)
          dim2_t=np.transpose(dim2_norm1)
          dim3_t=np.transpose(dim3_norm1)
          
          for i,c in enumerate(dim1_t):
            b=float(c)
            ch1.append(b)
          for i,c in enumerate(dim2_t):
            b=float(c)
            ch2.append(b)
          for i,c in enumerate(dim3_t):
            b=float(c)
            ch3.append(b)
          
          ch1_total_array.append(ch1)
          ch2_total_array.append(ch2)
          ch3_total_array.append(ch3)
          
         
          ch1_join=','.join(map(str,ch1))
          ch2_join=','.join(map(str,ch2))
          ch3_join=','.join(map(str,ch3))
          os.write(signal_file1, ch1_join)
          os.write(signal_file2, ch2_join)
          os.write(signal_file3, ch3_join)
          os.write(signal_file1, os.linesep)
          os.write(signal_file2, os.linesep)
          os.write(signal_file3, os.linesep)
                
      if average_angles=='on':
        ch1=[]
        ch2=[]
        ch3=[]
        frame='all_avg'
        date_time=data['datetime']
        
        ch1_avg=np.transpose(np.average(dim1_all,axis=0))
        ch2_avg=np.transpose(np.average(dim2_all,axis=0))
        ch3_avg=np.transpose(np.average(dim3_all,axis=0))

        ch1.append(date_int)
        ch2.append(date_int)
        ch3.append(date_int)
        ch1.append(barcode_label)
        ch2.append(barcode_label)
        ch3.append(barcode_label)
        ch1.append(frame)
        ch2.append(frame)
        ch3.append(frame)
        ch1.append(date_time)
        ch2.append(date_time)
        ch3.append(date_time)
          
        for i,c in enumerate(ch1_avg):
          b=float(c)
          ch1.append(b)
        for i,c in enumerate(ch2_avg):
          b=float(c)
          ch2.append(b)
        for i,c in enumerate(ch3_avg):
          b=float(c)
          ch3.append(b)
                  
        ch1_total_array.append(ch1)
        ch2_total_array.append(ch2)
        ch3_total_array.append(ch3)
        
        ch1_join=','.join(map(str,ch1))
        ch2_join=','.join(map(str,ch2))
        ch3_join=','.join(map(str,ch3))
        os.write(signal_file1, ch1_join)
        os.write(signal_file2, ch2_join)
        os.write(signal_file3, ch3_join)
        os.write(signal_file1, os.linesep)
        os.write(signal_file2, os.linesep)
        os.write(signal_file3, os.linesep)
  
  os.close(signal_file1)
  os.close(signal_file2)
  os.close(signal_file3)     
  
  return outdir_name

### Main pipeline
def main():
  # Get options
  args = options()

  img_file_dir =color_export(args.database,args.outdir,'vis','vis_sv','hsv','on')
  #img_file_dir='/home/mgehan/LemnaTec/out_folder/slice_figs_and_images_04-21-2014_16:59:07/'
  #avr.cat_fig(args.outdir,img_file_dir)

if __name__ == '__main__':
  main()
        