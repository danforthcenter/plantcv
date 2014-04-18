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
import Image
import matplotlib
if not os.getenv('DISPLAY'):
  matplotlib.use('Agg')
from matplotlib import pyplot as plt


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
  newfolder="slice_analysis_"+(str(timenow))
  
  os.mkdir((str(outdir)+newfolder))
  
  connect=sq.connect(sqlitedb)
  connect.row_factory = dict_factory
  connect.text_factory=str
  c = connect.cursor()
  h = connect.cursor()
  m = connect.cursor()
  
  if signal_type=='vis':
    signal=c.execute('select * from snapshots inner join vis_colors on snapshots.image_id =vis_colors.image_id order by plant_id asc')
  elif signal_type=='nir':
    signal=c.execute('select * from snapshots inner join nir_signal on snapshots.image_id =nir_signal.image_id order by plant_id asc')
  elif signal_type=='fluor':
    signal=c.execute('select * from snapshots inner join flu_signal on snapshots.image_id =flu_signal.image_id order by plant_id asc')
  
  id_array=[]
  
  for i, group in enumerate(signal):
    plant_id=group['plant_id']
    plantgeno=re.match('^([A-Z][a-zA-Z]\d*[A-Z]{2})',plant_id)
    if plantgeno==None:
      plantgeno_id=group['plant_id']
      id_array.append(plantgeno_id,)
    else:
      span1,span2=plantgeno.span()
      plantgeno_id=group['plant_id'][span1:span2]
      id_array.append(plantgeno_id,)
      plantgeno_id1=group['plant_id']
  id_unique=np.unique(id_array)
  
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
  
  for date in c.execute('select min(datetime) as first from snapshots'):
    firstday=date['first']
  
  ch1_total_array=[]
  ch2_total_array=[]
  ch3_total_array=[]
  
  if spacer=='on':
    for group_label in id_unique: 
      ch1=[]
      ch2=[]
      ch3=[]
      time_array=[]
      if signal_type=='vis':
        database=h.execute('select * from snapshots inner join vis_colors on snapshots.image_id=vis_colors.image_id where plant_id like ? and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))
      elif signal_type=='nir':
        database=h.execute('select * from snapshots inner join nir_signal on snapshots.image_id=nir_signal.image_id where plant_id like ? and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))
      elif signal_type=='flu':
        database=h.execute('select * from snapshots inner join flu_signal on snapshots.image_id=flu_signal.image_id where plant_id like ? and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))
      
      for i,t in enumerate(database):
        date_int=((t['datetime']-firstday)/86400) 
        time_array.append(str(date_int),)
      unique_time=np.unique(time_array)
      
      if average_angles=='on':
        for time in unique_time:
          barcode=[]
          if signal_type=='vis':
            database_time=h.execute('select * from snapshots inner join vis_colors on snapshots.image_id=vis_colors.image_id where cast((((datetime-'+str(firstday)+')/86400)) as int)=?',(time,))
          elif signal_type=='nir':
            database_time=h.execute('select * from snapshots inner join nir_signal on snapshots.image_id=nir_signal.image_id where cast((((datetime-'+str(firstday)+')/86400)) as int)=?',(time,))
          elif signal_type=='flu':
            database_time=h.execute('select * from snapshots inner join flu_signal on snapshots.image_id=flu_signal.image_id where cast((((datetime-'+str(firstday)+')/86400)) as int)=?',(time,))
          
          for i, data in enumerate(database_time):          
            plantid=data['plant_id']
            plantid1=str(plantid)
            barcode.append(plantid1,)
          barcode_unique=np.unique(barcode)
          for id_name in barcode_unique:
            dim1_avg=[]
            dim2_avg=[]
            dim3_avg=[]
            if signal_type=='vis':
              database_id=h.execute('select * from snapshots inner join vis_colors on snapshots.image_id=vis_colors.image_id where plant_id=? and camera=?' , (id_name,camera_label,))
            elif signal_type=='nir':
              database_id=h.execute('select * from snapshots inner join nir_signal on snapshots.image_id=nir_signal.image_id where plant_id=? and camera=?', ("%"+id_name+"%",camera_label,))
            elif signal_type=='flu':
              database_id=h.execute('select * from snapshots inner join flu_signal on snapshots.image_id=flu_signal.image_id where plant_id=? and camera=?', ("%"+id_name+"%",camera_label,))
            for i, name in enumerate(database_id):
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
              
              dim1_avg.append(dim1_norm)
              dim2_avg.append(dim2_norm)
              dim3_avg.append(dim3_norm)
            
            ch1_avg=np.average(dim1_avg,axis=0)
            ch2_avg=np.average(dim2_avg,axis=0)
            ch3_avg=np.average(dim3_avg,axis=0)
            
            ch1_total_array.append((time,id_name,ch1_avg))
            ch2_total_array.append((time,id_name,ch2_avg))
            ch3_total_array.append((time,id_name,ch3_avg))
            
            if signal_type=='vis':
              norm_slice=np.dstack((ch1_avg,ch2_avg,ch3_avg))
            else:
              size=np.shape(dim1)
              blank=np.zeros(size)
              norm_slice=np.dstack((blank,blank,ch1_avg))
            
            if average_angles=='on':
              pcv.print_image(norm_slice, (str(outdir)+newfolder+"/"+str(barcode[i])+"averaged_angles_slice.png"))
            else:
              angle=data['frame']
              pcv.print_image(norm_slice,(str(outdir)+newfolder+"/"+str(barcode[i])+"_"+str(angle)+"_slice.png"))
      print ch1_total_array


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
import Image
import matplotlib
if not os.getenv('DISPLAY'):
  matplotlib.use('Agg')
from matplotlib import pyplot as plt


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
  newfolder="slice_analysis_"+(str(timenow))
  
  os.mkdir((str(outdir)+newfolder))
  
  connect=sq.connect(sqlitedb)
  connect.row_factory = dict_factory
  connect.text_factory=str
  c = connect.cursor()
  h = connect.cursor()
  m = connect.cursor()
  
  if signal_type=='vis':
    signal=c.execute('select * from snapshots inner join vis_colors on snapshots.image_id =vis_colors.image_id order by plant_id asc')
  elif signal_type=='nir':
    signal=c.execute('select * from snapshots inner join nir_signal on snapshots.image_id =nir_signal.image_id order by plant_id asc')
  elif signal_type=='fluor':
    signal=c.execute('select * from snapshots inner join flu_signal on snapshots.image_id =flu_signal.image_id order by plant_id asc')
  
  id_array=[]
  
  for i, group in enumerate(signal):
    plant_id=group['plant_id']
    plantgeno=re.match('^([A-Z][a-zA-Z]\d*[A-Z]{2})',plant_id)
    if plantgeno==None:
      plantgeno_id=group['plant_id']
      id_array.append(plantgeno_id,)
    else:
      span1,span2=plantgeno.span()
      plantgeno_id=group['plant_id'][span1:span2]
      id_array.append(plantgeno_id,)
      plantgeno_id1=group['plant_id']
  id_unique=np.unique(id_array)
  
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
  
  for date in c.execute('select min(datetime) as first from snapshots'):
    firstday=date['first']
  
  ch1_total_array=[]
  ch2_total_array=[]
  ch3_total_array=[]
  
  if spacer=='on':
    for group_label in id_unique: 
      ch1=[]
      ch2=[]
      ch3=[]
      time_array=[]
      if signal_type=='vis':
        database=h.execute('select * from snapshots inner join vis_colors on snapshots.image_id=vis_colors.image_id where plant_id like ? and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))
      elif signal_type=='nir':
        database=h.execute('select * from snapshots inner join nir_signal on snapshots.image_id=nir_signal.image_id where plant_id like ? and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))
      elif signal_type=='flu':
        database=h.execute('select * from snapshots inner join flu_signal on snapshots.image_id=flu_signal.image_id where plant_id like ? and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))
      
      for i,t in enumerate(database):
        date_int=((t['datetime']-firstday)/86400) 
        time_array.append(str(date_int),)
      unique_time=np.unique(time_array)
      
      if average_angles=='on':
        for time in unique_time:
          barcode=[]
          if signal_type=='vis':
            database_time=h.execute('select * from snapshots inner join vis_colors on snapshots.image_id=vis_colors.image_id where cast((((datetime-'+str(firstday)+')/86400)) as int)=?',(time,))
          elif signal_type=='nir':
            database_time=h.execute('select * from snapshots inner join nir_signal on snapshots.image_id=nir_signal.image_id where cast((((datetime-'+str(firstday)+')/86400)) as int)=?',(time,))
          elif signal_type=='flu':
            database_time=h.execute('select * from snapshots inner join flu_signal on snapshots.image_id=flu_signal.image_id where cast((((datetime-'+str(firstday)+')/86400)) as int)=?',(time,))
          
          for i, data in enumerate(database_time):          
            plantid=data['plant_id']
            plantid1=str(plantid)
            barcode.append(plantid1,)
          barcode_unique=np.unique(barcode)
          for id_name in barcode_unique:
            dim1_avg=[]
            dim2_avg=[]
            dim3_avg=[]
            if signal_type=='vis':
              database_id=h.execute('select * from snapshots inner join vis_colors on snapshots.image_id=vis_colors.image_id where plant_id=? and camera=?' , (id_name,camera_label,))
            elif signal_type=='nir':
              database_id=h.execute('select * from snapshots inner join nir_signal on snapshots.image_id=nir_signal.image_id where plant_id=? and camera=?', ("%"+id_name+"%",camera_label,))
            elif signal_type=='flu':
              database_id=h.execute('select * from snapshots inner join flu_signal on snapshots.image_id=flu_signal.image_id where plant_id=? and camera=?', ("%"+id_name+"%",camera_label,))
            for i, name in enumerate(database_id):
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
              
              dim1_avg.append(dim1_norm)
              dim2_avg.append(dim2_norm)
              dim3_avg.append(dim3_norm)
            
            ch1_avg=np.average(dim1_avg,axis=0)
            ch2_avg=np.average(dim2_avg,axis=0)
            ch3_avg=np.average(dim3_avg,axis=0)
            
            ch1_total_array.append((time,id_name,ch1_avg))
            ch2_total_array.append((time,id_name,ch2_avg))
            ch3_total_array.append((time,id_name,ch3_avg))
            
            if signal_type=='vis':
              norm_slice=np.dstack((ch1_avg,ch2_avg,ch3_avg))
            else:
              size=np.shape(dim1)
              blank=np.zeros(size)
              norm_slice=np.dstack((blank,blank,ch1_avg))
            
            if average_angles=='on':
              pcv.print_image(norm_slice, (str(outdir)+newfolder+"/"+str(barcode[i])+"averaged_angles_slice.png"))
            else:
              angle=data['frame']
              pcv.print_image(norm_slice,(str(outdir)+newfolder+"/"+str(barcode[i])+"_"+str(angle)+"_slice.png"))
      print ch1_total_array

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



  