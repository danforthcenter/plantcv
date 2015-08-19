### Analyze signal data in NIR image
import os
import cv2
import numpy as np
from . import print_image


def analyze_NIR_intensity(img, imgname, mask, bins, device, histplot=False,debug=False, filename=False):
  # This function calculates the intensity of each pixel associated with the plant and writes the values out to a file
  # Can also print out a histogram plot of pixel intensity and a pseudocolor image of the plant
  # img = input image
  # imgname = name of input image 
  # mask = mask made from selected contours
  # bins = number of classes to divide spectrum into
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print data and histograms
  # filename= False or image name. If defined print image

  device += 1
  
  ori_img=np.copy(img)
  
  if len(np.shape(img))==3:
    ix,iy,iz = np.shape(img)
    size = ix,iy
  else:
    ix,iy = np.shape(img)
    size = ix, iy
  
  # Make empty images, background is a black backdrop and w_back is a white backdrop  
  background = np.zeros(size, dtype=np.uint8)
  w_back=background+255
  
  # apply plant shaped mask to image
  masked=cv2.bitwise_and(img,img, mask=mask)

  # allow user to choose number of bins
  nir_bin=masked/(256/bins)
  
  # calculate histogram
  hist_nir= cv2.calcHist([nir_bin],[0],mask,[bins], [0,(bins-1)])
  hist_data_nir=[l[0] for l in hist_nir]
  
  # make hist percentage for plotting
  pixels = cv2.countNonZero(mask)
  hist_percent = (hist_nir/pixels) * 100
  hist_data_percent=[l[0] for l in hist_percent]
    
  # report histogram data
  hist_header=(
    'HEADER_HISTOGRAM',
    'bin-number',
    'signal',
    'hist_percent_100'
    )
  
  hist_data= (
    'NIR_DATA',
    bins,
    hist_data_nir,
    hist_data_percent
    )
  
  analysis_img=[]
  
  if filename!=False:
    #make mask to select the background
    mask_inv=cv2.bitwise_not(mask)
    img_back=cv2.bitwise_and(img,img, mask=mask_inv)
    img_back3=np.dstack((img_back,img_back,img_back))
  
    # mask the background and color the plant with color scheme 'jet'
    cplant = cv2.applyColorMap(masked, colormap=2)
    cplant1=cv2.bitwise_and(cplant,cplant, mask=mask)
    cplant_back=cv2.add(cplant1,img_back3)
    
    fig_name_pseudo =(str(filename[0:-4]) + '_nir_pseudo_col.png')
    print_image(cplant_back, fig_name_pseudo)
    analysis_img.append(['IMAGE', 'pseudo', fig_name_pseudo])
  
  if filename!=False and (histplot==True or debug):
    import matplotlib
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm
    from matplotlib import colors as colors
    from matplotlib import colorbar as colorbar
    import pylab as pl
  
    if histplot==True:
      # plot hist percent
      hist_plot_nir=plt.plot(hist_percent, color = 'green', label = 'Signal Intensity')
      xaxis=plt.xlim([0,(bins-1)])
      plt.xlabel(('Grayscale pixel intensity (0-'+str(bins)+")"))
      plt.ylabel('Proportion of pixels (%)')
      fig_name_hist=(str(filename[0:-4]) + '_nir_hist.png')
      plt.savefig(fig_name_hist)
      plt.clf()
      analysis_img.append(['IMAGE', 'hist', fig_name_hist])
      print('\t'.join(map(str, ('IMAGE', 'hist', fig_name_hist))))
  
    if debug:
      print_image(cplant1,(str(device)+"_nir_pseudo_plant.png"))
      print_image(img_back3,(str(device)+"_nir_pseudo_background.png"))
      print_image(cplant_back,(str(device)+"_nir_pseudo_plant_back.png"))
  
      filename1=str(filename)
      name_array=filename1.split("/")
      filename2="/".join(map(str,name_array[:-1]))
      fig = plt.figure()
      ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
      valmin=-0
      valmax=(bins-1)
      norm=colors.Normalize(vmin=valmin, vmax=valmax)
      cb1=colorbar.ColorbarBase(ax1,cmap=cm.jet, norm=norm, orientation='horizontal')
      fig_name=str(filename2)+'/NIR_pseudocolor_colorbar.svg'
      fig.savefig(fig_name,bbox_inches='tight')
    fig.clf()
    
  return device, hist_header, hist_data,analysis_img



