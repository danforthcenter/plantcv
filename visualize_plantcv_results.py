#!/usr/bin/env python

import sys, traceback
import os
import re
import sqlite3 as sq
import distutils.core
import cv2
import numpy as np
import argparse
import string
import plantcv as pcv
from datetime import datetime
import matplotlib
if not os.getenv('DISPLAY'):
  matplotlib.use('SVG')
from matplotlib import pyplot as plt
import pylab as plab
import Image as im

def handle_vis_output(directory,imgtype,outdir,action):
  # directory = path to directory you want to grab images from
  # imgtype = type of output image you want to move or copy (options are rgb_slice, pseudo_on_img, pseudo_on_white, shapes, or, histogram)
  # outdir = where you want the images to go
  # action = either 'copy' or 'move'
  
  if imgtype=='rgb_slice':
    path=str(directory)
    opendir=os.listdir(path)
    for filename in opendir:
      if re.search("rgb_norm_slice\.png$",filename):
        fromDirectory = str(directory)+str(filename)
        toDirectory = str(outdir)+str(filename)
        if action=='copy':
          distutils.file_util.copy_file(fromDirectory, toDirectory)
        elif action=='move':
          distutils.file_util.move_file(fromDirectory, toDirectory)
        else:
          pcv.fatal_error('action' + (str(action) + ' is not move or copy'))
      else:
        pcv.fatal_error("Sorry no "+str(imgtype)+ " images found")
  elif imgtype=='pseudo_on_img':
    path=str(directory)
    opendir=os.listdir(path)
    for filename in opendir:
      if re.search("pseudo_on_img\.png$",filename):
        fromDirectory = str(directory)+str(filename)
        toDirectory = str(outdir)+str(filename)
        if action=='copy':
          distutils.file_util.copy_file(fromDirectory, toDirectory)
        elif action=='move':
          distutils.file_util.move_file(fromDirectory, toDirectory)
        else:
          pcv.fatal_error('action' + (str(action) + ' is not move or copy'))
      else:
        pcv.fatal_error("Sorry no "+str(imgtype)+ " images found")
  elif imgtype=='pseudo_on_white':
    path=str(directory)
    opendir=os.listdir(path)
    for filename in opendir:
      if re.search("pseudo_on_white\.png$",filename):
        fromDirectory = str(directory)+str(filename)
        toDirectory = str(outdir)+str(filename)
        if action=='copy':
          distutils.file_util.copy_file(fromDirectory, toDirectory)
        elif action=='move':
          distutils.file_util.move_file(fromDirectory, toDirectory)
        else:
          pcv.fatal_error('action' + (str(action) + ' is not move or copy'))
      else:
        pcv.fatal_error("Sorry no "+str(imgtype)+ " images found")
  elif imgtype=='shapes':
    path=str(directory)
    opendir=os.listdir(path)
    for filename in opendir:
      if re.search("shapes\.png$",filename):
        fromDirectory = str(directory)+str(filename)
        toDirectory = str(outdir)+str(filename)
        if action=='copy':
          distutils.file_util.copy_file(fromDirectory, toDirectory)
        elif action=='move':
          distutils.file_util.move_file(fromDirectory, toDirectory)
        else:
          pcv.fatal_error('action' + (str(action) + ' is not move or copy'))
      else:
        pcv.fatal_error("Sorry no "+str(imgtype)+ " images found")
  elif imgtype=='histogram':
    path=str(directory)
    opendir=os.listdir(path)
    for filename in opendir:
      if re.search("hist\.png$",filename):
        fromDirectory = str(directory)+str(filename)
        toDirectory = str(outdir)+str(filename)
        if action=='copy':
          distutils.file_util.copy_file(fromDirectory, toDirectory)
        elif action=='move':
          distutils.file_util.move_file(fromDirectory, toDirectory)
        else:
          pcv.fatal_error('action' + (str(action) + ' is not move or copy'))
      else:
        pcv.fatal_error("Sorry no "+str(imgtype)+ " images found")
  else:
    pcv.fatal_error('imgtype' + (str(imgtype) + ' is not rgb_slice, pseudo_on_img, pseudo_on_white, shapes, or, histogram!'))
  

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def visualize_slice(sqlitedb,outdir,signal_type='vis', camera_label='vis_sv',channels='rgb',average_angles='on',spacer='on', write_txt='no',makefig='yes', cat_treat='yes'):
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
  
  if write_txt=='yes':
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
        database_time=h.execute('select * from snapshots inner join vis_colors on snapshots.image_id=vis_colors.image_id where plant_id=? and camera=? and datetime=?',(barcode_label, camera_label,str(time),))
      elif signal_type=='nir':
        database_time=h.execute('select * from snapshots inner join nir_signal on snapshots.image_id=nir_signal.image_id where plant_id=? and camera=? and datetime=?',(barcode_label, camera_label,str(time),))
      elif signal_type=='flu':
        database_time=h.execute('select * from snapshots inner join flu_signal on snapshots.image_id=flu_signal.image_id where plant_id=? and camera=? and datetime=?',(barcode_label, camera_label,str(time),))
      for i, data in enumerate(database_time):
        dim1=np.matrix(data[channel1])
        dim2=np.matrix(data[channel2])
        dim3=np.matrix(data[channel3])
        
        #normalize
        max_dim1=np.amax(dim1)
        max_dim2=np.amax(dim2)
        max_dim3=np.amax(dim3)
        maxval=[max_dim1,max_dim2,max_dim3]
        max_max=np.amax(maxval)
        
        min_dim1=np.amin(dim1)
        min_dim2=np.amin(dim2)
        min_dim3=np.amin(dim3)
        minval=[min_dim1,min_dim2,min_dim3]
        min_min=np.amin(minval)
        
        dim1_norm=((dim1-min_min)/(max_max-min_min))*255
        dim2_norm=((dim2-min_min)/(max_max-min_min))*255
        dim3_norm=((dim3-min_min)/(max_max-min_min))*255
        
        dim1_all.append(dim1_norm)
        dim2_all.append(dim2_norm)
        dim3_all.append(dim3_norm)
        
        if average_angles=='off':
          ch1=[]
          ch2=[]
          ch3=[]
          frame=data['frame']
          
          ch1.append(date_int)
          ch2.append(date_int)
          ch3.append(date_int)
          ch1.append(barcode_label)
          ch2.append(barcode_label)
          ch3.append(barcode_label)
          ch1.append(frame)
          ch2.append(frame)
          ch3.append(frame)
          
          dim1_t=np.transpose(dim1_norm)
          dim2_t=np.transpose(dim2_norm)
          dim3_t=np.transpose(dim3_norm)
          
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
          
          if write_txt=='yes':
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
        
        if write_txt=='yes':
          ch1_join=','.join(map(str,ch1))
          ch2_join=','.join(map(str,ch2))
          ch3_join=','.join(map(str,ch3))
          os.write(signal_file1, ch1_join)
          os.write(signal_file2, ch2_join)
          os.write(signal_file3, ch3_join)
          os.write(signal_file1, os.linesep)
          os.write(signal_file2, os.linesep)
          os.write(signal_file3, os.linesep)
  
  # If you want text including, the day (y-axis) and plant genotype/treatment to be included in a figure, each genotype/treatment is an individual plot

  if makefig=='yes':  
    id_array=[]
    date_array=[]
    sort_ch1= np.array(ch1_total_array)
    sort_ch2= np.array(ch2_total_array)
    sort_ch3= np.array(ch3_total_array)
    
    # Sort the arrays by day and find the unique days
    sorted_ch1 =sort_ch1[sort_ch1[:,0].argsort()]
    sorted_ch2 =sort_ch2[sort_ch2[:,0].argsort()]
    sorted_ch3 =sort_ch3[sort_ch3[:,0].argsort()]
    day_int_array=np.array(sorted_ch1[:,0])
    unique_int_day=np.unique(day_int_array)
    
    unique_int_day1=unique_int_day.astype(int)
    sort_unique_day=np.sort(unique_int_day1,axis=None)
    
    sorted_ch1_final=[]
    sorted_ch2_final=[]
    sorted_ch3_final=[]
    
    for int_sort in sort_unique_day:
      for i, data in enumerate(sorted_ch1):
        if int(data[0])==int_sort:
          sorted_ch1_final.append(sorted_ch1[i])
          sorted_ch2_final.append(sorted_ch2[i])
          sorted_ch3_final.append(sorted_ch3[i])
        
    # Find each unique plant treatment
    for i,data in enumerate(sorted_ch1_final):
      plant_treat=sorted_ch1_final[i][1]
      date_val=sorted_ch1_final[i][0]
      plantgeno=re.match('^([A-Z][a-zA-Z]\d*[A-Z]{2})',plant_treat)
      if plantgeno==None:
        plantgeno_id=plant_treat
        date_array.append(date_val)
        id_array.append(plantgeno_id)
      else:
        span1,span2=plantgeno.span()
        plantgeno_id=plant_treat[span1:span2]
        date_array.append(date_val)
        id_array.append(plantgeno_id)
    unique_id=np.unique(id_array)
    
    # Build the slice figure by adding the data of each geno-treatment to an array
    for name in unique_id:
      ch1_all=[]
      ch2_all=[]
      ch3_all=[]
      ch1_day=[]
      ch2_day=[]
      ch3_day=[]
      ch1_fig=[]
      ch2_fig=[]
      ch3_fig=[]
      ch1_int=[]
      ch2_int=[]
      ch3_int=[]
      for i,n in enumerate(id_array):
        if n==name:
          if signal_type=='vis':
            ch1_line1=np.array(sorted_ch1_final[i][3:])
            ch2_line1=np.array(sorted_ch2_final[i][3:])
            ch3_line1=np.array(sorted_ch3_final[i][3:])
            ch1_line=ch1_line1.astype(float)
            ch2_line=ch2_line1.astype(float)
            ch3_line=ch3_line1.astype(float)
          else:
            ch1_line1=np.array(sorted_ch1_final[i][3:])
            ch1_line=ch1_line1.astype(float)            
            size=np.shape(ch1_line)
            ch2_line1=np.zeros(size)
            ch3_line1=np.zeros(size)
                    
          day=int(date_array[i])
    
          ch1_all.append(ch1_line)
          ch2_all.append(ch2_line)
          ch3_all.append(ch3_line)
          ch1_day.append(day)
          ch2_day.append(day)
          ch3_day.append(day)
      
      # if the spacer is off just stack the data 5 lines high
      if spacer=='off':
        for c,d in enumerate(ch1_all):
          if signal_type=='vis':
            ch1_line=np.array(ch1_all[c])
            ch2_line=np.array(ch2_all[c])
            ch3_line=np.array(ch3_all[c])
          else:
            ch1_line=np.array(ch1_all)
            size=np.shape(ch1_all[c])
            ch2_line=np.zeros(size)
            ch3_line=np.zeros(size)
      
          stacked_1=np.column_stack((ch1_line,ch1_line,ch1_line,ch1_line,ch1_line))
          stacked_2=np.column_stack((ch2_line,ch2_line,ch2_line,ch2_line,ch2_line))
          stacked_3=np.column_stack((ch3_line,ch3_line,ch3_line,ch3_line,ch3_line)) 
          stacked_1t=np.transpose(stacked_1)
          stacked_2t=np.transpose(stacked_2)
          stacked_3t=np.transpose(stacked_3)
          
          ch1_fig.extend(stacked_1t)
          ch2_fig.extend(stacked_2t)
          ch3_fig.extend(stacked_3t)
          
        color_cat=np.dstack((ch1_fig,ch2_fig,ch3_fig))
        fig_name=str(str(outdir)+str(newfolder)+"/"+str(name)+"_"+str(camera_label)+"_"+str(channels)+"_averaging_"+str(average_angles)+"_spacer_"+str(spacer)+"_slice_joined_img.png")
        print fig_name
        pcv.print_image(color_cat,(fig_name))
        
        unique_day=np.unique(ch1_day)
        length_time=[]
        unique_time1=[]
        ypos=[0]
        ypos1=[]
              
        for time in unique_day:
          time1=int(time)+1
          unique_time1.append(time1)
      
        for uday in unique_day:
          length=[]
          for t,d in enumerate(ch1_day):
            if d==uday:
              d1=1
              length.append(d1)
            else:
              d1=0
              length.append(d1)
          sumday=np.sum(length)
          length_time.append(sumday)
          
        for i,length in enumerate(length_time):
            yadd=(length*5)
            ypos.append(yadd)
                
        for i,y in enumerate(ypos):
          if i==0:
            y1=y
            ypos1.append(y1)
          else:
            y1=y+ypos1[i-1]
            ypos1.append(y1)
      
      # If the spacer is on stack the data and add a spacer of blank lines between each day
      if spacer=='on':
        for c,d in enumerate(ch1_all):
          if c==0:
            if signal_type=='vis':
              ch1_line=np.array(ch1_all[c])
              ch2_line=np.array(ch2_all[c])
              ch3_line=np.array(ch3_all[c])
            else:
              ch1_line=np.array(ch1_all)
              size=np.shape(ch1_all[c])
              ch2_line=np.zeros(size)
              ch3_line=np.zeros(size)
        
            stacked_1=np.column_stack((ch1_line,ch1_line,ch1_line,ch1_line,ch1_line))
            stacked_2=np.column_stack((ch2_line,ch2_line,ch2_line,ch2_line,ch2_line))
            stacked_3=np.column_stack((ch3_line,ch3_line,ch3_line,ch3_line,ch3_line)) 
            stacked_1t=np.transpose(stacked_1)
            stacked_2t=np.transpose(stacked_2)
            stacked_3t=np.transpose(stacked_3)
            
            ch1_fig.extend(stacked_1t)
            ch2_fig.extend(stacked_2t)
            ch3_fig.extend(stacked_3t)
            
          elif ch1_day[c]==ch1_day[c-1]:
            if signal_type=='vis':
              ch1_line=np.array(ch1_all[c])
              ch2_line=np.array(ch2_all[c])
              ch3_line=np.array(ch3_all[c])
            else:
              ch1_line=np.array(ch1_all[c])
              size=np.shape(ch1_all[c])
              ch2_line=np.zeros(size)
              ch3_line=np.zeros(size)
           
            stacked_1=np.column_stack((ch1_line,ch1_line,ch1_line,ch1_line,ch1_line))
            stacked_2=np.column_stack((ch2_line,ch2_line,ch2_line,ch2_line,ch2_line))
            stacked_3=np.column_stack((ch3_line,ch3_line,ch3_line,ch3_line,ch3_line)) 
            stacked_1t=np.transpose(stacked_1)
            stacked_2t=np.transpose(stacked_2)
            stacked_3t=np.transpose(stacked_3)
             
            ch1_fig.extend(stacked_1t)
            ch2_fig.extend(stacked_2t)
            ch3_fig.extend(stacked_3t)
            
          elif ch1_day[c]!=ch1_day[c-1]:
            if signal_type=='vis':
              ch1_line=np.array(ch1_all[c])
              ch2_line=np.array(ch2_all[c])
              ch3_line=np.array(ch3_all[c])
            else:
              ch1_line=np.array(ch1_all[c])
              size=np.shape(ch1_all[c])
              ch2_line=np.zeros(size)
              ch3_line=np.zeros(size)
          
            blank_size=np.shape(ch1_all[c])
            blank_line_black=np.zeros(blank_size)
            blank_line=blank_line_black+255
            
            stacked_1=np.column_stack((blank_line,blank_line,blank_line,blank_line,blank_line))
            stacked_2=np.column_stack((blank_line,blank_line,blank_line,blank_line,blank_line))
            stacked_3=np.column_stack((blank_line,blank_line,blank_line,blank_line,blank_line))
            stacked_1t=np.transpose(stacked_1)
            stacked_2t=np.transpose(stacked_2)
            stacked_3t=np.transpose(stacked_3)
            
            ch1_fig.extend(stacked_1t)
            ch2_fig.extend(stacked_2t)
            ch3_fig.extend(stacked_3t)
            
            stacked_4=np.column_stack((ch1_line,ch1_line,ch1_line,ch1_line,ch1_line))
            stacked_5=np.column_stack((ch2_line,ch2_line,ch2_line,ch2_line,ch2_line))
            stacked_6=np.column_stack((ch3_line,ch3_line,ch3_line,ch3_line,ch3_line)) 
            stacked_4t=np.transpose(stacked_4)
            stacked_5t=np.transpose(stacked_5)
            stacked_6t=np.transpose(stacked_6)
            
            ch1_fig.extend(stacked_4t)
            ch2_fig.extend(stacked_5t)
            ch3_fig.extend(stacked_6t)
      
        
        color_cat=np.dstack((ch1_fig,ch2_fig,ch3_fig))
        fig_name=str(str(outdir)+str(newfolder)+"/"+str(name)+"_"+str(camera_label)+"_"+str(channels)+"_averaging_"+str(average_angles)+"_spacer_"+str(spacer)+"_slice_joined_img.png")
        print fig_name
        pcv.print_image(color_cat,(fig_name))
        
        unique_day=np.unique(ch1_day)
                
        length_time=[]
        unique_time1=[]
        ypos=[0]
        ypos1=[]
              
        for time in unique_day:
          time1=int(time)+1
          unique_time1.append(time1)
      
        for uday in unique_day:
          length=[]
          for t,d in enumerate(ch1_day):
            if d==uday:
              d1=1
              length.append(d1)
            else:
              d1=0
              length.append(d1)
          sumday=np.sum(length)
          length_time.append(sumday)
          
        for i,length in enumerate(length_time):
          if i==0:
            yadd=length*5
            ypos.append(yadd)
          else:
            yadd=((length*5)+5)
            ypos.append(yadd)
    
        for i,y in enumerate(ypos):
          if i==0:
            y1=y
            ypos1.append(y1)
          else:
            y1=y+ypos1[i-1]
            ypos1.append(y1)
    
      img1=cv2.imread(str(fig_name), -1)
      if len(np.shape(img1))==3: 
        ch1,ch2,ch3=np.dsplit(img1,3)
      img=np.dstack((ch3,ch2,ch1))
          
      matplotlib.use('SVG')
      plt.imshow(img)
      ax = plt.subplot(111)
      ax.set_ylabel('Days', size=10)
      ax.set_yticks(ypos1)
      ax.set_yticklabels(unique_time1,size=5)
      ax.yaxis.tick_left()
      ax.set_xticks([0,255])
      ax.set_xticklabels([0,255],size=5)
      for t in ax.yaxis.get_ticklines(): t.set_color('white')
      for t in ax.xaxis.get_ticklines(): t.set_color('white')
      for line in ax.get_xticklines() + ax.get_yticklines(): line.set_alpha(0)
      ax.spines['bottom'].set_color('none')
      ax.spines['top'].set_color('none')
      ax.spines['left'].set_color('none')
      ax.spines['right'].set_color('none')
      
      plt.title(str(name))
      fig_name1=(str(outdir)+str(newfolder)+"/"+str(name)+"_"+str(camera_label)+"_"+str(channels)+"_averaging_"+str(average_angles)+"_spacer_"+str(spacer)+"_slice_joined_figure.svg")
      print fig_name1
      plt.savefig(fig_name1, dpi=300, bbox_inches='tight')
      plt.clf()
      
      name_array=[]
      
      fig_name2=str(fig_name)
      name_array=fig_name2.split("/")
      g=re.match('^([A-Z][a-zA-Z]\d*)',name_array[-1])
      gt=re.match('^([A-Z][a-zA-Z]\d*[A-Z]{2})',name_array[-1])
      if g!=None and gt!=None:
        span1,span2=gt.span()
        span3,span4=g.span()
        name1=name_array[-1]
        geno=name1[span3:span4]
        genotreat=name1[span1:span2]
        just_id.append(geno)
        group_id.append((geno,genotreat,ypos1,unique_time1,fig_name))
      elif g==None or gt==None:
        name1=name_array[-1]
        geno=name1
        genotreat=name1
        just_id.append(geno)
        group_id.append(genotreat)
        
  if cat_treat=='yes':
    unique_just_id=np.unique(just_id)
    for unique in unique_just_id:
      group_name=[]
      group_y=[]
      group_time=[]
      group_paths=[]
      for i,data in enumerate(group_id):
        if unique==data[0]:
          group_name.append(data[1])
          group_y.append(data[2])
          group_time.append(data[3])
          group_paths.append(data[4])
      x=len(group_paths)
      length=np.array((np.arange(0,x, step=1)))
      length1=length+1
      matplotlib.use('SVG')
      f = plt.figure()
      for n, fname in enumerate((group_paths)):
          image=im.open(fname)
          arr=np.asarray(image)
          f.add_subplot(x, 1, n)  # this line outputs images on top of each other
          ax = plt.subplot(x,1,n)
          ax.set_ylabel('Days', size=10)
          ax.set_yticks(group_y[n])
          ax.set_yticklabels(group_time[n],size=5)
          ax.set_title(group_name[n], size=10)
          ax.yaxis.tick_left()
          ax.set_xticks([0,255])
          ax.set_xticklabels([0,255],size=5)
          #for t in ax.yaxis.get_ticklines(): t.set_color('white')
          #for t in ax.xaxis.get_ticklines(): t.set_color('white')
          for line in ax.get_xticklines() + ax.get_yticklines(): line.set_alpha(0)
          ax.spines['bottom'].set_color('none')
          ax.spines['top'].set_color('none')
          ax.spines['left'].set_color('none')
          ax.spines['right'].set_color('none')
          plt.subplots_adjust()
          plt.imshow(arr)
      fig_name3=(str(outdir)+str(newfolder)+"/"+str(unique)+"_"+str(camera_label)+"_"+str(channels)+"_averaging_"+str(average_angles)+"_spacer_"+str(spacer)+"_slice_grouped_figure.svg")
      plt.savefig(fig_name3)
      plt.clf()
      
  elif cat_treat=='all':
    group_name=[]
    group_y=[]
    group_time=[]
    group_paths=[]
    height=[]
    unique_just_id=np.unique(just_id)
    for unique in unique_just_id:
      for i,data in enumerate(group_id):
        if unique==data[0]:
          group_name.append(data[1])
          group_y.append(data[2])
          group_time.append(data[3])
          group_paths.append(data[4])
      x=len(group_paths)
      length=np.array((np.arange(0,x, step=1)))
      length1=length+1
      matplotlib.use('SVG')
      f = plt.figure()
    for n, fname in enumerate((group_paths)):
        image=im.open(fname)
        arr=np.asarray(image)
        f.add_subplot(x, 1, n)  # this line outputs images on top of each other
        ax = plt.subplot(x,1,n)
        ax.set_ylabel('Days', size=10)
        ax.set_yticks(group_y[n])
        ax.set_yticklabels(group_time[n],size=5)
        ax.set_title(group_name[n], size=10)
        ax.yaxis.tick_left()
        ax.set_xticks([0,255])
        ax.set_xticklabels([0,255],size=5)
        #for t in ax.yaxis.get_ticklines(): t.set_color('white')
        #for t in ax.xaxis.get_ticklines(): t.set_color('white')
        for line in ax.get_xticklines() + ax.get_yticklines(): line.set_alpha(0)
        ax.spines['bottom'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_color('none')
        ax.spines['right'].set_color('none')
        plt.subplots_adjust()
        plt.imshow(arr)
        figheight=f.get_figheight()
        height.append(figheight)
    sumheight=np.sum(height)
    print sumheight
    #plt.set_figheight(figheight)
    fig_name3=(str(outdir)+str(newfolder)+"/"+"ALL_SAMPLES_"+str(camera_label)+"_"+str(channels)+"_averaging_"+str(average_angles)+"_spacer_"+str(spacer)+"_slice_grouped_figure.svg")
    plt.savefig(fig_name3)
    plt.clf
  
  if write_txt=='yes':
    os.close(signal_file1)
    os.close(signal_file2)
    os.close(signal_file3)     
  
  return outdir_name





  