"""Class to hold morphology objects"""
import os
import cv2
import numpy as np
from skimage import morphology as skmorph
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.color_palette import color_palette
from plantcv.plantcv.morphology.segment_sort import _segment_sort
from plantcv.plantcv.morphology.find_branch_pts import _find_branch_pts
from plantcv.plantcv.morphology.segment_skeleton import _segment_skeleton
from plantcv.plantcv._helpers import (_cv2_findcontours, _iterative_prune, _image_subtract,
                                      _dilate, _erode, _find_tips)


class morph:
    def __init__(self, mask, first_stem=True):
        """Initialize morph class

        Parameters
        ----------
        mask     = numpy.ndarray,
            binary or labeled mask
        image    = numpy.ndarray,
            optional image corresponding to the mask. Used in analyze module.
        """
        self.mask = mask
        skeleton = self._skeletonize()
        self.skeleton = skeleton

        skel_objects = _segment_skeleton(skeleton)
        skel_leaves, skel_stems, _ = _segment_sort(skeleton, skel_objects, first_stem=first_stem)

        self.pruned_skeleton = None
        self.stem = skel_stems
        self.leaves = skel_leaves
        self._cycles = 0
        self._leaf_tips = []
        self._branch_points = []

    # `mask`
    @property
    def mask(self):
        """public mask"""
        return self._mask

    @mask.setter
    def mask(self, new_mask):
        """update the public mask"""
        self._mask = new_mask

    # `skeleton`
    @property
    def skeleton(self):
        """public skeleton"""
        # we return the pruned skeleton for ease of use
        return self.pruned_skeleton

    @skeleton.setter
    def skeleton(self, new_skeleton):
        """update the skeleton"""
        self._skeleton = new_skeleton

    # `pruned skeleton`
    @property
    def pruned_skeleton(self):
        """Store the pruned skeleton"""
        if self._pruned_skeleton is None:
            self._pruned_skeleton = self._skeleton
        return self._pruned_skeleton

    @pruned_skeleton.setter
    def pruned_skeleton(self, new_pruned_skeleton):
        """update the pruned skeleton"""
        self._pruned_skeleton = new_pruned_skeleton

    # `Stem Objects`
    @property
    def stem(self):
        """Store a list of stem segments"""
        return self._stem

    @stem.setter
    def stem(self, new_stem):
        """Set stem segments"""
        self._stem = new_stem

    # `Leaf objects`
    @property
    def leaves(self):
        """Store a list of leaf segments"""
        return self._leaves

    @leaves.setter
    def leaves(self, new_leaves):
        """Set leaf segments"""
        self._leaves = new_leaves

    # `Cycles in skeleton`
    @property
    def cycles(self):
        """Store the number of cycles in the skeleton"""
        self._check_cycles()
        return self._cycles

    @cycles.setter
    def cycles(self, new_cycle):
        """Update number of cycles"""
        self._cycles = new_cycle

    # `leaf_tips`
    @property
    def leaf_tips(self):
        """Leaf tips of skeleton"""
        _, tip_list, _ = _find_tips(self.skeleton)
        # switch to X, Y
        self.leaf_tips = [(t[1], t[0]) for t in tip_list]
        return self._leaf_tips

    @leaf_tips.setter
    def leaf_tips(self, new_tips):
        """Update leaf tips"""
        self._leaf_tips = new_tips

    # `branch_points`
    @property
    def branch_points(self):
        """branch points of skeleton"""
        branch_list, _, _ = _find_branch_pts(self.skeleton)
        # switch to X, Y
        self.branch_points = [(t[1], t[0]) for t in branch_list]
        return self._branch_points

    @branch_points.setter
    def branch_points(self, new_points):
        """Update leaf tips"""
        self._branch_points = new_points

    # `Making and segmenting a skeleton`
    def _skeletonize(self):
        """Make a skeleton from a mask"""
        # make a skeleton
        skeleton = skmorph.skeletonize(self.mask.astype(bool))
        skeleton = skeleton.astype(np.uint8) * 255
        return skeleton

    # `Pruning a Skeleton`
    def prune(self, size=0, first_stem=True, reprune=False):
        """Prune the ends of skeletonized segments.
        The pruning algorithm proposed by https://github.com/karnoldbio
        Segments a skeleton into discrete pieces, prunes off all segments less than or
        equal to user specified size. Sets `pruned_skeleton` (retrieved by skeleton),
        `leaves`, and `stem` attributes.

        Parameters
        ----------
        size       = int,
            Size to get pruned off each branch
        first_stem = boolean,
            (Optional) if True, then the first (bottom) segment always gets classified as stem
        reprune    = boolean,
            Prune the already pruned skeleton. Defaults to False, which effectively is a new prune each time.

        Returns
        -------
        pruned_img      = numpy.ndarray,
            Pruned image
        segmented_img   = numpy.ndarray,
            Segmented debugging image
        segment_objects = list,
            List of contours
        """
        # always pull from the hidden _skeleton attribute
        # public skeleton attribute pulls from pruned_skeleton.
        skel_img = self._skeleton
        if reprune:
            skel_img = self.skeleton
        kept_segments = []
        removed_segments = []
        # Initialize pruned_skel array
        pruned_skel = skel_img.copy()
        if size > 0:
            objects = _segment_skeleton(skel_img)
            # Sort through segments since we don't want to remove primary segments
            secondary_objects, _, _ = _segment_sort(skel_img, objects, first_stem=first_stem)

            # Keep segments longer than specified size
            for i in range(0, len(secondary_objects)):
                if len(secondary_objects[i]) > size:
                    kept_segments.append(secondary_objects[i])
                else:
                    removed_segments.append(secondary_objects[i])
            # Draw the contours that got removed
            removed_barbs = np.zeros(skel_img.shape[:2], np.uint8)
            cv2.drawContours(removed_barbs, removed_segments, -1, 255, 1,
                             lineType=8)
            # Subtract all short segments from the skeleton image
            pruned_skel = _image_subtract(pruned_skel, removed_barbs)
            pruned_skel = _iterative_prune(pruned_skel, 1)

        # Store pruned skeleton and sorted segments of it in class
        pruned_objects = _segment_skeleton(pruned_skel)
        pruned_leaves, pruned_stems, _ = _segment_sort(pruned_skel, pruned_objects, first_stem=first_stem)
        self._pruned_skeleton = pruned_skel
        self._leaves = pruned_leaves
        self._stem = pruned_stems

        # Make debugging image
        if params.debug:
            pruned_plot = self.mask.copy()
            pruned_plot = cv2.cvtColor(pruned_plot, cv2.COLOR_GRAY2RGB)
            pruned_obj, _ = _cv2_findcontours(bin_img=pruned_skel)
            cv2.drawContours(pruned_plot, removed_segments,
                             -1, (0, 0, 255), params.line_thickness, lineType=8)
            cv2.drawContours(pruned_plot, pruned_obj,
                             -1, (150, 150, 150), params.line_thickness, lineType=8)
            _debug(visual=pruned_plot, filename=os.path.join(params.debug_outdir,
                                                             f"{params.device}_pruned_debug.png"))

    def _check_cycles(self):
        """Check for cycles, returning number of cycles"""
        skel_img = self.skeleton

        h, w = skel_img.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        # Copy the skeleton since cv2.floodFill will draw on it
        skel_copy = skel_img.copy()
        cv2.floodFill(skel_copy, mask=mask, seedPoint=(0, 0), newVal=255)

        # Invert so the holes are white and background black
        just_cycles = cv2.bitwise_not(skel_copy)

        # Erode slightly so that cv2.findContours doesn't think diagonal pixels are contours
        just_cycles = _erode(just_cycles, 2, 1)

        # Use pcv.find_objects to turn plots of holes into countable contours
        cycle_objects, cycle_hierarchies = _cv2_findcontours(bin_img=just_cycles)

        # Count the number of holes
        num_cycles = len(cycle_objects)

        if num_cycles and params.debug:
            cycle_img = skel_img.copy()
            cycle_img = _dilate(cycle_img, params.line_thickness, 1)
            cycle_img = cv2.cvtColor(cycle_img, cv2.COLOR_GRAY2RGB)
            rand_color = color_palette(num=num_cycles, saved=False)
            for i in range(0, len(cycle_objects)):
                cv2.drawContours(cycle_img, cycle_objects, i,
                                 rand_color[i], params.line_thickness,
                                 lineType=8, hierarchy=cycle_hierarchies)
            _debug(visual=cycle_img, filename=os.path.join(params.debug_outdir,
                                                           f"{params.device}_cycles.png"))
        self.cycles = num_cycles

    def combine_segments(self, leaves=None, stems=None, combined_type=None):
        """Combine selected leaf and/or stem segments into a single segment.

        Parameters
        ----------
        leaves        = list,
            Indices (into `leaves`) of leaf segments to combine
        stems         = list,
            Indices (into `stem`) of stem segments to combine
        combined_type = str or None,
            "leaf" or "stem", which list the combined segment is added to.
            Defaults to the type of the input segments; required when mixing
            leaves and stems.

        Returns
        -------
        None. Updates the `leaves` and `stem` attributes. The combined segment is
        appended to the end of its list.
        """
        leaves = [] if leaves is None else list(leaves)
        stems = [] if stems is None else list(stems)

        # Validate IDs before changing anything
        for name, ids, segs in (("leaves", leaves, self.leaves), ("stems", stems, self.stem)):
            if not all(isinstance(i, (int, np.integer)) and not isinstance(i, bool) for i in ids):
                fatal_error(f"{name} must be a list of integer segment IDs")
            if any(i < 0 or i >= len(segs) for i in ids):
                fatal_error(f"{name} IDs must be between 0 and {len(segs) - 1}")
            if len(set(ids)) != len(ids):
                fatal_error(f"{name} contains duplicate IDs")
        if len(leaves) + len(stems) < 2:
            fatal_error("At least two segments are needed to combine")

        # Pick which list gets the combined segment
        if combined_type is None:
            if leaves and stems:
                fatal_error("combined_type ('leaf' or 'stem') is required when combining leaves and stems")
            combined_type = "leaf" if leaves else "stem"
        if combined_type not in ("leaf", "stem"):
            fatal_error(f"combined_type must be 'leaf' or 'stem', not '{combined_type}'")

        # Concatenate contour points, highest index first to match legacy segment_combine
        to_combine = [self.leaves[i] for i in sorted(leaves, reverse=True)] + \
                     [self.stem[i] for i in sorted(stems, reverse=True)]
        combined_object = np.concatenate(to_combine, axis=0)

        # Build new lists instead of popping so the attributes are replaced, not mutated
        new_leaves = [seg for i, seg in enumerate(self.leaves) if i not in leaves]
        new_stem = [seg for i, seg in enumerate(self.stem) if i not in stems]
        if combined_type == "leaf":
            new_leaves.append(combined_object)
        else:
            new_stem.append(combined_object)
        self.leaves = new_leaves
        self.stem = new_stem

        # Debug image: leaves labeled with their (new) IDs, stems in green
        if params.debug:
            labeled_img = cv2.cvtColor(self.mask.copy(), cv2.COLOR_GRAY2RGB)
            rand_color = color_palette(num=len(self.leaves), saved=True)
            for i, seg in enumerate(self.leaves):
                cv2.drawContours(labeled_img, [seg], -1, rand_color[i], params.line_thickness, lineType=8)
                x, y = seg[0][0]
                cv2.putText(img=labeled_img, text=f"ID:{i}", org=(int(x), int(y)),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=params.text_size,
                            color=rand_color[i], thickness=2)
            cv2.drawContours(labeled_img, self.stem, -1, (0, 255, 0), params.line_thickness, lineType=8)
            _debug(visual=labeled_img,
                   filename=os.path.join(params.debug_outdir, f"{params.device}_combined_segment_ids.png"))
