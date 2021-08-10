import os
from plantcv import plantcv as pcv
import cv2
import numpy as np
from plantcv.plantcv import params
from sklearn import mixture
from sklearn.cluster import MiniBatchKMeans
import operator, random
import pickle

def color_clustering_train(img, remove=[], num_components=4, project_name="PlantCV", algorithm="Gaussian", remove_grays=False, sample_pixels=0, sample_pixel_file="alias_file.txt"):
    """
    img: An rgb image
    remove: Colors to ignore in the original when calculating the clusters.  For example,
            the background color of the image.  This can substantially speed up calculations.
    num_components: The number of clusters of colors you wish to divide the image into.  (Default=4)
    project_name: This will be used to name the output Gaussian model as well as images.

       :param img: numpy.ndarray
       :param remove: 2d List
       :param num_components: int
       :param sample_pixels: int
       :param remove_grays: binary
       :param project_name: str
       :param sample_pixel_file: str
       :param algorithm: str

    """

    chosen_algorithm={"Gaussian":mixture.GaussianMixture(n_components=num_components),
                "Kmeans":MiniBatchKMeans(n_clusters=num_components)}

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
        for x in remove:
            remain_zipped=zipped[np.all(np.any((zipped-np.array(x,ndmin=2)[:, None]), axis=2), axis=0)]
    else:
        remain_zipped=zipped

    if remove_grays==True:
        for x in range(0,256):
            remain_zipped=remain_zipped[np.all(np.any((remain_zipped-np.array([x,x,x],ndmin=2)[:, None]), axis=2), axis=0)]

    dict_of_colors={}
    colors = pcv.color_palette(num_components)
    colormap={}

    gmm = chosen_algorithm[algorithm].fit(remain_zipped)
    pickle.dump(gmm,open(os.path.join(params.debug_outdir,str(project_name)+"_"+algorithm+"_Model.mdl"),"wb"))
    pickle.dump(colors,open(os.path.join(params.debug_outdir,str(project_name)+"_"+algorithm+"_colors.mdl"),"wb"))
    pickle.dump(num_components,open(os.path.join(params.debug_outdir,str(project_name)+"_"+algorithm+"_numberOfComponents.mdl"),"wb"))
    pickle.dump(remove,open(os.path.join(params.debug_outdir,str(project_name)+"_"+algorithm+"_removed.mdl"),"wb"))
    pickle.dump(remove_grays,open(os.path.join(params.debug_outdir,str(project_name)+"_"+algorithm+"_removed_grays.mdl"),"wb"))
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
            h,w=tmp_img[v].shape[:2]
            for y in range(0,num_components):
                submask[v].append(np.zeros((h,w),np.uint8))

            output.append(np.zeros((h,w,3),np.uint8))
            for x in range(0,h):
                for y in range(0,w):
                    if tmp_img[v][x,y].tolist() in remove:
                        output[v][x,y]=[0,0,0]
                    elif tmp_img[v][x,y].tolist()[0]==tmp_img[v][x,y].tolist()[1]==tmp_img[v][x,y].tolist()[2] and remove_grays==True:
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
                pcv.print_image(output[v], os.path.join(params.debug_outdir, project_name+"_"+algorithm+"_"+str(params.device)+"_Train_Full_Image_Mask.png"))
                for c in range(0,num_components):
                    pcv.print_image(submask[v][c], os.path.join(params.debug_outdir, project_name+"_"+algorithm+"_"+str(params.device)+"_submask_"+str(c)+".png"))

            elif params.debug == 'plot':
                pcv.plot_image(output[v])
                for c in range(0,num_components):
                    pcv.plot_image(submask[v][c])


    else:
        output=np.zeros((h,w,3),np.uint8)
        submask=[]
        for y in range(0,num_components):
            submask.append(np.zeros((h,w),np.uint8))

        for x in range(0,h):
            for y in range(0,w):
                if img[x,y].tolist() in remove:
                    output[x,y]=[0,0,0]
                elif img[x,y].tolist()[0]==img[x,y].tolist()[1]==img[x,y].tolist()[2] and remove_grays==True:
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
            pcv.print_image(output, os.path.join(params.debug_outdir, project_name+"_"+algorithm+"_"+str(params.device)+"_Train_Full_Image_Mask.png"))
            for c in range(0,num_components):
                pcv.print_image(submask[c], os.path.join(params.debug_outdir, project_name+"_"+algorithm+"_"+str(params.device)+"_submask_"+str(c)+".png"))

        elif params.debug == 'plot':
            pcv.plot_image(output)
            for c in range(0,num_components):
                pcv.plot_image(submask[c])

    if sample_pixels != 0:
        listofcolors=[]
        mode=False
        with open(os.path.join(params.debug_outdir, sample_pixel_file),'w+') as filetowrite:
            for x in range(num_components):
                listofcolors.append([])
                if x < num_components-1:
                    filetowrite.write("Submask_"+str(x)+"\t")
                else:
                    filetowrite.write("Submask_"+str(x)+"\n")
            #filetowrite.write("\n")

            if type(sample_pixels)==str:

                if sample_pixels.lower()=="means":
                    means= {"Gaussian":gmm.means_,
                            "Kmeans":gmm.cluster_centers_}
                    centers=means[algorithm]
                    for line in range(num_components):
                        listofcolors[line].append(tuple((centers[line][2],centers[line][1],centers[line][0])))

                elif "most" in sample_pixels.lower() or "least" in sample_pixels.lower():
                    alreadydone=[]
                    multiplier={"most":True,"least":False}
                    countofcolors={}
                    for x in range(num_components):
                        countofcolors[x]={}
                    mode=[str(s) for s in sample_pixels.split() if s.isalpha()][0].lower()
                    sample_pixels=[int(s) for s in sample_pixels.split() if s.isdigit()][0]
                    for line in colormap.keys():
                        if not line in alreadydone:
                            alreadydone.append(line)
                            formattedline=line
                            formattedline=formattedline.lstrip("[")
                            formattedline=formattedline.rstrip("]")
                            formattedline=[int(s) for s in formattedline.split() if s.isdigit()]
                            count=np.count_nonzero(np.all(img==[formattedline[0],formattedline[1],formattedline[2]],axis=2))
                            countofcolors[colormap[line]][tuple((formattedline[2],formattedline[1],formattedline[0]))]=count

                    for x in range(num_components):
                        sorted_list=sorted(countofcolors[x].items(), key=operator.itemgetter(1), reverse=multiplier[mode])[:sample_pixels]
                        for y in range(sample_pixels):
                            listofcolors[x].append(tuple((sorted_list[y][0][2],sorted_list[y][0][1],sorted_list[y][0][0])))

                elif "random" in sample_pixels.lower():
                    mode=True
                    sample_pixels=[int(s) for s in sample_pixels.split() if s.isdigit()][0]
                    for line in colormap.keys():
                        formattedline=line
                        formattedline=formattedline.lstrip("[")
                        formattedline=formattedline.rstrip("]")
                        formattedline=[int(s) for s in formattedline.split() if s.isdigit()]
                        listofcolors[colormap[line]].append(tuple((formattedline[2],formattedline[1],formattedline[0])))

            else:
                for line in colormap.keys():
                    formattedline=line
                    formattedline=formattedline.lstrip("[")
                    formattedline=formattedline.rstrip("]")
                    formattedline=[int(s) for s in formattedline.split() if s.isdigit()]
                    listofcolors[colormap[line]].append(tuple((formattedline[2],formattedline[1],formattedline[0])))

            for x in range(sample_pixels):
                for y in range(num_components):
                    x1=random.choice(range(len(listofcolors[y])))
                    try:
                        if mode==True:
                            if y < num_components-1:
                                filetowrite.write(str(listofcolors[y][x1][0])+","+str(listofcolors[y][x1][1])+","+str(listofcolors[y][x1][2])+"\t")
                            else:
                                filetowrite.write(str(listofcolors[y][x1][0])+","+str(listofcolors[y][x1][1])+","+str(listofcolors[y][x1][2])+"\n")
                        else:
                            if y < num_components-1:
                                filetowrite.write(str(listofcolors[y][x][0])+","+str(listofcolors[y][x][1])+","+str(listofcolors[y][x][2])+"\t")
                            else:
                                filetowrite.write(str(listofcolors[y][x][0])+","+str(listofcolors[y][x][1])+","+str(listofcolors[y][x][2])+"\n")
                    except IndexError:
                        if y < num_components-1:
                            filetowrite.write("\t")
                        else:
                            filetowrite.write("\n")
                #filetowrite.write("\n")





