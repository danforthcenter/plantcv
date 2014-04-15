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
from matplotlib import pyplot as plt
from matplotlib import cm as cm
import pylab as pl


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

def slice_stitch(sqlitedb, outdir, camera_label='vis_sv', spacer='on'):
  #sqlitedb = sqlite database to query (path to db)
  #outdir = path to outdirectory
  #camera_label = either 'vis_tv','vis_sv',or 'fluor_tv'
  #spacer = either 'on' or 'off', adds a gray line between days

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
      for i, data in enumerate(h.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where plant_id like ? and type = "slice" and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))):
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
          
          spacer_size=np.shape(split1)
          spacer=(np.zeros((spacer_size)))+255
          spacer_f=spacer.flatten()
          
          stacked_1=np.column_stack((spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,spacer_f, spacer_f, spacer_f, spacer_f, spacer_f, split1_f,split1_f, split1_f, split1_f, split1_f))
          stacked_2=np.column_stack((spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,spacer_f, spacer_f, spacer_f, spacer_f, spacer_f, split2_f, split2_f, split2_f, split2_f, split2_f))
          stacked_3=np.column_stack((spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,spacer_f, spacer_f, spacer_f, spacer_f, spacer_f,  split3_f, split3_f, split3_f, split3_f, split3_f)) 
          stacked_1t=np.transpose(stacked_1)
          stacked_2t=np.transpose(stacked_2)
          stacked_3t=np.transpose(stacked_3)
      
          ch1.extend(stacked_1t)
          ch2.extend(stacked_2t)
          ch3.extend(stacked_3t) 
    
      color_cat=np.dstack((ch1,ch2,ch3))
      pcv.print_image(color_cat,(str(outdir)+newfolder+"/"+str(group_label)+"_"+str(camera_label)+"_spacer_"+str(spacer)+"_slice_joined_img.png"))
    
  if spacer=='off':
    for group_label in id_unique:
      ch1=[]
      ch2=[]
      ch3=[]
      time_array=[]
      for i, data in enumerate(h.execute('select * from snapshots inner join analysis_images on snapshots.image_id = analysis_images.image_id where plant_id like ? and type = "slice" and camera=? order by datetime asc', ("%"+group_label+"%",camera_label,))):
        date_int=((data['datetime']-firstday)/86400) 
        time_array.append(date_int)
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
      
  return time_array, id_unique ,folder_path

def slice_figure(folder_path):
  
  i=datetime.now()
  timenow=i.strftime('%m-%d-%Y_%H:%M:%S')
  newfolder="slice_figure_"+(str(timenow))
  
  os.mkdir((str(folder_path)+"/"+newfolder))
  new_folder_path=str(folder_path)+"/"+newfolder+"/"
  
  list_files=os.listdir(folder_path)
  sorted_list=sorted(list_files)
  for files in sorted_list:
    img=cv2.imread((str(folder_path)+"/"+str(files)))
    titles=re.match('^([A-Z][a-zA-Z]\d*[A-Z]{2})',files)
    span1,span2=titles.span()
    title_name=files[span1:span2]
    
    plt.imshow(img)
    plt.axis('off')
    plt.title(str(title_name))
    fig_name=new_folder_path+str(title_name)+"_slice_join_figure_img.png"
    plt.savefig(fig_name, dpi=300)
    plt.clf()



  