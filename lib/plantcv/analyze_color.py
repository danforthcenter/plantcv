import os
import cv2
import numpy as np
import matplotlib
if not os.getenv('DISPLAY'):
  matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from matplotlib import colors as colors
from matplotlib import colorbar as colorbar
import pylab as pl
from . import print_image
from . import fatal_error

### Analyze Color of Object
def _pseudocolored_image(histogram, bins, img, mask, background, channel, filename, resolution):
  # histogram = a normalized histogram of color values from one color channel
  # bins = number of color bins the channel is divided into
  # img = input image
  # mask = binary mask image
  # background = what background image?: channel image (img) or white
  # channel = color channel name
  # filename = input image filename
  # resolution = output image resolution
  
  # Get the image size
  if np.shape(img)[2] == 3:
    ix, iy, iz = np.shape(img)
  else:
    ix, iy = np.shape(img)
  size = ix, iy
  
  plt.imshow(histogram, vmin=0, vmax=(bins - 1), cmap=cm.jet)
  mask_inv = cv2.bitwise_not(mask)
  my_cmap = plt.get_cmap('binary_r')
  
  if background == 'img':
    # Plot pseudocolored plant on the channel image
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pot = cv2.bitwise_and(img_gray, img_gray, mask=mask_inv)
    pot_img = cv2.add(pot, mask)
    pot_rgba = np.dstack((pot_img, pot_img, pot_img, mask_inv))
    plt.imshow(pot_rgba, cmap=my_cmap)
  elif background == 'white':
    # Plot pseudocolored plant on a white background
    # Create white background
    w_back = np.zeros(size, dtype=np.uint8) + 255
    white_rgba = np.dstack((w_back, w_back, w_back, mask_inv))
    plt.imshow(white_rgba, cmap=my_cmap)
  else:
    fatal_error("Background type " + background + " is not a valid type!")

  plt.axis('off')
  
  # Name output file
  fig_name = str(filename[0:-4]) + '_' + str(channel) + '_pseudo_on_' + str(background) + '.png'
  
  # Save image
  plt.savefig(fig_name, dpi=resolution, bbox_inches='tight')
  print('\t'.join(map(str, ('IMAGE', 'pseudo', fig_name))))
  plt.clf()
  
  
