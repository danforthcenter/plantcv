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
        plt.savefig(fig_name, dpi=300)
        plt.clf()
      
  return folder_path





  