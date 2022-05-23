# Identify landmark positions within a contour for morphometric analysis

import numpy as np
import math
import cv2
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def acute(img, obj, mask, win, threshold):
    """
    Identify landmark positions within a contour for morphometric analysis

    Inputs:
    img         = Original image used for plotting purposes
    obj         = An opencv contour array of interest to be scanned for landmarks
    mask        = binary mask used to generate contour array (necessary for ptvals)
    win         = maximum cumulative pixel distance window for calculating angle
                  score; 1 cm in pixels often works well
    threshold   = angle score threshold to be applied for mapping out landmark
                  coordinate clusters within each contour

    Outputs:
    homolog_pts = pseudo-landmarks selected from each landmark cluster
    start_pts   = pseudo-landmark island starting position; useful in parsing homolog_pts in downstream analyses
    stop_pts    = pseudo-landmark island end position ; useful in parsing homolog_pts in downstream analyses
    ptvals      = average values of pixel intensity from the mask used to generate cont;
                  useful in parsing homolog_pts in downstream analyses
    chain       = raw angle scores for entire contour, used to visualize landmark
                  clusters
    verbose_out = supplemental file which stores coordinates, distance from
                  landmark cluster edges, and angle score for entire contour.  Used
                  in troubleshooting.

    :param img: numpy.ndarray
    :param obj: numpy.ndarray
    :param mask: numpy.ndarray
    :param win: int
    :param threshold: int
    :return homolog_pts:
    """

    chain = []                                         # Create empty chain to store angle scores
    for k in list(range(len(obj))):                    # Coordinate-by-coordinate 3-point assignments
        vert = obj[k]
        dist_1 = 0
        for r in range(len(obj)):                      # Reverse can to obtain point A
            rev = k - r
            pos = obj[rev]
            dist_2 = np.sqrt(np.square(pos[0][0]-vert[0][0])+np.square(pos[0][1]-vert[0][1]))
            if r >= 2:
                if (dist_2 > dist_1) & (dist_2 <= win):  # Further from vertex than current pt A while within window?
                    dist_1 = dist_2
                    pt_a = pos                              # Load best fit within window as point A
                elif dist_2 > win:
                    break
            else:
                pt_a = pos
        dist_1 = 0
        for f in range(len(obj)):                      # Forward scan to obtain point B
            fwd = k + f
            if fwd >= len(obj):
                fwd -= len(obj)
            pos = obj[fwd]
            dist_2 = np.sqrt(np.square(pos[0][0]-vert[0][0])+np.square(pos[0][1]-vert[0][1]))
            if f >= 2:
                if (dist_2 > dist_1) & (dist_2 <= win):  # Further from vertex than current pt B while within window?
                    dist_1 = dist_2
                    pt_b = pos                              # Load best fit within window as point B
                elif dist_2 > win:
                    break
            else:
                pt_b = pos

        # Angle in radians derived from Law of Cosines, converted to degrees
        p12 = np.sqrt((vert[0][0]-pt_a[0][0])*(vert[0][0]-pt_a[0][0])+(vert[0][1]-pt_a[0][1])*(vert[0][1]-pt_a[0][1]))
        p13 = np.sqrt((vert[0][0]-pt_b[0][0])*(vert[0][0]-pt_b[0][0])+(vert[0][1]-pt_b[0][1])*(vert[0][1]-pt_b[0][1]))
        p23 = np.sqrt((pt_a[0][0]-pt_b[0][0])*(pt_a[0][0]-pt_b[0][0])+(pt_a[0][1]-pt_b[0][1])*(pt_a[0][1]-pt_b[0][1]))
        dot = (p12*p12 + p13*p13 - p23*p23)/(2*p12*p13)

        # Used a random number generator to test if either of these cases were possible but neither is possible
        # if dot > 1:              # If float exceeds 1 prevent arcos error and force to equal 1
        #     dot = 1
        # elif dot < -1:           # If float exceeds -1 prevent arcos error and force to equal -1
        #     dot = -1

        ang = math.degrees(math.acos(dot))
        # print(str(k)+'  '+str(dot)+'  '+str(ang))
        chain.append(ang)

    index = []                      # Index chain to find clusters below angle threshold

    for c, link in enumerate(chain):     # Identify links in chain with acute angles
        if float(link) <= threshold:
            index.append(c)         # Append positions of acute links to index

    # acute_pos = obj[index]            # Extract all island points blindly
    #
    # float(len(acute_pos)) / float(len(obj))  # Proportion of informative positions

    if len(index) != 0:

        isle = []
        island = []

        for ind in index:           # Scan for iterative links within index
            if not island:
                island.append(ind)       # Initiate new link island
            elif island[-1]+1 == ind:
                island.append(ind)       # Append successful iteration to island
            elif island[-1]+1 != ind:
                pt_a = obj[ind]
                pt_b = obj[island[-1]+1]
                dist = np.sqrt(np.square(pt_a[0][0]-pt_b[0][0])+np.square(pt_a[0][1]-pt_b[0][1]))
                if win/2 > dist:
                    island.append(ind)
                else:
                    isle.append(island)
                    island = [ind]

        isle.append(island)

        if len(isle) > 1:
            if (isle[0][0] == 0) & (isle[-1][-1] == (len(chain)-1)):
                if params.debug is not None:
                    print('Fusing contour edges')
                island = isle[-1]+isle[0]  # Fuse overlapping ends of contour
                # Delete islands to be spliced if start-end fusion required
                del isle[0]
                del isle[-1]
                isle.insert(0, island)      # Prepend island to isle
        else:
            if params.debug is not None:
                print('Microcontour...')

        # Homologous point maximum distance method
        pt = []
        vals = []
        maxpts = []
        ss_pts = []
        ts_pts = []
        ptvals = []
        max_dist = [['cont_pos', 'max_dist', 'angle']]
        for island in isle:

            # Identify if contour is concavity/convexity using image mask
            pix_x, pix_y, w, h = cv2.boundingRect(obj[island])  # Obtain local window around island

            for c in range(w):
                for r in range(h):
                    # Identify pixels in local window internal to the island hull
                    pos = cv2.pointPolygonTest(obj[island], (pix_x+c, pix_y+r), 0)
                    if 0 < pos:
                        vals.append(mask[pix_y+r][pix_x+c])  # Store pixel value if internal
            if len(vals) > 0:
                ptvals.append(sum(vals)/len(vals))
                vals = []
            else:
                ptvals.append('NaN')        # If no values can be retrieved (small/collapsed contours)
                vals = []

            # Identify pixel coordinate to use as pseudolandmark for island
            # if len(isle[x]) == 1:           # If landmark is a single point (store position)
            #    if debug == True:
            #        print('route A')
            #    pt = isle[x][0]
            #    max_dist.append([isle[x][0], '-', chain[isle[x][0]]])
            #    # print pt
            # elif len(isle[x]) == 2:         # If landmark is a pair of points (store more acute position)
            #    if debug == True:
            #        print('route B')
            #    pt_a = chain[isle[x][0]]
            #    pt_b = chain[isle[x][1]]
            #    print(pt_a, pt_b)
            #    if pt_a == pt_b:
            #        pt = isle[x][0]             # Store point A if both are equally acute
            #        max_dist.append([isle[x][0], '-', chain[isle[x][0]]])
            #    elif pt_a < pt_b:
            #        pt = isle[x][0]             # Store point A if more acute
            #        max_dist.append([isle[x][0], '-', chain[isle[x][0]]])
            #    elif pt_a > pt_b:
            #        pt = isle[x][1]             # Store point B if more acute
            #        max_dist.append([isle[x][1], '-', chain[isle[x][1]]])
            #     print pt

            if len(island) >= 3:               # If landmark is multiple points (distance scan for position)
                if params.debug is not None:
                    print('route C')
                ss = obj[island[0]]            # Store isle "x" start site
                ts = obj[island[-1]]           # Store isle "x" termination site
                dist_1 = 0
                for d in island:   # Scan from ss to ts within isle "x"
                    site = obj[[d]]
                    ss_d = np.sqrt(np.square(ss[0][0] - site[0][0][0]) + np.square(ss[0][1] - site[0][0][1]))
                    ts_d = np.sqrt(np.square(ts[0][0] - site[0][0][0]) + np.square(ts[0][1] - site[0][0][1]))
                    # Current mean distance of 'd' to 'ss' & 'ts'
                    dist_2 = np.mean([np.abs(ss_d), np.abs(ts_d)])
                    max_dist.append([d, dist_2, chain[d]])
                    if dist_2 > dist_1:                          # Current mean distance better fit that previous best?
                        pt = d
                        dist_1 = dist_2                          # Current mean becomes new best mean
                # print pt
                if params.debug is not None:
                    print(f"Landmark site: {pt}, Start site: {island[0]}, Term. site: {island[-1]}")

                maxpts.append(pt)           # Empty 'pts' prior to next mean distance scan
                ss_pts.append(island[0])
                ts_pts.append(island[-1])

            if params.debug is not None:
                print(f'Landmark point indices: {maxpts}')
                print(f'Starting site indices: {ss_pts}')
                print(f'Termination site indices: {ts_pts}')

        homolog_pts = obj[maxpts]
        start_pts = obj[ss_pts]
        stop_pts = obj[ts_pts]

        ori_img = np.copy(img)
        # Convert grayscale images to color
        if len(np.shape(ori_img)) == 2:
            ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)
        # Draw acute points on the original image
        cv2.drawContours(ori_img, homolog_pts, -1, (255, 255, 255), params.line_thickness)
        # print/plot debug image
        _debug(visual=ori_img, filename=f"{params.device}_acute_plms.png")

        return homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist
    else:
        return [], [], [], [], [], []
