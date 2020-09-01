# Train the GMM segmentation model

import os
from plantcv import plantcv as pcv
import cv2
import numpy as np
from plantcv.plantcv import params
from sklearn import mixture
import pickle


def gmm_segmentation_train(img, remove=[], num_components=4, project_name="PlantCV"):
    """
    Train the GMM segmentation model

    Inputs:
    img             = An rgb image
    remove          = Colors to ignore in the original when calculating the clusters.  For example,
                    the background color of the image.  This can substantially speed up calculations.
    num_components  =  The number of clusters of colors you wish to divide the image into.  (Default=4)
                    project_name: This will be used to name the output Gaussian model as well as images.


       :param img: numpy.ndarray
       :param remove: list
       :param num_components: int
       :param project_name: str
    """

    zipped=[]
    if type(img)==str:
        tmp_img=[]
        arr=img.split(",")
        for v in range(0,len(arr)):
            if not os.path.exists(arr[v]):
                raise NameError("File '" + str(arr[v]) + "' doesn't exist.")
            tmp_img.append(cv2.imread(arr[v], -1))
            h,w=tmp_img[v].shape[:2]
            for x in range(0, h):
                for y in range(0, w):
                    zipped.append(tmp_img[v][x, y])
    else:
        h,w=img.shape[:2]
        for x in range(0, h):
            for y in range(0, w):
                zipped.append(img[x, y])

    zipped=np.array(zipped)

    if not len(remove)==0:
        remain_zipped=zipped[np.all(np.any((zipped-np.array(remove)[:, None]), axis=2), axis=0)]
    else:
        remain_zipped=np.copy(zipped)

    tbd_removed=[]
    tmp=remain_zipped.tolist()

    for i in range(0,len(tmp)):
        if tmp[i][0]==tmp[i][1]==tmp[i][2]:
           tbd_removed.append(i)

    tmp = [i for j, i in enumerate(tmp) if j not in tbd_removed]
    remain_zipped=np.array(tmp)

    dict_of_colors={}
    colors = pcv.color_palette(num_components)
    colormap={}

    gmm = mixture.GaussianMixture(n_components=num_components).fit(remain_zipped)
    pickle.dump(gmm,open(str(project_name)+"_GaussianMixtureModel.mdl","wb"))
    pickle.dump(colors,open(str(project_name)+"_colors.mdl","wb"))
    pickle.dump(num_components,open(str(project_name)+"_numberOfComponents.mdl","wb"))
    pickle.dump(remove,open(str(project_name)+"_removed.mdl","wb"))
    labels = gmm.predict(remain_zipped)

    for x in range(len(remain_zipped)):
        colormap[str(remain_zipped[x])]=labels[x]

    for y in range(0,num_components):
        dict_of_colors[str(y)]=colors[y]



    if type(img)==str:
        output=[]
        submask=[]
        for v in range(0,len(arr)):
            submask.append(v)
            submask[v]=[]
            for y in range(0,num_components):
                submask[v].append(np.zeros((h,w),np.uint8))

            h,w=tmp_img[v].shape[:2]
            output.append(np.zeros((h,w,3),np.uint8))
            for x in range(0,h):
                for y in range(0,w):
                    if tmp_img[v][x,y].tolist() in remove:
                        output[v][x,y]=[0,0,0]
                    elif tmp_img[v][x,y].tolist()[0]==tmp_img[v][x,y].tolist()[1]==tmp_img[v][x,y].tolist()[2]:
                        output[v][x,y]=[0,0,0]
                    else:
                        tocheck=tmp_img[v][x,y]
                        lab_=colormap[str(tocheck)]
                        output[v][x,y]=(dict_of_colors[str(lab_)][2],
                                        dict_of_colors[str(lab_)][1],
                                        dict_of_colors[str(lab_)][0])

                        submask[v][lab_][x,y]=255
            params.device += 1
            if params.debug == 'print':
                pcv.print_image(output[v],project_name+"_"+str(params.device)+"_Train_Full_Image_Mask.png")
                for c in range(0,num_components):
                    pcv.print_image(submask[v][c],project_name+"_"+str(params.device)+"_submask_"+str(c)+".png")

            elif params.debug == 'plot':
                pcv.plot_image(output[v],project_name+"_"+str(params.device)+"_Train_Full_Image_Mask.png")
                for c in range(0,num_components):
                    pcv.plot_image(submask[v][c],project_name+"_"+str(params.device)+"_submask_"+str(c)+".png")


    else:
        output=np.zeros((h,w,3),np.uint8)
        submask=[]
        for y in range(0,num_components):
            submask.append(np.zeros((h,w),np.uint8))

        for x in range(0,h):
            for y in range(0,w):
                if img[x,y].tolist() in remove:
                    output[x,y]=[0,0,0]
                elif img[x,y].tolist()[0]==img[x,y].tolist()[1]==img[x,y].tolist()[2]:
                    output[x,y]=[0,0,0]
                else:
                    tocheck=img[x,y]
                    lab_=colormap[str(tocheck)]
                    output[x,y]=(dict_of_colors[str(lab_)][2],
                                 dict_of_colors[str(lab_)][1],
                                 dict_of_colors[str(lab_)][0])
                    submask[lab_][x,y]=255
        params.device += 1

        if params.debug == 'print':
            pcv.print_image(output,project_name+"_"+str(params.device)+"_Train_Full_Image_Mask.png")
            for c in range(0,num_components):
                pcv.print_image(submask[c],project_name+"_"+str(params.device)+"_submask_"+str(c)+".png")

        elif params.debug == 'plot':
            pcv.plot_image(output,project_name+"_"+str(params.device)+"_Train_Full_Image_Mask.png")
            for c in range(0,num_components):
                pcv.plot_image(submask[c],project_name+"_"+str(params.device)+"_submask_"+str(c)+".png")
