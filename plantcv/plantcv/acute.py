# Identify landmark positions within a contour for morphometric analysis

import numpy as np
import math
import cv2


def acute(obj, mask, win, thresh):
    """acute: identify landmark positions within a contour for morphometric analysis

    Inputs:
    obj         = An opencv contour array of interest to be scanned for landmarks
    mask        = binary mask used to generate contour array (necessary for ptvals)
    win         = maximum cumulative pixel distance window for calculating angle
                  score; 1 cm in pixels often works well
    thresh      = angle score threshold to be applied for mapping out landmark
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

    :param obj: ndarray
    :param mask: ndarray
    :param win: int
    :param thresh: int
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
                    ptA = pos                              # Load best fit within window as point A
                elif dist_2 > win:
                    break
            else:
                ptA = pos
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
                    ptB = pos                              # Load best fit within window as point B
                elif dist_2 > win:
                    break
            else:
                ptB = pos

        # Angle in radians derived from Law of Cosines, converted to degrees
        P12 = np.sqrt((vert[0][0]-ptA[0][0])*(vert[0][0]-ptA[0][0])+(vert[0][1]-ptA[0][1])*(vert[0][1]-ptA[0][1]))
        P13 = np.sqrt((vert[0][0]-ptB[0][0])*(vert[0][0]-ptB[0][0])+(vert[0][1]-ptB[0][1])*(vert[0][1]-ptB[0][1]))
        P23 = np.sqrt((ptA[0][0]-ptB[0][0])*(ptA[0][0]-ptB[0][0])+(ptA[0][1]-ptB[0][1])*(ptA[0][1]-ptB[0][1]))
        dot = (P12*P12 + P13*P13 - P23*P23)/(2*P12*P13)

        # Used a random number generator to test if either of these cases were possible but neither is possible
        # if dot > 1:              # If float exceeds 1 prevent arcos error and force to equal 1
        #     dot = 1
        # elif dot < -1:           # If float exceeds -1 prevent arcos error and force to equal -1
        #     dot = -1
        ang = math.degrees(math.acos(dot))
        chain.append(ang)

    index = []                      # Index chain to find clusters below angle threshold

    for c in range(len(chain)):     # Identify links in chain with acute angles
        if float(chain[c]) <= thresh:
            index.append(c)         # Append positions of acute links to index

    acute_pos = obj[index]            # Extract all island points blindly

    float(len(acute_pos)) / float(len(obj))  # Proportion of informative positions

    if len(index) != 0:

        isle = []
        island = []

        for c in range(len(index)):           # Scan for iterative links within index
            if not island:
                island.append(index[c])       # Initiate new link island
            elif island[-1]+1 == index[c]:
                island.append(index[c])       # Append successful iteration to island
            elif island[-1]+1 != index[c]:
                ptA = obj[index[c]]
                ptB = obj[island[-1]+1]
                dist = np.sqrt(np.square(ptA[0][0]-ptB[0][0])+np.square(ptA[0][1]-ptB[0][1]))
                if win/2 > dist:
                    island.append(index[c])
                else:
                    isle.append(island)
                    island = [index[c]]

        isle.append(island)

        if len(isle) > 1:
            if (isle[0][0] == 0) & (isle[-1][-1] == (len(chain)-1)):
                print('Fusing contour edges')

                # Cannot add a range and a list (or int)
                # island = range(-(len(chain)-isle[-1][0]), 0)+isle[0]  # Fuse overlapping ends of contour
                # Delete islands to be spliced if start-end fusion required
                del isle[0]
                del isle[-1]
                # isle.insert(0, island)      # Prepend island to isle
        else:
            print('Microcontour...')

        # Homologous point maximum distance method
        pt = []
        vals = []
        maxpts = []
        SSpts = []
        TSpts = []
        ptvals = []
        max_dist = [['cont_pos', 'max_dist', 'angle']]
        for x in range(len(isle)):

            # Identify if contour is concavity/convexity using image mask
            pix_x, pix_y, w, h = cv2.boundingRect(obj[isle[x]])  # Obtain local window around island

            for c in range(w):
                for r in range(h):
                    # Identify pixels in local window internal to the island hull
                    pos = cv2.pointPolygonTest(obj[isle[x]], (pix_x+c, pix_y+r), 0)
                    if 0 < pos:
                        vals.append(mask[pix_y+r][pix_x+c])  # Store pixel value if internal
            if len(vals) > 0:
                ptvals.append(sum(vals)/len(vals))
                vals = []
            else:
                ptvals.append('NaN')        # If no values can be retrieved (small/collapsed contours)
                vals = []

            # Identify pixel coordinate to use as pseudolandmark for island
            if len(isle[x]) == 1:           # If landmark is a single point (store position)
                # print 'route A'
                pt = isle[x][0]
                max_dist.append([isle[x][0], '-', chain[isle[x][0]]])
                # print pt
            elif len(isle[x]) == 2:         # If landmark is a pair of points (store more acute position)
                # print 'route B'
                ptA = chain[isle[x][0]]
                ptB = chain[isle[x][1]]
                if ptA < ptB:
                    pt = isle[x][0]             # Store point A if more acute
                    max_dist.append([isle[x][0], '-', chain[isle[x][0]]])
                elif ptA > ptB:
                    pt = isle[x][1]             # Store point B if more acute
                    max_dist.append([isle[x][1], '-', chain[isle[x][1]]])
                # print pt
            else:                           # If landmark is multiple points (distance scan for position)
                # print 'route C'
                SS = obj[[isle[x]]][0]          # Store isle "x" start site
                TS = obj[[isle[x]]][-1]         # Store isle "x" termination site
                dist_1 = 0
                for d in range(len(isle[x])):   # Scan from SS to TS within isle "x"
                    site = obj[[isle[x][d]]]
                    SSd = np.sqrt(np.square(SS[0][0]-site[0][0][0])+np.square(SS[0][1]-site[0][0][1]))
                    TSd = np.sqrt(np.square(TS[0][0]-site[0][0][0])+np.square(TS[0][1]-site[0][0][1]))
                    # Current mean distance of 'd' to 'SS' & 'TS'
                    dist_2 = np.mean([np.abs(SSd), np.abs(TSd)])
                    max_dist.append([isle[x][d], dist_2, chain[isle[x][d]]])
                    if dist_2 > dist_1:                           # Current mean distance better fit that previous best?
                        pt = isle[x][d]
                        dist_1 = dist_2                           # Current mean becomes new best mean
                # print pt
            maxpts.append(pt)           # Empty 'pts' prior to next mean distance scan
            SSpts.append(isle[x][0])
            TSpts.append(isle[x][-1])

        homolog_pts = obj[maxpts]
        start_pts = obj[SSpts]
        stop_pts = obj[TSpts]

        return homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist
    else:
        return [], [], [], [], [], []
