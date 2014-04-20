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
  matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pylab as plab
import Image

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

def visualize_slice(sqlitedb,outdir,signal_type='vis', camera_label='vis_sv',channels='rgb',average_angles='on',spacer='on', makefig='yes'):
  #sqlitedb = sqlite database to query (path to db)
  #outdir = path to outdirectory
  #camera_type='vis','nir' or 'fluor'
  #camera_label = either 'vis_tv','vis_sv',or 'fluor_tv'
  #channels = signal,'rgb' 'lab' or 'hsv'
  #average_angles = if on side angles for a plant are averaged
  #spacer = either 'on' or 'off', adds a white line between day breaks
  #makefig = either 'yes' or 'no', adds labels to days and a title
  
  i=datetime.now()
  timenow=i.strftime('%m-%d-%Y_%H:%M:%S')
  newfolder="slice_figs_and_images_"+(str(timenow))
  
  os.mkdir((str(outdir)+newfolder))
  outdir_name=str(outdir)+str(newfolder)+"/"
  
  connect=sq.connect(sqlitedb)
  connect.row_factory = dict_factory
  connect.text_factory=str
  c = connect.cursor()
  h = connect.cursor()
  m = connect.cursor()
  
  for date in c.execute('select min(datetime) as first from snapshots'):
    firstday=date['first']
    
  if signal_type=='vis':
    signal=c.execute('select * from snapshots inner join vis_colors on snapshots.image_id =vis_colors.image_id order by plant_id asc')
  elif signal_type=='nir':
    signal=c.execute('select * from snapshots inner join nir_signal on snapshots.image_id =nir_signal.image_id order by plant_id asc')
  elif signal_type=='fluor':
    signal=c.execute('select * from snapshots inner join flu_signal on snapshots.image_id =flu_signal.image_id order by plant_id asc')
  
  barcode_array=[]
  ch1_total_array=[]
  ch2_total_array=[]
  ch3_total_array=[]
  
  for i, group in enumerate(signal):
    bins=int(group['bins'])
    plant_id=group['plant_id']
    barcode_array.append(plant_id,)
  barcode_unique=np.unique(barcode_array)

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
        
        ch1_join=','.join(map(str,ch1))
        ch2_join=','.join(map(str,ch2))
        ch3_join=','.join(map(str,ch3))
        os.write(signal_file1, ch1_join)
        os.write(signal_file2, ch2_join)
        os.write(signal_file3, ch3_join)
        os.write(signal_file1, os.linesep)
        os.write(signal_file2, os.linesep)
        os.write(signal_file3, os.linesep)

  if makefig=='yes':  
    id_array=[]
    date_array=[]
    sort_ch1= np.array(ch1_total_array)
    sort_ch2= np.array(ch2_total_array)
    sort_ch3= np.array(ch3_total_array)
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
      fig_name1=(str(outdir)+str(newfolder)+"/"+str(name)+"_"+str(camera_label)+"_"+str(channels)+"_averaging_"+str(average_angles)+"_spacer_"+str(spacer)+"_slice_joined_figure.png")
      print fig_name1
      plt.savefig(fig_name1, dpi=300, bbox_inches='tight')
      plt.clf()
  
  os.close(signal_file1)
  os.close(signal_file2)
  os.close(signal_file3)     

  return outdir_name