def analyze_color(img, imgname, mask, bins, device, debug=False, hist_plot_type='all', cslice_type='rgb', pseudo_channel='v', pseudo_bkg='img', resolution=300, filename=False):
  # img = image
  # imgname = name of input image
  # mask = mask made from selected contours
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print data and histograms
  # hist_plot_type= 'None', 'all', 'rgb','lab' or 'hsv'
  # color_slice_type = 'None', 'rgb', 'hsv' or 'lab'
  # pseudo_channel= 'None', 'l', 'm' (green-magenta), 'y' (blue-yellow), h','s', or 'v', creates pseduocolored image based on the specified channel
  # pseudo_bkg = 'img' => channel image, 'white' => white background image, 'both' => both img and white options
  # filename= False or image name. If defined print image
  
  device += 1
  if np.shape(img)[2]==3:
    ix,iy,iz=np.shape(img)
  else:
    ix,iy=np.shape(img)
  size = ix,iy
  background = np.zeros(size, dtype=np.uint8)
  w_back=background+255
  ori_img=np.copy(img)
  
  masked=cv2.bitwise_and(img,img, mask=mask)
  b,g,r=cv2.split(masked)
  lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
  l,m,y=cv2.split(lab)
  hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
  h,s,v=cv2.split(hsv)
  
  channel=(b,g,r,l,m,y,h,s,v)
  graph_color=('blue','forestgreen','red','dimgray','magenta','yellow','blueviolet','cyan','orange' )
  label=('blue','green','red', 'lightness','green-magenta','blue-yellow','hue','saturation', 'value')

  # Create Color Histogram Data
  b_bin=b/(256/bins)
  g_bin=g/(256/bins)
  r_bin=r/(256/bins)
  l_bin=l/(256/bins)
  m_bin=m/(256/bins)
  y_bin=y/(256/bins)
  h_bin=h/(256/bins)
  s_bin=s/(256/bins)
  v_bin=v/(256/bins)
  
  hist_b= cv2.calcHist([b_bin],[0],mask,[bins], [0,(bins-1)])
  hist_g= cv2.calcHist([g_bin],[0],mask,[bins], [0,(bins-1)])
  hist_r= cv2.calcHist([r_bin],[0],mask,[bins], [0,(bins-1)])
  hist_l= cv2.calcHist([l_bin],[0],mask,[bins], [0,(bins-1)])
  hist_m= cv2.calcHist([m_bin],[0],mask,[bins], [0,(bins-1)])
  hist_y= cv2.calcHist([y_bin],[0],mask,[bins], [0,(bins-1)])
  hist_h= cv2.calcHist([h_bin],[0],mask,[bins], [0,(bins-1)])
  hist_s= cv2.calcHist([s_bin],[0],mask,[bins], [0,(bins-1)])
  hist_v= cv2.calcHist([v_bin],[0],mask,[bins], [0,(bins-1)])

  hist_data_b=[l[0] for l in hist_b]
  hist_data_g=[l[0] for l in hist_g]
  hist_data_r=[l[0] for l in hist_r]
  hist_data_l=[l[0] for l in hist_l]
  hist_data_m=[l[0] for l in hist_m]
  hist_data_y=[l[0] for l in hist_y]
  hist_data_h=[l[0] for l in hist_h]
  hist_data_s=[l[0] for l in hist_s]
  hist_data_v=[l[0] for l in hist_v]
    
  
  #Store Color Histogram Data
  hist_header=(
    'HEADER_HISTOGRAM',
    'bin-number',
    'blue',
    'green',
    'red',
    'lightness',
    'green-magenta',
    'blue-yellow',
    'hue',
    'saturation',
    'value'
    )

  hist_data= (
    'HISTOGRAM_DATA',
    bins,
    hist_data_b,
    hist_data_g,
    hist_data_r,
    hist_data_l,
    hist_data_m,
    hist_data_y,
    hist_data_h,
    hist_data_s,
    hist_data_v
    )
  
  # Create Histogram Plot
  if filename:
    if hist_plot_type=='all':
      plt.plot(hist_b,color=graph_color[0],label=label[0])
      plt.plot(hist_g,color=graph_color[1],label=label[1])
      plt.plot(hist_r,color=graph_color[2],label=label[2])
      plt.plot(hist_l,color=graph_color[3],label=label[3])
      plt.plot(hist_m,color=graph_color[4],label=label[4])
      plt.plot(hist_y,color=graph_color[5],label=label[5])
      plt.plot(hist_h,color=graph_color[6],label=label[6])
      plt.plot(hist_s,color=graph_color[7],label=label[7])
      plt.plot(hist_v,color=graph_color[8],label=label[8])
      plt.xlim([0,(bins-1)])
      plt.legend()
    elif hist_plot_type=='rgb':
      plt.plot(hist_b,color=graph_color[0],label=label[0])
      plt.plot(hist_g,color=graph_color[1],label=label[1])
      plt.plot(hist_r,color=graph_color[2],label=label[2])
      plt.xlim([0,(bins-1)])
      plt.legend()
    elif hist_plot_type=='lab':
      plt.plot(hist_l,color=graph_color[3],label=label[3])
      plt.plot(hist_m,color=graph_color[4],label=label[4])
      plt.plot(hist_y,color=graph_color[5],label=label[5])
      plt.xlim([0,(bins-1)])
      plt.legend()
    elif hist_plot_type=='hsv':
      plt.plot(hist_h,color=graph_color[6],label=label[6])
      plt.plot(hist_s,color=graph_color[7],label=label[7])
      plt.plot(hist_v,color=graph_color[8],label=label[8])
      plt.xlim([0,(bins-1)])
      plt.legend()
    elif hist_plot_type==None:
      pass
    else:
      fatal_error('Histogram Plot Type' + str(hist_plot_type) + ' is not "none", "all","rgb", "lab" or "hsv"!')
    
    if hist_plot_type != None:
      # Print plot
      fig_name = (str(filename[0:-4]) + '_' + str(hist_plot_type) + '_hist.svg')
      plt.savefig(fig_name)
      print('\t'.join(map(str, ('IMAGE', 'hist', fig_name))))
      if debug:
        fig_name=(str(device) +'_' + str(hist_plot_type) + '_hist.svg')
        plt.savefig(fig_name)
      plt.clf()
    
  # Generate Color Slice: Get Flattened RGB, LAB or HSV Histogram for Visualization     
  if cslice_type==None:
    pass
  elif cslice_type=='rgb':
    b_stack = np.vstack(hist_b)
    g_stack= np.vstack(hist_g)
    r_stack = np.vstack(hist_r)
  
    b_max=np.amax(b_stack)
    g_max=np.amax(g_stack)
    r_max=np.amax(r_stack)
    
    b_min=np.amin(b_stack)
    g_min=np.amin(g_stack)
    r_min=np.amin(r_stack)
    
    maximums=(b_max,g_max,r_max)
    minimums=(b_min,g_min,r_min)
    max_max=np.amax(maximums)
    min_min=np.amin(minimums)
    
    b_norm=((b_stack-min_min)/(max_max-min_min))*255
    g_norm=((g_stack-min_min)/(max_max-min_min))*255
    r_norm=((r_stack-min_min)/(max_max-min_min))*255
    
    norm_slice=np.dstack((b_norm,g_norm,r_norm))

  elif cslice_type=='hsv':
    h_stack = np.vstack(hist_h)
    s_stack= np.vstack(hist_s)
    v_stack = np.vstack(hist_v)
  
    h_max=np.amax(h_stack)
    s_max=np.amax(s_stack)
    v_max=np.amax(v_stack)
    
    h_min=np.amin(h_stack)
    s_min=np.amin(s_stack)
    v_min=np.amin(v_stack)
    
    maximums=(h_max,s_max,v_max)
    minimums=(h_min,s_min,v_min)
    max_max=np.amax(maximums)
    min_min=np.amin(minimums)
    
    h_norm=((h_stack-min_min)/(max_max-min_min))*255
    s_norm=((s_stack-min_min)/(max_max-min_min))*255
    v_norm=((v_stack-min_min)/(max_max-min_min))*255
    
    norm_slice=np.dstack((h_norm,s_norm,v_norm))

  elif cslice_type=='lab':
    l_stack = np.vstack(hist_l)
    m_stack= np.vstack(hist_m)
    y_stack = np.vstack(hist_y)
  
    l_max=np.amax(l_stack)
    m_max=np.amax(m_stack)
    y_max=np.amax(y_stack)
    
    l_min=np.amin(l_stack)
    m_min=np.amin(m_stack)
    y_min=np.amin(y_stack)
    
    maximums=(l_max,m_max,y_max)
    minimums=(l_min,m_min,y_min)
    max_max=np.amax(maximums)
    min_min=np.amin(minimums)
    
    l_norm=((l_stack-min_min)/(max_max-min_min))*255
    m_norm=((m_stack-min_min)/(max_max-min_min))*255
    y_norm=((y_stack-min_min)/(max_max-min_min))*255
    
    norm_slice=np.dstack((l_norm,m_norm,y_norm))
    
  else:
    fatal_error('Visualize Type' + str(visualize_type) + ' is not "None", "rgb","hsv" or "lab"!')
  
  if filename:
    # Print color-slice image
    out_file = str(filename[0:-4]) + '_' + str(cslice_type) + '_norm_slice.png'
    print_image(norm_slice, out_file)
    print('\t'.join(map(str, ('IMAGE', 'slice', out_file))))
  else:
    pass
  
  if debug:
    print_image(norm_slice, (str(device)+ '_'+ str(cslice_type)+ '_norm_slice.png'))

  # PseudoColor Image Based On l,A,B, H, S, or V Channel
  
  p_channel=pseudo_channel
  pseudocolor_img=1
  
  if p_channel==None:
    pass
    
  elif p_channel=='h':
    if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
      _pseudocolored_image(h_bin, bins, img, mask, 'white', p_channel, filename, resolution)
    
    if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
      _pseudocolored_image(h_bin, bins, img, mask, 'img', p_channel, filename, resolution)
    
  elif p_channel=='s':
    if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
      _pseudocolored_image(s_bin, bins, img, mask, 'white', p_channel, filename, resolution)
    
    if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
      _pseudocolored_image(s_bin, bins, img, mask, 'img', p_channel, filename, resolution)
    
  elif p_channel=='v':
    if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
      _pseudocolored_image(v_bin, bins, img, mask, 'white', p_channel, filename, resolution)
    
    if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
      _pseudocolored_image(v_bin, bins, img, mask, 'img', p_channel, filename, resolution)
    
  elif p_channel=='l':
    if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
      _pseudocolored_image(l_bin, bins, img, mask, 'white', p_channel, filename, resolution)
    
    if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
      _pseudocolored_image(l_bin, bins, img, mask, 'img', p_channel, filename, resolution)
    
  elif p_channel=='m':
    if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
      _pseudocolored_image(m_bin, bins, img, mask, 'white', p_channel, filename, resolution)
    
    if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
      _pseudocolored_image(m_bin, bins, img, mask, 'img', p_channel, filename, resolution)
    
  elif p_channel=='y':
    if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
      _pseudocolored_image(y_bin, bins, img, mask, 'white', p_channel, filename, resolution)
    
    if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
      _pseudocolored_image(y_bin, bins, img, mask, 'img', p_channel, filename, resolution)
    
  else:
    fatal_error('Pseudocolor Channel' + str(pseudo_channel) + ' is not "None", "l","m", "y", "h","s" or "v"!')
  
  if p_channel!=None:
    if os.path.isfile(('1_vis_pseudocolor_colorbar_' + str(pseudo_channel) + '_channel.svg')):
      pass
    else:
      filename1=str(filename)
      name_array=filename1.split("/")
      filename2="/".join(map(str,name_array[:-1]))
      fig = plt.figure()
      ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
      valmin=-0
      valmax=(bins-1)
      norm=colors.Normalize(vmin=valmin, vmax=valmax)
      cb1=colorbar.ColorbarBase(ax1,cmap=cm.jet, norm=norm, orientation='horizontal')
      fig_name=str(filename2)+'/1_vis_pseudocolor_colorbar_' + str(pseudo_channel) + '_channel.svg'
      fig.savefig(fig_name,bbox_inches='tight')
      fig.clf()
  
  return device, hist_header, hist_data, norm_slice