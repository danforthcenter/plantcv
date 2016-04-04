import numpy as np
import math


### Identify landmark positions within a contour for morphometric analysis
def acute(cont, win, thresh, debug=False):
    #Inputs:
    #cont        = opencv contour array of interest to be scanned for landmarks
    #win         = maximum cumulative pixel distance window for calculating angle 
    #              score; 1 cm in pixels often works well
    #thresh      = angle score threshold to be applied for mapping out landmark 
    #              coordinate clusters within each contour
    #Outputs:
    #homolog_pts = homologous points selected from each landmark cluster
    #chain       = raw angle scores for entire contour, used to visualize landmark
    #              clusters 
    #verbose_out = supplemental file which stores coordinates, distance from
    #              landmark cluster edges, and angle score for entire contour.  Used
    #              in troubleshooting.

    #*#*#*#*#*# Warning: Here be Trigonometry... #*#*#*#*#*#

    vert = obj[0]                                      #Initialize first vertex for chain scan
    chain = []                                         #Create empty chain to store angle scores
    for k in list(range(len(obj))):                    #Coordinate-by-coordinate 3-point assignments
        former = vert
        vert = obj[k]
        dist_1 = 0; dist_2 = 0; pos = [];
        for r in range(len(obj)):                      #Reverse can to obtain point A
            rev = k - r
            pos = obj[rev]
            dist_2 = np.sqrt(np.square(pos[0][0]-vert[0][0])+np.square(pos[0][1]-vert[0][1]))   
            if ((dist_2 > dist_1) & (dist_2 <= win)):  #Further from vertex than current point A while within window?
                dist_1 = dist_2
                ptA = pos                              #Load best fit within window as point A
            elif (dist_2 > win):
                break          
        #print(ptA, dist_1)                     #Unnecessary 
        dist_1 = 0; dist_2 = 0; pos = [];
        for f in range(len(obj)):                      #Forward scan to obtain point B
            fwd = k + f
            if fwd >= len(obj):
                fwd = fwd - len(obj)
            pos = obj[fwd]
            dist_2 = np.sqrt(np.square(pos[0][0]-vert[0][0])+np.square(pos[0][1]-vert[0][1]))   
            if ((dist_2 > dist_1) & (dist_2 <= win)):  #Further from vertex than current point B while within window?
                dist_1 = dist_2
                ptB = pos                              #Load best fit within window as point B
            elif (dist_2 > win):
                break
        #print(ptB, dist_1)                     #Unnecessary 

        #Angle in radians derived from Law of Cosines, converted to degrees
        P12 = np.sqrt((vert[0][0]-ptA[0][0])*(vert[0][0]-ptA[0][0])+(vert[0][1]-ptA[0][1])*(vert[0][1]-ptA[0][1]))
        P13 = np.sqrt((vert[0][0]-ptB[0][0])*(vert[0][0]-ptB[0][0])+(vert[0][1]-ptB[0][1])*(vert[0][1]-ptB[0][1]))
        P23 = np.sqrt((ptA[0][0]-ptB[0][0])*(ptA[0][0]-ptB[0][0])+(ptA[0][1]-ptB[0][1])*(ptA[0][1]-ptB[0][1]))
        dot = (P12*P12 + P13*P13 - P23*P23)/(2*P12*P13)
        if dot > 1:              #If float excedes 1 prevent arcos error and force to equal 1
            dot = 1
        elif dot < -1:           #If float excedes -1 prevent arcos error and force to equal -1
            dot = -1      
        ang = math.degrees(math.acos(dot))
        chain.append(ang)
        
    #*#*#*#*#*#

    index = []                      #Index chain to find clusters below angle threshold

    for c in range(len(chain)):     #Identify links in chain with acute angles
        if float(chain[c]) <= thresh:
            index.append(c)         #Append positions of acute links to index 

    acute = obj[[index]]            #Extract all island points blindly

    float(len(acute)) / float(len(obj))  #Proportion of informative positions

    isle = []                       #Create empty isle to store islands
    island = []                     #Create empty island to store chain clusters

    for c in range(len(index)):     #Scan for iterative links within index
        if not island:
            island.append(index[c]) #Initiate new link island
        elif (island[-1]+1 != index[c]) & (len(island) > 10): 
            isle.append(island)     #If iteration ends and island is large append to isle
            island = []             #Empty island
        else:
            island.append(index[c]) #Append successful iteration to island

    isle.append(island)             #Append final island to isle
    island =  []                    #Empty island

    if (isle[0][0] == 0) & (isle[-1][-1] == (len(chain)-1)):
        island = range(-(len(chain)-isle[-1][0]), 0)+isle[0] #Fuse overlapping ends of contour
        del isle[0]; del isle[-1];  #Delete islands to be spliced if start-end fusion required
        isle.insert(0, island)      #Prepend island to isle
        island = []                 #Empty island

    #Homologous point maximum distance method
    pt = ''
    maxpts = [];
    max_dist = [['cont_pos', 'max_dist', 'angle']]
    for x in range(len(isle)):
        if pt:
    #Slope within island    
            maxpts.append(pt)          #Empty 'pts' prior to next mean distance scan
        SS = obj[[isle[x]]][0]         #Store isle "x" start site
        TS = obj[[isle[x]]][-1]        #Store isle "x" termination site
        dist_1 = 0
        for d in range(len(isle[x])):  #Scan from SS to TS within isle "x"
            site = obj[[isle[x][d]]]
            SSd = np.sqrt(np.square(SS[0][0]-site[0][0][0])+np.square(SS[0][1]-site[0][0][1]))
            TSd = np.sqrt(np.square(TS[0][0]-site[0][0][0])+np.square(TS[0][1]-site[0][0][1]))
            dist_2 = np.mean([np.abs(SSd),np.abs(TSd)])               #Cureent mean distance of 'd' to 'SS' & 'TS'
            max_dist.append([isle[x][d], dist_2, chain[isle[x][d]]])
            if dist_2 > dist_1:                                       #Current mean distance better fit that previous best?
                pt = isle[x][d]
                dist_1 = dist_2                                       #Current mean becomes new best mean
                site = ''; SSd = ''; TSd = ''; dist_2 = '';

    maxpts.append(pt)                  #Empty final 'pts'
    homolog_pts = obj[[maxpts]]        #Extract coordinates of interest as image landmarks

    if debug: 
        print '[landmarks, contour scores, verbose output]'
        return [homolog_pts, chain, max_dist]
    else:
        print '[landmarks]'
        return [homolog_pts]
