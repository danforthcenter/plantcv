import os
from plantcv import plantcv as pcv
import cv2
import numpy as np
from plantcv.plantcv import params
from sklearn import mixture
from sklearn.cluster import MiniBatchKMeans
import pickle

def color_clustering_segmentation(img, project_name="PlantCV", alias_file="", algorithm="Gaussian"):
    """
    img: An rgb image
    project_name: This name is used to load the Guassian or Mini-Batch Kmeans model.
    alias_file: A file of a list of pixel color values to retreive particular clusters.  Default is blank (in which case,
               clusters are simply numbered sequentially).


    Returns:
        output          =  Mask of full image with each component listed by color
        mask_alias      =  Individual masks for each component

       :param img: numpy.ndarray
       :param project_name: str
       :param alias_file: str
       :param algorithm: str
       :return output: numpy.ndarray
       :return mask_alias: numpy.ndarray

    """

    gmm = pickle.load(open(os.path.join(params.debug_outdir, str(project_name)+"_"+algorithm+"_Model.mdl"), "rb"))
    colors = pickle.load(open(os.path.join(params.debug_outdir, str(project_name)+"_"+algorithm+"_colors.mdl"), "rb"))
    num_components = pickle.load(open(os.path.join(params.debug_outdir, str(project_name)+"_"+algorithm+"_numberOfComponents.mdl"), "rb"))
    remove=pickle.load(open(os.path.join(params.debug_outdir, str(project_name)+"_"+algorithm+"_removed.mdl"), "rb"))
    remove_grays=pickle.load(open(os.path.join(params.debug_outdir, str(project_name)+"_"+algorithm+"_removed_grays.mdl"),"rb"))

    zipped=[]

    h,w=img.shape[:2]
    for x in range(0,h):
        for y in range(0,w):
            zipped.append(img[x,y])

    zipped=np.array(zipped)

    if not len(remove)==0:
        for x in remove:
            remain_zipped=zipped[np.all(np.any((zipped-np.array(x,ndmin=2)[:, None]), axis=2), axis=0)]
    else:
        remain_zipped=zipped

    if remove_grays==True:
        for x in range(0,256):
            remain_zipped=remain_zipped[np.all(np.any((remain_zipped-np.array([x,x,x],ndmin=2)[:, None]), axis=2), axis=0)]


    dict_of_colors={}
    colormap={}

    if not alias_file=="":
        mask_alias={}
        with open(alias_file,"r") as file:
            header = file.readline()
            header = header.rstrip("\n")
            class_list = header.split("\t")
            mask_header={}

            for cls in class_list:
                mask_header[cls] = []

            for row in file:
                row = row.rstrip("\n")
                row = row.replace('"', '')
                if len(row) > 0:
                    points = row.split("\t")
                    for i, point in enumerate(points):
                       mask_header[class_list[i]].append(point)


        for key in mask_header.keys():
            final_temp_list=[]
            listtokeep=[]
            for i in mask_header[key]:
                temp=list(map(int, i.split(',')))
                final_temp_list.append(list((temp[2],temp[1],temp[0])))
            final_temp_list=np.array(final_temp_list,ndmin=2)

            remain_zipped=np.concatenate((remain_zipped,final_temp_list))

            labels = gmm.predict(remain_zipped)
            sub_mask=[]

            for x in range(len(remain_zipped)):
                colormap[str(remain_zipped[x])]=labels[x]

            for y in range(0,num_components):
                    dict_of_colors[str(y)]=colors[y]
                    sub_mask.append(np.zeros((h, w), np.uint8))

            for index in final_temp_list:
                listtokeep.append(int(colormap[str(index)]))

            listtokeep=str(max(set(listtokeep), key=listtokeep.count))

            output=np.zeros((h, w, 3), np.uint8)
            for x in range(0, h):
                for y in range(0, w):
                    if img[x, y].tolist() in remove:
                        output[x, y]=[0, 0, 0]
                    elif remove_grays==True and img[x, y].tolist()[0]==img[x, y].tolist()[1]==img[x, y].tolist()[2]:
                        output[x, y]=[0, 0, 0]
                    else:
                        tocheck=img[x, y]
                        lab_=colormap[str(tocheck)]
                        output[x, y]=(dict_of_colors[str(lab_)][2],
                                     dict_of_colors[str(lab_)][1],
                                     dict_of_colors[str(lab_)][0])

                        sub_mask[lab_][x, y]=255

            #concatenated_image=np.zeros((h, w), np.uint8)
            #for index in listtokeep:
    ##        concatenated_image = cv2.add(concatenated_image,sub_mask[int(index)])

            mask_alias[key]=sub_mask[int(listtokeep)]
        params.device += 1
        if params.debug == 'print':
            pcv.print_image(output, os.path.join(params.debug_outdir, project_name+"_"+algorithm+"_"+str(params.device)+"_Train_Full_Image_Mask.png"))
            for c in mask_alias.keys():
                pcv.print_image(mask_alias[c], os.path.join(params.debug_outdir, project_name+"_"+algorithm+"_"+str(params.device)+str(c)+".png"))

        elif params.debug == 'plot':
            pcv.plot_image(output)
            for c in mask_alias.keys():
                pcv.plot_image(mask_alias[c])

        return output, mask_alias


    else:
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
                elif remove_grays==True and img[x, y].tolist()[0]==img[x, y].tolist()[1]==img[x, y].tolist()[2]:
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
            pcv.print_image(output, os.path.join(params.debug_outdir, project_name+"_"+algorithm+"_"+str(params.device)+"_Train_Full_Image_Mask.png"))
            for c in range(0,num_components):
                pcv.print_image(sub_mask[c], os.path.join(params.debug_outdir, project_name+"_"+algorithm+"_"+str(params.device)+"_submask_"+str(c)+".png"))

        elif params.debug == 'plot':
            pcv.plot_image(output)
            for c in range(0,num_components):
                pcv.plot_image(sub_mask[c])

        return output, sub_mask