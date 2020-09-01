# GMM Classifier

from plantcv import plantcv as pcv
import numpy as np
from plantcv.plantcv import params
import pickle
import os

def gmm_classifier(img, project_name="PlantCV", alias_file=""):
    """
    Train the GMM segmentation model

    Inputs:
    img             = An rgb image
    project_name    = This name is used to load the Guassian model.
    alias_file      =  A file of list to rename the individual clusters.  Default is blank (in which case,
                    clusters are simply number sequentially).

    Returns:
    output          =  Mask of full image with each component listed by color
    mask_alias      = Individual masks for each component

       :param img: numpy.ndarray
       :param project_name: str
       :param alias_file: str
       :param project_name: str
       :return output: numpy.ndarray
       :return mask_alias: numpy.ndarray
    """
    gmm = pickle.load(open(str(project_name)+"_GaussianMixtureModel.mdl", "rb"))
    colors = pickle.load(open(str(project_name)+"_colors.mdl", "rb"))
    num_components = pickle.load(open(str(project_name)+"_numberOfComponents.mdl", "rb"))
    remove = pickle.load(open(str(project_name)+"_removed.mdl", "rb"))

    zipped=[]

    h,w=img.shape[:2]
    for x in range(0,h):
        for y in range(0,w):
            zipped.append(img[x,y])

    zipped=np.array(zipped)

    if not len(remove)==0:
        remain_zipped=zipped[np.all(np.any((zipped-np.array(remove)[:, None]), axis=2), axis=0)]
    else:
        remain_zipped=zipped

    tbd_removed=[]
    tmp=remain_zipped.tolist()

    for i in range(0,len(tmp)):
        if tmp[i][0]==tmp[i][1]==tmp[i][2]:
           tbd_removed.append(i)

    tmp = [i for j, i in enumerate(tmp) if j not in tbd_removed]
    remain_zipped=np.array(tmp)
    dict_of_colors={}
    colormap={}

    labels = gmm.predict(remain_zipped)
    sub_mask=[]

    for x in range(len(remain_zipped)):
        colormap[str(remain_zipped[x])]=labels[x]

    for y in range(0,num_components):
            dict_of_colors[str(y)]=colors[y]
            sub_mask.append(np.zeros((h, w), np.uint8))

    output=np.zeros((h, w, 3), np.uint8)
    for x in range(0, h):
        for y in range(0, w):
            if img[x, y].tolist() in remove:
                output[x, y]=[0, 0, 0]
            elif img[x, y].tolist()[0]==img[x, y].tolist()[1]==img[x, y].tolist()[2]:
                output[x, y]=[0, 0, 0]
            else:
                tocheck=img[x, y]
                lab_=colormap[str(tocheck)]
                output[x, y]=(dict_of_colors[str(lab_)][2],
                             dict_of_colors[str(lab_)][1],
                             dict_of_colors[str(lab_)][0])

                sub_mask[lab_][x, y]=255

    params.device += 1
    if params.debug == 'print':
        fname = project_name + "_" + str(params.device) +"_Full_Image_Mask.png"
        name = os.path.join(params.debug_outdir, fname)
        pcv.print_image(output,name )
    elif params.debug == 'plot':
        pcv.plot_image(output)

    if alias_file=="":
        return output, sub_mask
    else:
        mask_alias={}
        with open(alias_file,"r") as file:
            for line in file:
                arr=line.split("\t")
                mask_alias[arr[1]]=sub_mask[int(arr[0])]
        return output, mask_alias

