import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import cut_tree
from plantcv.plantcv import params


def constella(cur_plms, pc_starscape, group_iter, outfile_prefix):
    """
    Group pseudo-landmarks into homology groupings

    Inputs:
    cur_plms      = A pandas array of plm multivariate space representing capturing two adjacent frames in a
                    time series or otherwise analogous dataset in order to enable homology assignments
    pc_starscape  = PCA results from starscape
    group_iter    =
    outfile_prefix = User defined file path and prefix name for PCA output graphics

    :param cur_plms: pandas.core.frame.DataFrame
    :param pc_starscape: pandas.core.frame.DataFrame
    :param group_iter: int
    :param outfile_prefix: str
    """
    sanity_check_pos = 2  # Needs to point at days in image identifier!

    singleton_no = pc_starscape.shape[0]

    if params.debug is not None:
        print(f'{singleton_no} plms to group')

    plm_links = linkage(pc_starscape.loc[:, pc_starscape.columns[2:len(pc_starscape.columns)]].values, 'ward')

    # For n-1 to 2 leaves on the current hierarchical cluster dendrogram...
    for c in np.arange(singleton_no - 1, 2, -1):
        # Extract current number of clusters for the agglomeration step
        cutree = cut_tree(plm_links, n_clusters=c)
        # Generate a list of all current clusters identified
        group_list = np.unique(cutree)

        # For the current cluster being queried...
        for g in group_list:
            # Create list of current clusters row indices in pandas dataframe
            cur_index = [i for i, x in enumerate(cutree == g) if x]
            # Create list of current clusters present group identity assignments
            cur_index_id = np.array(cur_plms.iloc[cur_index, 0])
            # Are any of the plms in the current cluster unnamed, how many?
            empty_count = np.count_nonzero(cur_index_id is None)
            empty_index = [i for (i, v) in zip(cur_index, cur_plms.iloc[cur_index, 0].values is None) if v]
            # Are any of the plms in the current cluster already assigned an identity, what are those identities?
            unique_ids = np.unique(cur_index_id[np.array(cur_index_id) is not None])

            # If cluster is two unnamed plms exactly, assign this group their own identity as a pair
            if empty_count == 2:
                pair_names = cur_plms.iloc[empty_index, 1].values
                # Sanity check! Pairs must be on different days
                if pair_names[0].split('_')[sanity_check_pos] != pair_names[1].split('_')[sanity_check_pos]:
                    cur_plms.iloc[empty_index, 0] = group_iter
                    group_iter = group_iter + 1
                else:
                    cur_plms.iloc[empty_index[0], 0] = group_iter
                    cur_plms.iloc[empty_index[1], 0] = group_iter + 1
                    group_iter = group_iter + 2

            # For the identities that already exist...
            for ID in unique_ids:
                # If only one plm assigned a name in current cluster and a second unnamed plm exists
                # transfer ID over to create a pair
                if np.count_nonzero(np.array(cur_index_id) == ID) < 2 and empty_count == 1:
                    # Store boolean positions for plms with IDs matching current ID out of current cluster
                    match_ids = [i for i, x in enumerate(cur_plms.iloc[cur_index, 0].values == ID) if x]
                    # Store boolean positions for plms which are unnamed out of current cluster
                    null_ids = [i for i, x in enumerate(cur_plms.iloc[cur_index, 0].values is None) if x]
                    # If exactly 1 matching ID and 1 null ID (i.e. 2 plms total)
                    # continue to pass ID name to the unnamed plm
                    if len(match_ids) + len(null_ids) == 2:
                        # Sanity check! Pairs must be on different days
                        pair_names = cur_plms.iloc[[cur_index[i] for i in match_ids + null_ids], 1].values
                        if pair_names[0].split('_')[sanity_check_pos] != pair_names[1].split('_')[sanity_check_pos]:
                            # Transfer identities to the unnamed plm
                            cur_plms.iloc[[cur_index[i] for i in null_ids], 0] = ID

    # Now that all groups that can be linked are formed, name rogues...
    rogues = [i for i, x in enumerate(cur_plms.loc[:, 'group'].values is None) if x]
    for rogue in rogues:
        cur_plms.iloc[[rogue], 0] = group_iter
        group_iter = group_iter + 1

    grpnames = cur_plms.loc[:, ['group']].values
    plmnames = cur_plms.loc[:, ['plmname']].values

    labelnames = []

    for li in range(0, len(plmnames)):
        labelnames.append(''.join(plmnames[li] + ' (' + str(int(grpnames[li])) + ')'))

    if params.debug is not None:
        plt.figure()
        plt.title('')
        plt.xlabel('')
        plt.ylabel('')
        dendrogram(plm_links, color_threshold=100, orientation="left", leaf_font_size=10, labels=np.array(labelnames))
        plt.tight_layout()

        if params.debug == "print":
            plt.savefig(outfile_prefix + '_plmHCA.png')
            plt.close()
        elif params.debug == "plot":
            plt.show()

    return cur_plms, group_iter