#def analyze_NIR_intensity(img, imgname, mask, bins, device, debug=False, filename=False):
#  # This function calculates the intensity of each pixel associated with the plant and writes the values out to a file
#  # Can also print out a histogram plot of pixel intensity and a pseudocolor image of the plant
#  # img = input image
#  # imgname = name of input image 
#  # mask = mask made from selected contours
#  # bins = number of classes to divide spectrum into
#  # device = device number. Used to count steps in the pipeline
#  # debug = True/False. If True, print data and histograms
#  # filename= False or image name. If defined print image
#  
#  device += 1
#  ix,iy = np.shape(img)
#  size = ix,iy
#  background = np.zeros(size, dtype=np.uint8)
#  w_back=background+255
#  ori_img=np.copy(img)
#  
#  masked=cv2.bitwise_and(img,img, mask=mask)
#  
#  nir_bin=img/(256/bins)
#  hist_nir= cv2.calcHist([nir_bin],[0],mask,[bins], [0,(bins-1)])
#  pixels = cv2.countNonZero(mask)
#  hist_nir = (hist_nir/pixels) * 100
#  hist_data_nir=[l[0] for l in hist_nir]
#  
#  hist_header=(
#    'HEADER_HISTOGRAM',
#    'bin-number',
#    'signal'
#    )
#  
#  hist_data= (
#    'NIR_DATA',
#    bins,
#    hist_data_nir
#    )
#  
#  hist_plot_nir=plt.plot(hist_nir, color = 'red', label = 'Signal Intensity')
#  xaxis=plt.xlim([0,(bins-1)])
#  plt.xlabel('Grayscale pixel intensity (0-255)')
#  plt.ylabel('Proportion of pixels (%)')
#  fig_name_hist=(str(filename[0:-4]) + '_nir_hist.png')
#  plt.savefig(fig_name_hist)
#  plt.clf()
#  print('\t'.join(map(str, ('IMAGE', 'hist', fig_name_hist))))
# 
# 
#  # Normalize histogram data
#  h_max=np.amax(hist_data_nir)
#  h_min=np.amin(hist_data_nir)
#  h_norm=((h_min)/(h_max-h_min))*255
#  
#  #Make Pseudo colored image
#  
#  mask_inv=cv2.bitwise_not(mask)
#  # mask the background and color the plant with color scheme 'summer' see cmap/applyColorMap fxn
#  plant = cv2.bitwise_and(img, mask)
#  cplant = cv2.applyColorMap(plant, colormap =2)
#  # need to make the mask 3 dimensional if you want to mask the image because the pseudocolor image is now ~RGB
#  mask3 = np.dstack((mask, mask, mask))
#  # mask the image
#  col_msk_plant = cv2.bitwise_and(cplant, cplant, mask = mask)
#  # mask the plant out of the background using the inverse make
#  bkg = cv2.bitwise_and(img,img,mask=mask_inv)
#  bkg3 = np.dstack((bkg, bkg, bkg))
#  # overlay the masked images
#  final_pseudo = cv2.add(col_msk_plant, bkg3)
#  fig_name_pseudo =(str(filename[0:-4]) + '_nir_pseudo_col.png')
#  cv2.imwrite(fig_name_pseudo, final_pseudo)
#  print('\t'.join(map(str, ('IMAGE', 'pseudo', fig_name_pseudo))))
#  
#  #print a colorbar which can be associated with pseudo image
#  if debug:
#    plt.imshow(final_pseudo, cmap='jet')
#    plt.colorbar(orientation='horizontal')
#    plt.axis('off')
#    fig_name=('NIR' + '_colorbar_' + imgname)
#    plt.savefig(fig_name, dpi=600)
#  plt.clf()
#  
#  return device, hist_header, hist_data, h_norm