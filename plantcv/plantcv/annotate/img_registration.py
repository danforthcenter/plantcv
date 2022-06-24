# Image Registration Based On User Selected Landmark Points

import cv2
from plantcv import plantcv as pcv
from plantcv.plantcv.annotate.points import _find_closest_pt
import matplotlib.pyplot as plt
import pickle as pkl


class ImageRegistrator:
    """
    An interactive tool that takes user selected landmark points to register two images
    """
    def __init__(self, ref_img, target_img, figsize=(12, 6), cmap='jet'):
        self.img_ref = ref_img
        self.img_tar = target_img

        self.fig, self.axes = plt.subplots(1, 2, figsize=figsize)
        self.axes[0].text(0, -100,
                          'Collect points matching features between images. '
                          'Select location on reference image then target image. '
                          '\nPlease first click on the reference image, then on the same point on the target image.'
                          '\nPlease select at least 4 pairs of points.')

        # assumption: any 3-d images whose 3rd dimension is 3 are rgb images
        # This check to be replaced when image class implemented
        dim_ref, dim_tar = ref_img.shape, target_img.shape
        if len(dim_ref) == 3 and dim_ref[-1] == 3:
            self.axes[0].imshow(cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB))
        else:
            self.axes[0].imshow(ref_img, cmap=cmap)
        self.axes[0].set_title('Reference Image')

        if len(dim_tar) == 3 and dim_tar[-1] == 3:
            self.axes[1].imshow(cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB))
        else:
            self.axes[1].imshow(target_img, cmap=cmap)
        self.axes[1].set_title('Target Image')

        # Set useblit=True on most backends for enhanced performance.
        # cursor = Cursor(axes[0], horizOn=True, vertOn=True, useblit=True, color='red', linewidth=2)

        self.points = [[], []]
        self.events = []

        # onclick = functools.partial(_onclick_, fig, axes, array_data, wvs)

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.model = None
        self.img_registered = None

    def left_click(self, idx_ax, x, y):
        self.axes[idx_ax].plot(x, y, 'x', c='red')
        self.points[idx_ax].append((x, y))

    def right_click(self, idx_ax, x, y):
        idx_remove, _ = _find_closest_pt((x, y), self.points[idx_ax])
        self.points[idx_ax].pop(idx_remove)
        axplots = self.axes[idx_ax].lines
        self.axes[idx_ax].lines.remove(axplots[idx_remove])

    def onclick(self, event):
        self.events.append(event)

        # collect points on reference image
        if str(event.inaxes._subplotspec) == 'GridSpec(1, 2)[0:1, 0:1]':
            # left click
            if event.button == 1:
                self.left_click(0, event.xdata, event.ydata)
            # right click
            else:
                self.right_click(0, event.xdata, event.ydata)

        # collect points on target image
        elif str(event.inaxes._subplotspec) == 'GridSpec(1, 2)[0:1, 1:2]':
            if event.button == 1:
                self.left_click(1, event.xdata, event.ydata)
            else:
                self.right_click(1, event.xdata, event.ydata)
        self.fig.canvas.draw()

    def save_model(self, model_file="model"):
        pkl.dump(self.model, open("{}.pkl".format(model_file), "wb"))

    def display_coords(self):
        print("\nCoordinates for selected reference points: ")
        for point_ref in self.points[0]:
            print("\n{}".format(point_ref))
        print("\nCoordinates for selected target points: ")
        for point_tar in self.points[1]:
            print("\n{}".format(point_tar))

    def regist(self):
        # use warp function in plantcv
        self.model, self.img_registered = pcv.transform.warp(self.img_tar,
                                                                   self.img_ref,
                                                                   self.points[1],
                                                                   self.points[0],
                                                                   method='ransac')