def cat_fig(outdir,img_dir_name):
  i=datetime.now()
  timenow=i.strftime('%m-%d-%Y_%H:%M:%S')
  newfolder="concatenated_slice_figs_"+(str(timenow))
  
  os.mkdir((str(outdir)+newfolder))
  
  path=str(img_dir_name)
  opendir=os.listdir(path)

  slice_fig_path=[]
  treat_array=[]
  geno_treat=[]

  for filename in opendir:
    if re.search("_slice_joined_figure\.png$",filename):
      slice_fig=str(filename)
      slice_fig_path.append(slice_fig)
  for fig in slice_fig_path:
    gt=re.match('^([A-Z][a-zA-Z]\d*[A-Z]{2})',fig)
    if gt!=None:
      t=re.match('^([A-Z][a-zA-Z]\d*)',fig)
      span1,span2=gt.span()
      span3,span4=t.span()
      geno_id=fig[span1:span2]
      treat=fig[span3:span4]
      fig_path=str(path)+str(fig)
      info_array=(treat,geno_id,fig_path)
      treat_array.append(treat)
      geno_treat.append(info_array)
  
  path_info=np.array(geno_treat)
  treat_array1=np.array(treat_array)
  unique_treat=np.unique(treat_array1)
  
  print path_info
  print unique_treat
  
  for t in unique_treat:
    cat=[]
    for i,p in enumerate(path_info):
      if p[0]==t:
        path_cat=p[2]
        cat.append(path_cat)
     
    x=len(cat)    
    f = plt.figure()
    for n, fname in enumerate(cat):
      image=Image.open(fname)
      arr=np.asarray(image)
      f.add_subplot(x,1,n, aspect='equal')
      plt.imshow(arr)
      plt.axis('off')
    fig_name1=(str(outdir)+str(newfolder)+"/"+str(t)+"_slice_joined_figure.png")
    print fig_name1
    plt.savefig(fig_name1, dpi=300,bbox_inches='tight')
    plt.clf()

