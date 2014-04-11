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

def slice_stitch(sqlitedb, outdir):
  #sqlitedb = sqlite database to query (path to db)

  connect=sq.connect(sqlitedb)
  connect.row_factory = dict_factory
  connect.text_factory=str
  c = connect.cursor()
  h = connect.cursor()
  
  time_array=[]
  id_array=[]
  path_array=[]
  ch1=[]
  ch2=[]
  ch3=[]
  
  for date in h.execute('select min(datetime) as first from snapshots'):
    firstday=date['first']

  for i, data in enumerate(h.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where type = "slice" order by cast((((datetime-'+str(firstday)+')/86400)) as int), plant_id asc')):
    imgpath=data['image_path']

    plantid=data['plant_id']
    plantgeno=re.match('^([A-Z][a-zA-Z]\d*[A-Z]{2})',plantid)
    if plantgeno==None:
      plantgeno_id=data['plant_id']
      id_array.append(plantgeno_id)
    else:
      span1,span2=plantgeno.span()
      plantgeno_id=data['plant_id'][span1:span2]
      id_array.append(plantgeno_id)
    
    time=(data['datetime'])
    time_con=(float(time-firstday)/86400)
    time_int=int(time_con)
    time_array.append(time_int)
    
    path=(data['image_path'])
    path_array.append(path)
    
    if i==0:
      line1=cv2.imread(path_array[i])
      split1, split2, split3=np.dsplit(line1,3)
      
      split1_f=split1.flatten()
      split2_f=split2.flatten()
      split3_f=split3.flatten()
      
      stacked_1=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f))
      stacked_2=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f))
      stacked_3=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f)) 
      stacked_1t=np.transpose(stacked_1)
      stacked_2t=np.transpose(stacked_2)
      stacked_3t=np.transpose(stacked_3)
      
      ch1.extend(stacked_1t)
      ch2.extend(stacked_2t)
      ch3.extend(stacked_3t)
    else:
      if time_array[i-1]==time_array[i] and id_array[i-1]==id_array[i]:
        line1=cv2.imread(path_array[i])      
        split1, split2, split3=np.dsplit(line1,3)
        
        split1_f=split1.flatten()
        split2_f=split2.flatten()
        split3_f=split3.flatten()
        
        spacer_size=np.shape(split1)
        spacer=(np.zeros((spacer_size)))+255
        stacked_spacer=np.column_stack((spacer, spacer, spacer, spacer, spacer))
        stacked_spacert=np.transpose(stacked_spacer)
        
        stacked_1=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f))
        stacked_2=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f))
        stacked_3=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f)) 
        stacked_1t=np.transpose(stacked_1)
        stacked_2t=np.transpose(stacked_2)
        stacked_3t=np.transpose(stacked_3)
      
        ch1.extend(stacked_1t)
        ch2.extend(stacked_2t)
        ch3.extend(stacked_3t)
      elif time_array[i-1]!=time_array[i] and id_array[i-1]==id_array[i]:
        line1=cv2.imread(path_array[i])      
        split1, split2, split3=np.dsplit(line1,3)
        
        split1_f=split1.flatten()
        split2_f=split2.flatten()
        split3_f=split3.flatten()
        
        spacer_size=np.shape(split1)
        spacer_blank=np.zeros(spacer_size)
        spacer=spacer_blank+255
        
        stacked_1=np.column_stack((spacer,spacer,spacer,spacer,spacer, split1_f,split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f))
        stacked_2=np.column_stack((spacer,spacer, spacer, spacer, spacer, split2_f,split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f))
        stacked_3=np.column_stack((spacer, spacer, spacer, spacer,spacer,split3_f,split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f)) 
        stacked_1t=np.transpose(stacked_1)
        stacked_2t=np.transpose(stacked_2)
        stacked_3t=np.transpose(stacked_3)
        
        ch1.extend(stacked_1t)
        ch2.extend(stacked_2t)
        ch3.extend(stacked_3t)
      elif id_array[i-1]!=id_array[i]:
        color_cat=np.dstack((ch1,ch2,ch3))
        pcv.print_image(color_cat,(str(outdir)+str(plantgeno_id)+"_slice_joined_img.png"))
        ch1=[]
        ch2=[]
        ch3=[]
        line1=cv2.imread(path_array[i])
        split1, split2, split3=np.dsplit(line1,3)
         
        split1_f=split1.flatten()
        split2_f=split2.flatten()
        split3_f=split3.flatten()
        
        stacked_1=np.column_stack((split1_f,split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f, split1_f))
        stacked_2=np.column_stack((split2_f,split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f, split2_f))
        stacked_3=np.column_stack((split3_f,split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f, split3_f)) 
        stacked_1t=np.transpose(stacked_1)
        stacked_2t=np.transpose(stacked_2)
        stacked_3t=np.transpose(stacked_3)
        
        ch1.extend(stacked_1t)
        ch2.extend(stacked_2t)
        ch3.extend(stacked_3t)
  
  print np.shape(path_array)
  print np.shape(time_array)
  print np.shape(id_array)  
      #else:
      #  color_cat=np.dstack((ch1,ch2,ch3))
      #  pcv.print_image(color_cat,(str(outdir)+str(plantgeno_id)+"_slice_joined_img.png"))
      #  ch1=[]
      #  ch2=[]
      #  ch3=[]
  
  


        


    
