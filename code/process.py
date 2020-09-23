import numpy as np
import siamxt
import option

def AP(im, thresholds=option.thresholds, connexity=1):
    S = len(thresholds)
    n_features = 2*S+1

    # Element structurant
    Se = np.ones((3, 3), dtype=bool)
    if connexity == 1:
        Se[0, 0] = False
        Se[2, 0] = False
        Se[0, 2] = False
        Se[2, 2] = False
    
    # Construction du tableau résultat
    h, w = im.shape
    ap = np.zeros((h, w, n_features))

    # Max value of image for negative
    maxi = im.max()
    neg = maxi - im
    
    # Min-tree (max-tree with negative image)
    min_tree = siamxt.MaxTreeAlpha(neg, Se)
    # Max-tree
    max_tree = siamxt.MaxTreeAlpha(im, Se)

    # Closings (Thickening Profile)
    for i in range(S):
        n = S - i - 1
        clone = min_tree.clone()
        clone.areaOpen(thresholds[n])
        ap[:, :, i] = maxi - clone.getImage()
        
    # Original
    ap[:, :, S] = im
        
    # Openings (Thinnening Profile)
    for i in range(S+1, 2*S+1):
        n = i - 1 - S
        clone = min_tree.clone()
        clone.areaOpen(thresholds[n])
        ap[:, :, i] = maxi - clone.getImage()
        
    return ap

def EP(im, connexity=1):
    n_features = option.n_features
    extrema = option.extrema
    S = option.S

    # Element structurant
    Se = np.ones((3, 3), dtype=bool)
    if connexity == 1:
        Se[0, 0] = False
        Se[2, 0] = False
        Se[0, 2] = False
        Se[2, 2] = False
    
    # Construction du tableau résultat
    h, w = im.shape
    EPa = np.zeros((h, w, n_features))
    #EPh = np.zeros((h, w, n_features))
    
    # Max value of image for negative
    maxi = im.max()
    neg = maxi - im
    
    # Min-tree (max-tree with negative image)
    min_tree = siamxt.MaxTreeAlpha(neg, Se)
    # Max-tree
    max_tree = siamxt.MaxTreeAlpha(im, Se)
    
    # Area extinction
    area_min = min_tree.node_array[3, :]
    area_max = max_tree.node_array[3, :]

    # Extinction values
    extAreaMin = min_tree.computeExtinctionValues(area_min, "area")
    extAreaMax = max_tree.computeExtinctionValues(area_max, "area")
    #extContrastMin = min_tree.computeExtinctionValues(min_tree.computeHeight(), "height")
    #extContrastMax = max_tree.computeExtinctionValues(max_tree.computeHeight(), "height")
    
    # Thickening Profile
    for i in range(S):
        n = S - i - 1
        clone = min_tree.clone()
        clone.extinctionFilter(extAreaMin, extrema[n])
        EPa[:, :, i] = maxi - clone.getImage()
        # EPh
        #clone = min_tree.clone()
        #clone.extinctionFilter(extContrastMin, extrema[n])
        #EPh[:, :, i] = maxi - clone.getImage()
        
    EPa[:, :, S] = im
    #EPh[:, :, S] = im
        
    # Thinning Profile
    for i in range(S+1, 2*S+1):
        n = i - 1 - S
        clone = max_tree.clone()
        clone.extinctionFilter(extAreaMax, extrema[n])
        EPa[:, :, i] = clone.getImage()
        # EPh
        #clone = max_tree.clone()
        #clone.extinctionFilter(extContrastMax, extrema[n])
        #EPh[:, :, i] = clone.getImage()
        
    return EPa