def slice_stitch(sqlitedb, outdir, camera_label='vis_sv', spacer='on',makefig='yes'):
  #sqlitedb = sqlite database to query (path to db)
  #outdir = path to outdirectory
  #camera_label = either 'vis_tv','vis_sv',or 'fluor_tv'
  #spacer = either 'on' or 'off', adds a white line between day breaks
  #makefig = either 'yes' or 'no', adds labels to days and a title

  i=datetime.now()
  timenow=i.strftime('%m-%d-%Y_%H:%M:%S')
  newfolder="slice_analysis_"+(str(timenow))
  
  os.mkdir((str(outdir)+newfolder))
  
  connect=sq.connect(sqlitedb)
  connect.row_factory = dict_factory
  connect.text_factory=str
  c = connect.cursor()
  h = connect.cursor()
  m = connect.cursor()
  k = connect.cursor()

  id_array=[]
  path_array=[]
  unique_array=[]
  
  
  for date in c.execute('select min(datetime) as first from snapshots'):
    firstday=date['first']
  
  for i, group in enumerate(m.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where type = "slice" order by plant_id asc')):
    plant_id=group['plant_id']
    plantgeno=re.match('^([A-Z][a-zA-Z]\d*[A-Z]{2})',plant_id)
    if plantgeno==None:
      plantgeno_id=group['plant_id']
      id_array.append(plantgeno_id,)
    else:
      span1,span2=plantgeno.span()
      plantgeno_id=group['plant_id'][span1:span2]
      id_array.append(plantgeno_id,)
  id_unique=np.unique(id_array)
  
  if spacer=='on':
    for group_label in id_unique:
      ch1=[]
      ch2=[]
      ch3=[]
      time_array=[]
      for i, data in enumerate(h.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where plant_id like ? and type = "slice" and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))):
        date_int=((data['datetime']-firstday)/86400) 
        time_array.append(date_int)
      for i, data in enumerate(k.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where plant_id like ? and type = "slice" and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))): 
        if i==0:
          line1=cv2.imread(data['image_path'])
          split1, split2, split3=np.dsplit(line1,3)
          split1_f=split1.flatten()
          split2_f=split2.flatten()
          split3_f=split3.flatten()
          
          stacked_1=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f))
          stacked_2=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f))
          stacked_3=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f)) 
          stacked_1t=np.transpose(stacked_1)
          stacked_2t=np.transpose(stacked_2)
          stacked_3t=np.transpose(stacked_3)
        
          ch1.extend(stacked_1t)
          ch2.extend(stacked_2t)
          ch3.extend(stacked_3t)
        elif time_array[i-1]==time_array[i]:
          line1=cv2.imread(data['image_path'])
          split1, split2, split3=np.dsplit(line1,3)
          
          split1_f=split1.flatten()
          split2_f=split2.flatten()
          split3_f=split3.flatten()
          
          stacked_1=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f))
          stacked_2=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f))
          stacked_3=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f)) 
          stacked_1t=np.transpose(stacked_1)
          stacked_2t=np.transpose(stacked_2)
          stacked_3t=np.transpose(stacked_3)
        
          ch1.extend(stacked_1t)
          ch2.extend(stacked_2t)
          ch3.extend(stacked_3t)
        else:
          line1=cv2.imread(data['image_path'])
          split1, split2, split3=np.dsplit(line1,3)
          
          split1_f=split1.flatten()
          split2_f=split2.flatten()
          split3_f=split3.flatten()
          
          spacer_size=np.shape(split1_f)
          spacer1=np.zeros(spacer_size)
          spacer_f=spacer1+255
          
          stacked_1=np.column_stack((spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,spacer_f, spacer_f, spacer_f, spacer_f, spacer_f))
          stacked_2=np.column_stack((spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,spacer_f, spacer_f, spacer_f, spacer_f, spacer_f))
          stacked_3=np.column_stack((spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,spacer_f, spacer_f, spacer_f, spacer_f, spacer_f)) 
          stacked_1t=np.transpose(stacked_1)
          stacked_2t=np.transpose(stacked_2)
          stacked_3t=np.transpose(stacked_3)
          
          ch1.extend(stacked_1t)
          ch2.extend(stacked_2t)
          ch3.extend(stacked_3t)
          
          stacked_4=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f))
          stacked_5=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f))
          stacked_6=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f)) 
          stacked_4t=np.transpose(stacked_4)
          stacked_5t=np.transpose(stacked_5)
          stacked_6t=np.transpose(stacked_6)
        
          ch1.extend(stacked_4t)
          ch2.extend(stacked_5t)
          ch3.extend(stacked_6t)
        
      color_cat=np.dstack((ch1,ch2,ch3))
      pcv.print_image(color_cat,(str(outdir)+str(newfolder)+"/"+str(group_label)+"_"+str(camera_label)+"_spacer_"+str(spacer)+"_slice_joined_img.png"))
      
  if spacer=='off':
    for group_label in id_unique:
      ch1=[]
      ch2=[]
      ch3=[]
      for i, data in enumerate(h.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where plant_id like ? and type = "slice" and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))):
        line1=cv2.imread(data['image_path'])
        
        split1, split2, split3=np.dsplit(line1,3)
         
        split1_f=split1.flatten()
        split2_f=split2.flatten()
        split3_f=split3.flatten()
        
        stacked_1=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f))
        stacked_2=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f))
        stacked_3=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f)) 
        stacked_1t=np.transpose(stacked_1)
        stacked_2t=np.transpose(stacked_2)
        stacked_3t=np.transpose(stacked_3)
      
        ch1.extend(stacked_1t)
        ch2.extend(stacked_2t)
        ch3.extend(stacked_3t)
      
      color_cat=np.dstack((ch1,ch2,ch3))
      pcv.print_image(color_cat,(str(outdir)+newfolder+"/"+str(group_label)+"_"+str(camera_label)+"_spacer_"+str(spacer)+"_slice_joined_img.png"))
  
  folder_path=(str(outdir)+newfolder)
      
  if makefig=='yes':
    list_files=os.listdir(folder_path)
    sorted_list=sorted(list_files)
  
    for group_label in id_unique:
      time_array=[]
      length_time=[]
      ypos=[]
      ypos1=[]
      ypos2=[]
      unique_time1=[]
      for i, data in enumerate(h.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where plant_id like ? and type = "slice" and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))):
        date_int=((data['datetime']-firstday)/86400) 
        time_array.append(date_int)
    
      unique_time=np.unique(time_array)
      
      for times in unique_time:
        length=[]
        for i,time in enumerate(time_array):
          if time_array[i]==times:
            tm=1
            length.append(tm)
          else:
            tm=0
            length.append(tm)
        sum_time=np.sum(length)
        length_time.append(sum_time) 
  
      if spacer=='off':  
        for i,length in enumerate(length_time):
          if i==0:
            yadd=length*5
            ypos.append(yadd)
          else:
            yadd=(length*5)
            ypos.append(yadd)
      elif spacer=='on':
        for i,length in enumerate(length_time):
          if i==0:
            yadd=length*5
            ypos.append(yadd)
          else:
            yadd=(length*5)+10
            ypos.append(yadd)
            
      for i,y in enumerate(ypos):
        if i==0:
          y1=y
          ypos1.append(y1)
        else:
          y1=y+ypos1[i-1]
          ypos1.append(y1)
      
      for time in unique_time:
        time1=time+1
        unique_time1.append(time1)
  
      file_name=str(group_label)+"_"+str(camera_label)+"_spacer_"+str(spacer)+"_slice_joined_img.png"
      img1=cv2.imread((str(folder_path)+"/"+str(file_name)), -1)
      if len(np.shape(img1))==3: 
        ch1,ch2,ch3=np.dsplit(img1,3)
        img=np.dstack((ch3,ch2,ch1))
        
        plt.imshow(img)
        ax = plt.subplot(111)
        ax.set_ylabel('Days on Bellwether Phenotyper', size=10)
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
        #ax.tick_params(axis='y',direction='out')

        plt.title(str(group_label))
        fig_name=(str(folder_path)+"/"+str(group_label)+"_spacer_"+str(spacer)+"_slice_join_figure_img.png")
        plt.savefig(fig_name, dpi=300,bbox_inches='tight')
        plt.clf()
      
  return folder_path


