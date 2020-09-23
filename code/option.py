trees = 200
inputDir = "images/trains"
outputDir = "output"
testDir = "images/tests"
labelFile = "labels/train.csv"
maxImages = 500
thresholds = [ 16, 32, 64, 128, 256 ]
classes = [ 
    "autre", 
    "mitochondrie",
    "reticulum endoplasmique",
    "membrane nucleaire",
    "membrane cellulaire" 
]
S = len(thresholds)
alpha = 2
extrema = [int(alpha**(i+1)) for i in range(S)]
n_features = 2*S+1