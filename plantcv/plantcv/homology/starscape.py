# Generate a plm multivariate space for downstream use in homology group assignments

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np
from plantcv.plantcv import params


def starscape(cur_plms, group_a, group_b, outfile_prefix):
    """
    Principal Component Analysis on pseudo-landmark data between two timepoints

    Inputs:
    cur_plms        = A pandas array of plm multivariate space representing capturing two adjacent frames in a
                      time series or otherwise analogous dataset in order to enable homology assignments
    group_a         = Name of group A (timepoint 1)
    group_b         = Name of group B (timepoint 2)
    outfile_prefix  = User defined file path and prefix name for PCA output graphics

    Outputs:
    final_df        = Output dataframe
    eigenvals       = PCA eigen values
    loadings        = PCA loadings

    :param cur_plms: pandas.core.frame.DataFrame
    :param group_a: str
    :param group_b: str
    :param outfile_prefix: str
    :return final_df: pandas.core.frame.DataFrame
    :return eigenvals: numpy.ndarray
    :return loadings: pandas.core.frame.DataFrame
    """
    init_comps = 4

    # Store names of our features/dimensions used to generate our PCA
    features = cur_plms.columns[3:len(cur_plms.columns)].tolist()

    # Remove label columns prior to running PCA
    x = cur_plms.loc[:, features].values
    # Rescale dataframe values
    scaler = StandardScaler()
    scaler.fit(x)
    x_scaled = scaler.transform(x)

    # Set initial number of components to fit PC space to
    pca2 = PCA(init_comps)
    # Fit PCA space to rescaled dataframe
    pca2.fit(x_scaled)

    # Store eigenvalues
    eigenvals = pca2.explained_variance_
    # Store variance explained by each component
    var_exp = pca2.explained_variance_ratio_

    if params.debug is not None:
        # Print cumulative variance explained by each component
        print('Eigenvalues: ', eigenvals, '\n\n')
        # Print cumulative variance explained by each component
        print('Var. Explained: ', var_exp, '\n\n')
        # Print cumulative variance explained by each component
        print('Cumul. Var. Explained: ', np.cumsum(pca2.explained_variance_ratio_), '\n\n')

    # Store the number of informative components required to surpass cutoff
    informative_comps = sum(eigenvals > 1)

    print(informative_comps, ' components sufficiently informative')

    # Rerun PCA to extract informative components specifically
    pca = PCA(informative_comps)
    # Fit Second PCA space to rescaled dataframe
    pca.fit(x_scaled)

    principal_components = pca.fit_transform(x)

    principal_df = pd.DataFrame(data=principal_components,
                                columns=["PC" + str(i) for i in range(1, informative_comps + 1)])
    cur_plm_names = pd.DataFrame(cur_plms.loc[:, 'plmname'].values)
    cur_plm_names.columns = ['plmname']
    cur_filenames = pd.DataFrame(cur_plms.loc[:, 'filename'].values)
    cur_filenames.columns = ['filename']

    final_df = pd.concat([cur_plm_names, cur_filenames, principal_df], axis=1)

    loadings = pd.DataFrame(pca.components_.T, columns=["PC" + str(i) for i in range(1, informative_comps + 1)],
                            index=features)

    if params.debug is not None:
        # Generate Screeplot for PCA of plm space
        plt.figure()
        plt.plot(np.arange(1, len(eigenvals) + 1), eigenvals)
        plt.hlines(1, 1, len(eigenvals) + 1, linestyles='dotted', color='r')
        plt.title('Screeplot for Principal Components of plm Space')
        plt.xlabel('Number of Components', fontsize=12)
        plt.ylabel('Eigenvalues', fontsize=12)

        if params.debug == 'print':
            plt.savefig(f"{outfile_prefix}_screeplot.png", dpi=params.dpi)
            plt.close()
        elif params.debug == 'plot':
            # Use non-blocking mode in case the function is run more than once
            plt.show(block=False)

        # Plot principal components
        plt.figure()
        targets = [group_a, group_b]
        colors = ['r', 'b']
        if informative_comps >= 3:
            # 3D plot of first 3 PCA dimensions
            prcomp = plt.axes(projection='3d')
            # Set axis labels
            prcomp.set_xlabel('Principal Component 1')
            prcomp.set_ylabel('Principal Component 2')
            prcomp.set_zlabel('Principal Component 3')

            indices_to_keep = final_df['filename'] == targets[0]
            prcomp.scatter3D(final_df.loc[indices_to_keep, 'PC1'],
                             final_df.loc[indices_to_keep, 'PC2'],
                             final_df.loc[indices_to_keep, 'PC3'], c=colors[0])

            indices_to_keep = final_df['filename'] == targets[1]
            prcomp.scatter3D(final_df.loc[indices_to_keep, 'PC1'],
                             final_df.loc[indices_to_keep, 'PC2'],
                             final_df.loc[indices_to_keep, 'PC3'], c=colors[1])
        elif informative_comps == 2:
            # 2D plot of First 2 PCA dimensions
            indices_to_keep = final_df['filename'] == targets[0]
            plt.scatter(final_df.loc[indices_to_keep, 'PC1'], final_df.loc[indices_to_keep, 'PC2'], c=colors[0])

            indices_to_keep = final_df['filename'] == targets[1]
            plt.scatter(final_df.loc[indices_to_keep, 'PC1'], final_df.loc[indices_to_keep, 'PC2'], c=colors[1])

            plt.xlabel('Principal Component 1')
            plt.ylabel('Principal Component 2')

        if params.debug == "print":
            plt.savefig(f"{outfile_prefix}_PCspace.png", dpi=params.dpi)
            plt.close()
        elif params.debug == "plot":
            plt.show(block=False)

    return final_df, eigenvals, loadings