def slice_stitch_geno(sqlitedb, outdir, title, camera_label='vis_sv', spacer='on',makefig='yes'):
  ###note: this function only works well if you have a reasonable number of genotypes and timepoints otherwise use the fig_stitch tool###
  #sqlitedb = sqlite database to query (path to db)
  #outdir = path to outdirectory
  #camera_label = either 'vis_tv','vis_sv',or 'fluor_tv'
  #spacer = either 'on' or 'off', adds a white line between day breaks
  #makefig = either 'yes' or 'no', adds labels to days and a title

  i=datetime.now()
  timenow=i.strftime('%m-%d-%Y_%H:%M:%S')
  newfolder="slice_analysis_"+(str(timenow))
  
  os.mkdir((str(outdir)+newfolder))
  
  connect=sq.connect(sqlitedb)
  connect.row_factory = dict_factory
  connect.text_factory=str
  c = connect.cursor()
  h = connect.cursor()
  m = connect.cursor()
  k = connect.cursor()

  id_array=[]
  path_array=[]
  unique_array=[]
  geno_id=[]
  ch1=[]
  ch2=[]
  ch3=[]
  
  for date in c.execute('select min(datetime) as first from snapshots'):
    firstday=date['first']
  
  for i, group in enumerate(m.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where type = "slice" order by plant_id asc')):
    plant_id=group['plant_id']
    plantgeno=re.match('^([A-Z][a-zA-Z]\d*[A-Z]{2})',plant_id)
    if plantgeno==None:
      plantgeno_id=group['plant_id']
      id_array.append(plantgeno_id,)
    else:
      span1,span2=plantgeno.span()
      plantgeno_id=group['plant_id'][span1:span2]
      id_array.append(plantgeno_id,)
  id_unique=np.unique(id_array)
  
  if spacer=='on':
    for group_label in id_unique:
      geno_array=[]
      for i, data in enumerate(h.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where plant_id like ? and type = "slice" and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))):
        plantid=data['plant_id']
        geno_array.append(plantid)
      length_id=len(geno_array)
      for i, data in enumerate(k.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where plant_id like ? and type = "slice" and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))): 
        geno_id.append(group_label)
        if i==(length_id-1):
          line1=cv2.imread(data['image_path'])
          split1, split2, split3=np.dsplit(line1,3)
          
          split1_f=split1.flatten()
          split2_f=split2.flatten()
          split3_f=split3.flatten()
          
          stacked_4=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f))
          stacked_5=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f))
          stacked_6=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f)) 
          stacked_4t=np.transpose(stacked_4)
          stacked_5t=np.transpose(stacked_5)
          stacked_6t=np.transpose(stacked_6)
        
          ch1.extend(stacked_4t)
          ch2.extend(stacked_5t)
          ch3.extend(stacked_6t)
          
          spacer_size=np.shape(split1_f)
          spacer1=np.zeros(spacer_size)
          spacer_f=spacer1+255
          
          stacked_1=np.column_stack((spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,spacer_f, spacer_f, spacer_f, spacer_f, spacer_f))
          stacked_2=np.column_stack((spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,spacer_f, spacer_f, spacer_f, spacer_f, spacer_f))
          stacked_3=np.column_stack((spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,spacer_f, spacer_f, spacer_f, spacer_f, spacer_f)) 
          stacked_1t=np.transpose(stacked_1)
          stacked_2t=np.transpose(stacked_2)
          stacked_3t=np.transpose(stacked_3)
          
          ch1.extend(stacked_1t)
          ch2.extend(stacked_2t)
          ch3.extend(stacked_3t)
          
        else:
          line1=cv2.imread(data['image_path'])
          split1, split2, split3=np.dsplit(line1,3)
          split1_f=split1.flatten()
          split2_f=split2.flatten()
          split3_f=split3.flatten()
          
          stacked_1=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f))
          stacked_2=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f))
          stacked_3=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f)) 
          stacked_1t=np.transpose(stacked_1)
          stacked_2t=np.transpose(stacked_2)
          stacked_3t=np.transpose(stacked_3)
        
          ch1.extend(stacked_1t)
          ch2.extend(stacked_2t)
          ch3.extend(stacked_3t)
   
    color_cat=np.dstack((ch1,ch2,ch3))
    pcv.print_image(color_cat,(str(outdir)+str(newfolder)+"/"+str(group_label)+"_"+str(camera_label)+"_spacer_"+str(spacer)+"_slice_joined_img.png"))
      
  if spacer=='off':
    for group_label in id_unique:
      for i, data in enumerate(h.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where plant_id like ? and type = "slice" and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))):
        geno_id.append(group_label)

        line1=cv2.imread(data['image_path'])
        
        split1, split2, split3=np.dsplit(line1,3)
         
        split1_f=split1.flatten()
        split2_f=split2.flatten()
        split3_f=split3.flatten()
        
        stacked_1=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f))
        stacked_2=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f))
        stacked_3=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f)) 
        stacked_1t=np.transpose(stacked_1)
        stacked_2t=np.transpose(stacked_2)
        stacked_3t=np.transpose(stacked_3)
      
        ch1.extend(stacked_1t)
        ch2.extend(stacked_2t)
        ch3.extend(stacked_3t)
      
    color_cat=np.dstack((ch1,ch2,ch3))
    pcv.print_image(color_cat,(str(outdir)+newfolder+"/"+"ALL_GENOTYPE_"+str(camera_label)+"_spacer_"+str(spacer)+"_slice_joined_img.png"))
  
  folder_path=(str(outdir)+newfolder)
      
  if makefig=='yes':
      ypos=[]
      ypos1=[]
      geno_num=[]
      
      unique_geno=np.unique(geno_id)
      for geno in unique_geno:
        length=[]
        for i, id in enumerate(geno_id):
          if geno_id[i]==geno:
            g=1
            length.append(g)
          else:
            g=0
            length.append(g)
        sum_geno=np.sum(length)
        geno_num.append(sum_geno)
      
  
      if spacer=='off':  
        for i,geno in enumerate(geno_num):
          if i==0:
            yadd=geno*5
            ypos.append(yadd)
          else:
            yadd=(geno*5)
            ypos.append(yadd)
      elif spacer=='on':
        for i,geno in enumerate(geno_num):
          if i==0:
            yadd=geno*5
            ypos.append(yadd)
          else:
            yadd=(geno*5)+10
            ypos.append(yadd)
            
      for i,y in enumerate(ypos):
        if i==0:
          y1=y
          ypos1.append(y1)
        else:
          y1=y+ypos1[i-1]
          ypos1.append(y1)
      
      print unique_geno
  
      file_name=str(group_label)+"_"+str(camera_label)+"_spacer_"+str(spacer)+"_slice_joined_img.png"
      img1=cv2.imread((str(folder_path)+"/"+str(file_name)), -1)
      if len(np.shape(img1))==3: 
        ch1,ch2,ch3=np.dsplit(img1,3)
        img=np.dstack((ch3,ch2,ch1))
        
        plt.imshow(img)
        ax = plt.subplot(111)
        ax.set_ylabel('Genotype', size=10)
        ax.set_yticks(ypos1)
        ax.set_yticklabels(unique_geno,size=3)
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
        #ax.tick_params(axis='y',direction='out')

        plt.title(str(title))
        fig_name=(str(folder_path)+"/"+"All_genotypes_spacer_"+str(spacer)+"_slice_join_figure_img.png")
        plt.savefig(fig_name, dpi=300)
        plt.clf()
      
  return folder_path




  