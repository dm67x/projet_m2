from os import path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from skimage import img_as_ubyte
import numpy as np
from tqdm import tqdm
import pickle
import process
import option

class RFClassifier:
    def __init__(self, profiles=None, labels=None):
        trees = option.trees
        classes = option.classes

        self.classes = classes
        self.profiles = profiles
        self.labels = labels
        self.rf = RandomForestClassifier(trees, n_jobs=-1)
        self.kf = KFold(n_splits=10)

    def train(self):
        print("Entrainement en cours...")

        profiles = self.profiles
        labels = self.labels
        rf = self.rf
        kf = self.kf

        nImages, d = profiles.shape
        if nImages == 0:
            pass

        X = profiles
        y = labels

        # EP
        with tqdm(desc="KFold", total=10) as pbar:
            for train_index, test_index in kf.split(X, y):
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                rf.fit(X_train, y_train)
                print("Test accuracy:", rf.score(X_test, y_test) * 100, "%", flush=True)
                pbar.update()

        # prediction
        print("Accuracy:", rf.score(X, y) * 100, "%")
        # Matrice de confusion
        y_pred = rf.predict(X)
        print(confusion_matrix(y, y_pred))
        # Importance
        print("Importances :", rf.feature_importances_)
        print("Entrainement terminé")

    def open(self, filename):
        with open(filename, 'rb') as file:
            self.rf = pickle.load(file)

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.rf, file)

    def predict(self, im):
        classes = self.classes
        rf = self.rf
        h, w, d = im.shape
        X = np.zeros((1, d * h * w))
        X[0, :] = im.reshape((h * w * d))
        pred = rf.predict(X)
        return pred