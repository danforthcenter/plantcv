"""Label ClickCount."""
import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.visualize import colorize_label_img
from plantcv.plantcv import outputs


def _clickcount_labels(counter):
    """Get the label names"""

    labels = list(counter.count)
    
    return labels


def clickcount_label(gray_img, counter, imgname='default'):
    """Labels ClickCount Output with Categories"""
    # gray_img - gray image with objects labeled (e.g.watershed output)
    # counter - ClickCount object
    # imagename - imagename or sample identification to add to output information
    
    debug = params.debug
    params.debug = None

    labelnames = _clickcount_labels(counter)
    
    dict_class_labels = {}
    
    for i, x in enumerate(labelnames):
        dict_class_labels[x] = i+1
    
    shape = np.shape(gray_img)
    class_label = np.zeros((shape[0], shape[1]), dtype=np.uint8)

    class_number = []
    class_name = []
    
    # Only keep watersed results that overlap with a clickpoint and do not ==0
    
    for cl in list(dict_class_labels.keys()):
        for (y, x) in counter.points[cl]:
            x = int(x)
            y = int(y)
            seg_label = gray_img[x, y]
            if seg_label != 0:
                class_number.append(seg_label)
                class_name.append(cl)
                class_label[gray_img == seg_label] = seg_label
    
    # Get corrected name
    
    corrected_number = []
    corrected_name = []
    
    for i, x in enumerate(class_number):
        if x in corrected_number:
            ind = (corrected_number.index(x))
            y = corrected_name[ind]+"_"+str(class_name[i])
            corrected_name[ind] = y
        else:
            corrected_number.append(x)
            y = str(class_name[i])
            corrected_name.append(y)
            
    classes = np.unique(corrected_name)
    class_dict = {}
    count_class_dict = {}
    
    for i, x in enumerate(classes):
        class_dict[x] = i+1
        count_class_dict[x] = corrected_name.count(x)
    
    corrected_label = np.zeros((shape[0], shape[1]), dtype=np.uint8)
    corrected_class = np.zeros((shape[0], shape[1]), dtype=np.uint8)
    

    for i, value in enumerate(corrected_number):
        if value != 0:
            corrected_label[gray_img == value] = i+1
            corrected_class[gray_img == value] = class_dict[corrected_name[i]]
            corrected_name[i] = str(i+1)+"_"+corrected_name[i]
    
    num = len(corrected_name)

    vis_labeled = colorize_label_img(corrected_label)
    vis_class = colorize_label_img(corrected_class)

    params.debug = debug
    _debug(visual=vis_labeled,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_corrected__labels_img.png'))
    _debug(visual=vis_class,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_corrected_class.png'))
    
    for i, x in enumerate(count_class_dict.keys()):
        variable = x
        value = count_class_dict[x]
        outputs.add_observation(sample=imgname, variable=variable, 
                                trait='count of category',
                                method='count', scale='count', datatype=int,
                                value=value, label=variable)
    

    return corrected_label, corrected_name, num
