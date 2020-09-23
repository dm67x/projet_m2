from os import path, listdir, remove, makedirs
import numpy as np
import sys
from skimage import io, img_as_ubyte
from skimage.transform import resize
from tqdm import tqdm
import matplotlib.pyplot as plt
import option
from classifier import RFClassifier
import process
from multiprocessing import Pool
import pandas as pd
import ntpath

def _process(args):
    filename, i, aep = args
    outputDir = option.outputDir
    name = path.splitext(ntpath.basename(filename))[0]
    im = img_as_ubyte(io.imread(filename, as_gray=True))
    if aep == "ap":
        data = process.AP(im)
    else:
        data = process.EP(im)
    np.savez_compressed(path.join(outputDir, name), data=data, labelIndex=i)

def _save(aep):
    labelFile = option.labelFile
    maxImages = option.maxImages
    outputDir = option.outputDir
    inputDir = option.inputDir
    n_features = option.n_features

    # Suppression des contenus du repertoire de sortie
    if path.exists(outputDir):
        for f in listdir(outputDir):
            remove(path.join(outputDir, f))
    else:
        makedirs(outputDir)

    # Récupération des labels
    df = pd.read_csv(labelFile)
    total = maxImages if maxImages > 0 else len(df['ID'])
    labels = np.zeros((total,))
    files = []

    with tqdm(total=total, desc="Récupération des labels") as pbar:
        for i in range(total):
            files.append(str(df['ID'][i]))
            labels[i] = int(df['Category'][i])
            pbar.update()

    n = labels.shape[0]
    print("Nombre d'etiquettes :", n)
    print("Nombre de fichiers :", len(files))
    # Sauvegarde des labels
    np.save(path.join(outputDir, "labels.npy"), labels)

    # Extraction des profils d'attribut et des profils d'"extinction"
    args = []
    for index, file in enumerate(files):
        filename = path.join(inputDir, file + ".png")
        if path.exists(filename) and path.isfile(filename):
            args.append((filename, index, aep))

    with Pool() as pool:
        with tqdm(desc="Extraction des profils", total=len(files)) as pbar:
            for i, _ in enumerate(pool.imap_unordered(_process, args)):
                pbar.update()

    # Récupérer les profils et labels
    lbl = np.load(path.join(outputDir, "labels.npy"))
    max_ = len(files)

    # Finalite
    h, w = 28, 28
    images = np.zeros((max_, n_features * h * w), dtype=np.uint8)
    labels = np.zeros((max_), dtype=np.uint8)

    j = 0
    with tqdm(desc="Lecture des profils", total=max_) as pbar:
        for f in listdir(outputDir):
            filename = path.join(outputDir, f)
            if path.isfile(filename) and filename.endswith(".npz"):
                p = np.load(filename)
                data = p['data']
                _data = np.zeros((h, w, n_features))
                for d in range(n_features):
                    _data[:, :, d] = resize(data[:, :, d], (h, w), anti_aliasing=False)
                images[j, :] = _data[:, :, :].reshape((h * w * n_features))
                labels[j] = lbl[int(p['labelIndex'])]     
                j += 1
                pbar.update()

    # Classification
    classifier = RFClassifier(images, labels)
    classifier.train()
    classifier.save(path.join(outputDir, "model.pkl"))

def _load(im, attr):
    outputDir = option.outputDir
    testDir = option.testDir
    classes = option.classes

    classifier = RFClassifier()
    classifier.open(path.join(outputDir, "model.pkl"))

    p = None
    if attr == 0: # EP
        p = process.EP(im)
    else:
        p = process.AP(im)

    p = resize(p, (28, 28), anti_aliasing=False)
    pred = classifier.predict(p)
    print(classes[int(pred)])
    plt.imshow(im, cmap='gray')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: %s <predict/build>" % sys.argv[0])
        exit(1)

    if sys.argv[1] == "build":
        if len(sys.argv) != 3:
            print("usage: %s build <ep/ap>" % sys.argv[0])
            exit(1)

        if sys.argv[2] == "ap" or sys.argv[2] == "ep":
            _save(sys.argv[2])
        else:
            print("usage: %s build <ep/ap>" % sys.argv[0])
            exit(1)
    elif sys.argv[1] == "predict":
        if len(sys.argv) < 3:
            print("usage: %s predict <image> <ep/ap>" % sys.argv[0])
            exit(1)

        attr = 0 if len(sys.argv) < 4 else 1
        im = img_as_ubyte(io.imread(sys.argv[2], as_gray=True))
        _load(im, attr)
    else:
        print("usage: %s <predict/build>" % sys.argv[0])
        exit(1)
    