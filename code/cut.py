import siamxt
from skimage import io
import option
from os import path
import numpy as np

def gcf_val(im, p, l):
    x = im.sum()
    y = p[:, :, l].sum()
    return abs(x - y)

def gcf_pix(im, p, l):
    pp = p[:, :, l]
    i = np.intersect1d(im, pp)
    return abs(im.size - i.size)

def cut_selection(im, connexity=1):
    # Element structurant
    Se = np.ones((3, 3), dtype=bool)
    if connexity == 1:
        Se[0, 0] = False
        Se[2, 0] = False
        Se[0, 2] = False
        Se[2, 2] = False

    # Computation of tree representation T(f)
    T = siamxt.MaxTreeAlpha(im, Se)
    # Computation of attribute A(T) on nodes
    A = T.node_array[3, :]
    # Sort
    lambda_ = np.unique(np.sort(A))
    L = lambda_.shape[0]

    # Compute profile
    h, w = im.shape
    profile = np.zeros((h, w, L))
    for i in range(L):
        clone = T.clone()
        clone.areaOpen(lambda_[i])
        profile[:, :, i] = clone.getImage()

    GCF = np.zeros((L,))
    for i in range(L):
        GCF[i] = gcf_pix(im, profile, i)

    # Problème de compréhension de l'algo
    # au niveau de l'estimation G^C^F (piecewise linear regression)
    
    nth = 1
    cut_t = [lambda_[0]]
    while nth < L:
        GCF_p = np.zeros((nth,))
        for i in range(nth):
            GCF_p[i] = gcf_pix(im, profile, i)

        gcf_t = gcf_pix(im, profile, nth)
        if GCF_p[:] == GCF[:nth]:
            break
        cut_t.append(lambda_[nth])
        nth += 1

    L_p = nth
    print(L_p)
    print(cut_t)

if __name__ == "__main__":
    inputDir = option.inputDir
    cut_selection(io.imread(path.join(inputDir, "3.png")))