import pandas as pd
import numpy as np


def constellaqc(denovo_groups, annotated_groups, debug):

    """plmConstellaQC: Compare de novo annotations of Constella to known standards in order to estimate error rates

    Inputs:
    denovo_groups    = A pandas array representing homology groups predicted by Constella for plms
    annotated_groups = A pandas array representing the true biological identities of plms
    debug		     = Debugging mode enabled/disabled for use in troubleshooting


    :param denovo_groups: pandas.core.frame.DataFrame
    :param annotated_groups: pandas.core.frame.DataFrame
    :param debug: bool

    """

    known_feat=np.unique(annotated_groups.loc[:,'group'])
    pred_group=np.unique(denovo_groups.loc[:,'group'])

    scores=[]

    for anno in known_feat:
        anno_bool_index=annotated_groups.loc[:,'group']==anno
        anno_group_calls=denovo_groups.loc[annotated_groups.loc[:,'group']==anno, 'group'].values
        #print(anno, 'count: ', np.sum(anno_bool_index))
        score_row=[]
        for denovo in pred_group:
            score_row.append(np.sum(anno_group_calls==denovo))
        scores.append(score_row)

    scores=pd.DataFrame(scores, index=known_feat, columns=pred_group)

    if debug == True:
        print('Known Feature-Predicted Group Scoring Matrix:\n')
        print(scores)

    anno_sum=[]; anno_no=[]; anno_error=[]; ni=[];

    for anno in known_feat:
        anno_sum.append(np.sum(scores.loc[anno,:].values))
        anno_no.append(np.sum(scores.loc[anno,:].values!=0))
        anno_error.append(np.sum(scores.loc[anno,:].values!=0)-1)
        ni.append(1)
    pred_sum=[]; pred_no=[]; pred_error=[]; nj=[];

    for denovo in pred_group:
        pred_sum.append(np.sum(scores.loc[:,denovo].values))
        pred_no.append(np.sum(scores.loc[:,denovo].values!=0))
        pred_error.append(np.sum(scores.loc[:,denovo].values!=0)-1)
        nj.append(1)

    anno_valid=np.array(anno_sum)-ni-np.array(anno_error)
    pred_valid=np.array(pred_sum)-nj-np.array(pred_error)

    VSum=np.sum(anno_valid)
    SSum=np.sum(anno_error)
    CSum=np.sum(pred_error)
    Total=VSum+SSum+CSum


    print('\n\nValid Call Rate:     ', round(100*(VSum/Total),2), '%')
    print('Splitting Call Rate: ', round(100*(SSum/Total),2), '%')
    print('Clumping Call Rate:  ', round(100*(CSum/Total),2), '%')
