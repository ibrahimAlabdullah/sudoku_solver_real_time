import numpy as np
import os
import cv2
import random
from sklearn.svm import SVC

IMAGE_WIDTH = 28
IMAGE_HEIGHT = 28



def create_dataset():
    DATADIR = r'DataSet'
    CATEGORIES = ['0','1','2','3','4','5','6','7','8','9']
    training_data= []
    for categories in CATEGORIES:
        path = os.path.join(DATADIR , categories)

        num_class = CATEGORIES.index(categories)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path , img))
                img_array = cv2.resize(img_array , (IMAGE_WIDTH , IMAGE_HEIGHT))
                winSize = (img_array.shape[1], img_array.shape[0])
                blockSize = (4,4)
                blockStride = (4, 4)
                cellSize = (2, 2)
                nbins = 5
                hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
                locations = []
                hist = hog.compute(img_array, None, None, locations)
                training_data.append([hist , num_class])
            except Exception as e:
                print(e)
    return training_data

data_set = create_dataset()
random.shuffle(data_set)

X_train = []
y_train = []

for sample in data_set:
    X_train.append(sample[0])
    y_train.append(sample[1])

X_train = np.asarray(X_train)
y_train = np.asarray(y_train)
print(X_train.shape)

X_train = X_train[0:X_train.shape[0], 0:X_train.shape[1], 0]

def classify():
    #kernel='sigmoid'
    svcClassifier = SVC(gamma=0.001 , C=100)
    svcClassifier.fit(X_train,y_train)
    return svcClassifier

'''
clf = classify()
img = cv2.imread('digit/9.jpg')
img = cv2.resize(img, (28, 28))
winSize = (img.shape[1], img.shape[0])
blockSize = (4, 4)
blockStride = (4, 4)
cellSize = (2, 2)
nbins = 5
hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
locations = []
hist = hog.compute(img, None, None, locations)

hist = np.asarray(hist)
hist = hist.reshape(1, -1)
print(clf.predict(hist))
'''



'''
digits = datasets.load_digits()
digit_x = digits.data[:-1]
digit_y = digits.target[:-1]
X_digit = []
for img in digit_x:
    img = img.reshape(8,8)
    img = cv2.resize(img , (28,28))
    img_array = np.empty( (28,28,3) , dtype=np.uint8)
    img_array[: ,:, 0] = img
    img_array[:, :, 1] = img
    img_array[:, :, 2] = img

    #img_array = cv2.resize(img_array , (IMAGE_WIDTH , IMAGE_HEIGHT))

    winSize = (img_array.shape[1], img_array.shape[0])
    blockSize = (4, 4)
    blockStride = (4, 4)
    cellSize = (2, 2)
    nbins = 5
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    locations = []
    hist = hog.compute(img_array, None, None, locations)
    X_digit.append(hist)
    #training_data.append([hist , num_class])


X_digit = np.asarray(X_digit)
digit_y = np.asarray(digit_y)

X_digit = X_digit[0:X_digit.shape[0], 0:X_digit.shape[1], 0]
'''

