import pickle
from SPICE import *
import matplotlib.pyplot as plt


def main():

    # load the data from the pickle file
    f = open('hsi_data.pkl', 'rb')
    hsi_file = pickle.load(f)
    hsi = hsi_file['hsi']
    valid_mask = hsi['valid_mask'].astype(bool)

    # trim the noisy bands
    hsi_image = hsi['Data'][:, :, 4:-4]
    img_shape = hsi_image.shape
    n_r, n_c, n_b = hsi_image.shape

    # load the wavelength information
    wvl = hsi['info']['wavelength'][4:-4]
    # reshape the data because SPICE takes an MxN array, not a full HSI cube
    hsi_image = np.reshape(hsi_image, (img_shape[0]*img_shape[1], img_shape[2]))
    valid_array = np.reshape(valid_mask, (img_shape[0]*img_shape[1],))
    # take the hsi data at the "valid" points
    M = hsi_image[valid_array, :]

    # since analyzing the image will take a long time, we will down sample the data for the sake of this demo
    input_data = M.T.astype(float)
    ds_data = input_data[:, ::20]

    # get the default parameters from the SPICE.py file
    params = SPICEParameters()

    # run the spice algorithm on the down sampled data
    [endmembers, ds_proportions] = SPICE(ds_data, params)

    # prompt the user to see if they would like to graph the output
    if input('Would you like to plot the output? (Y/n): ') == 'n':
        return

    # plot the wavelength versus the reflectance
    n_em = endmembers.shape[1]
    plt.plot(wvl, endmembers)
    plt.xlabel('wavelength (nm)')
    plt.ylabel('reflectance')
    plt.legend([str(i + 1) for i in range(n_em)])
    plt.title('SPICE Endmembers')

    # unmix the data using the non-downsampled array and the endmembers that SPICE discovered
    P = unmix2(input_data, endmembers)

    # re-reval abundance maps
    P_imgs = []
    for i in range(n_em):
        map_lin = np.zeros((n_r * n_c,))
        map_lin[valid_array] = P[:, i]
        P_imgs.append(np.reshape(map_lin, (n_r, n_c)))

    # display abundance maps in the form of a subplot
    fig, axes = plt.subplots(2, int(n_em/2) + 1, squeeze=True)
    for i in range(n_em):
        im = axes.flat[i].imshow(P_imgs[i], vmin=0, vmax=1)
        axes.flat[i].set_title('SPICE Abundance Map %d' % (i + 1))

    # add the original RGB image to the subplot
    im = axes.flat[n_em].imshow(hsi['RGB'])
    axes.flat[n_em].set_title('RGB Image')
    fig.colorbar(im, ax=axes.ravel().tolist())

    # delete any empty subplots
    if (n_em % 2 == 0):
        fig.delaxes(axes.flatten()[(2*(int(n_em/2)+1)) -1])
    plt.show()
    return

# run the main method
main()