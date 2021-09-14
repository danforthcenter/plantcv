# Generate a plm multivariate space for downstream use in homology group assignments

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np

def starscape(cur_plms, groupA, groupB, outfile_prefix, debug):

    init_comps=4
    cutoff=0.99

    """plmSpace: Generate a plm multivariate space for downstream use in homology group assignments

    Inputs:
    cur_plms        = A pandas array of plm multivariate space representing capturing two adjacent frames in a 
                      time series or otherwise analogous dataset in order to enable homology assignments
    groupA
    groupB
    comps           = User defined number of principal components to retrieve
    outfile_prefix  = User defined file path and prefix name for PCA output graphics
    debug           = Debugging mode enabled/disabled for use in troubleshooting


    :param cur_plms: pandas.core.frame.DataFrame
    :param debug: bool

    """
    
    #Store names of our features/dimensions used to generate our PCA
    features = cur_plms.columns[3:len(cur_plms.columns)].tolist()

    #Remove label columns prior to running PCA
    x = cur_plms.loc[:, features].values
    #Rescale dataframe values 
    scaler = StandardScaler()
    scaler.fit(x)
    x_scaled=scaler.transform(x)

    #Set initial number of components to fit PC space to
    pca2 = PCA(init_comps)
    #Fit PCA space to rescaled dataframe
    pca2.fit(x_scaled)

    #Store eigenvalues
    eigenvals=pca2.explained_variance_
    #Store variance explained by each component
    var_exp=pca2.explained_variance_ratio_

    if debug==True:
        #Print cumulative variance explained by each component
        print('Eigenvalues: ', eigenvals, '\n\n')
        #Print cumulative variance explained by each component
        print('Var. Explained: ', var_exp, '\n\n')
        #Print cumulative variance explained by each component
        print('Cumul. Var. Explained: ', np.cumsum(pca2.explained_variance_ratio_), '\n\n')

    #Store the number of informative components required to surpass cutoff
    informative_comps=sum(eigenvals>1)

    print(informative_comps, ' components sufficiently informative')

    #Rerun PCA to extract informative components specifically
    pca = PCA(informative_comps)
    #Fit Second PCA space to rescaled dataframe
    pca.fit(x_scaled)

    principalComponents = pca.fit_transform(x)
    principalComponents
    principalDf = pd.DataFrame(data = principalComponents, columns = ["PC" + str(i) for i in range(1,informative_comps+1)])
    cur_plm_names=pd.DataFrame(cur_plms.loc[:,'plmname'].values)
    cur_plm_names.columns = ['plmname']
    cur_filenames=pd.DataFrame(cur_plms.loc[:,'filename'].values)
    cur_filenames.columns = ['filename']

    finalDf = pd.concat([cur_plm_names, cur_filenames, principalDf], axis = 1)

    loadings = pd.DataFrame(pca.components_.T, columns = ["PC" + str(i) for i in range(1,informative_comps+1)], index=features)

    #Generate Screeplot for PCA of plm space
    screeplot=plt.figure(figsize=(6, 6))
    screeplot = plt.plot(np.arange(1,len(eigenvals)+1), eigenvals)
    screeplot = plt.hlines(1, 1, len(eigenvals)+1, linestyles='dotted', color='r')
    screeplot = plt.title('Screeplot for Principal Components of plm Space')
    screeplot = plt.xlabel('Number of Components', fontsize = 12)
    screeplot = plt.ylabel('Eigenvalues', fontsize = 12)

    if debug==True:
        if outfile_prefix==None:
            plt.show(screeplot)
        else:
            plt.savefig(outfile_prefix+'_screeplot.png')

    plt.close()

    colors = ['r', 'b']

    if informative_comps>=3:
        #3D plot of First 3 PCA dimensions
        fig_PrComp = plt.figure(figsize=(8, 8))
        fig_PrComp = plt.axes(projection='3d')

        fig_PrComp.set_xlabel('Principal Component 1', fontsize = 14)
        fig_PrComp.set_ylabel('Principal Component 2', fontsize = 14)
        fig_PrComp.set_zlabel('Principal Component 3', fontsize = 14)

        targets = [groupA, groupB]

        indicesToKeep = finalDf['filename'] == targets[0]
        fig_PrComp.scatter3D(finalDf.loc[indicesToKeep, 'PC1'], 
                      finalDf.loc[indicesToKeep, 'PC2'], 
                      finalDf.loc[indicesToKeep, 'PC3'], c=colors[0]);

        indicesToKeep = finalDf['filename'] == targets[1]
        fig_PrComp.scatter3D(finalDf.loc[indicesToKeep, 'PC1'], 
                      finalDf.loc[indicesToKeep, 'PC2'], 
                      finalDf.loc[indicesToKeep, 'PC3'], c=colors[1]);
    elif informative_comps==2:
        #2D plot of First 2 PCA dimensions
        fig_PrComp = plt.figure(figsize=(8, 8))

        targets = [groupA, groupB]

        indicesToKeep = finalDf['filename'] == targets[0]
        fig_PrComp = plt.scatter(finalDf.loc[indicesToKeep, 'PC1'], 
                      finalDf.loc[indicesToKeep, 'PC2'], c=colors[0]);

        indicesToKeep = finalDf['filename'] == targets[1]
        fig_PrComp = plt.scatter(finalDf.loc[indicesToKeep, 'PC1'], 
                      finalDf.loc[indicesToKeep, 'PC2'], c=colors[1]);

        fig_PrComp = plt.xlabel('Principal Component 1', fontsize = 14)
        fig_PrComp = plt.ylabel('Principal Component 2', fontsize = 14)

    if debug==True:
        if outfile_prefix==None:
            plt.show(fig_PrComp)
        else:
            plt.savefig(outfile_prefix+'_PCspace.png')

    plt.close()

    return(finalDf, eigenvals, loadings)