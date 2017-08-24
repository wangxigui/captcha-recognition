#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from sklearn.svm import SVC
from sklearn import grid_search
import numpy as np
from sklearn import cross_validation as cs
from sklearn.externals import joblib

from icofeature import cutPictures, getBinayPix

PROJECT_HOME = os.path.abspath('.')
DATA_HOME = os.path.join(PROJECT_HOME, 'input/ico3')

category_dirs = DATA_HOME + '/category'
cut_dirs = DATA_HOME + '/cut'
train_data_file = DATA_HOME + '/train_data.txt'
out_cut_dirs = os.path.abspath('.') + '/output/ico3/cut'

PKL = os.path.abspath('.') + '/model/ico.pkl'

def load_data():
    dataset = np.loadtxt(train_data_file, dtype=str, delimiter=',')
    return dataset

def cross_validate():
    dataset = load_data()
    row, col = dataset.shape
    X = dataset[:, :col-1]
    Y = dataset[:, -1]
    clf = SVC(kernel='rbf', C=1000)
    scores = cs.cross_val_score(clf, X, Y, cv=5)
    print('Accuracy: %0.2f (+/- %0.2f)' %(scores.mean(), scores.std() * 2))
    return clf

def train():
    dataset = load_data()
    row, col = dataset.shape
    X = dataset[:, :col-1]
    Y = dataset[:, -1]
    clf = SVC(kernel='rbf', C=1000)
    clf.fit(X,Y)
    joblib.dump(clf, PKL)

def predict(captcha):
    clf = joblib.load(PKL)
    cutPictures(captcha, out_cut_dirs)

    digits = []

    for im in os.listdir(out_cut_dirs):
        print im
        path = os.path.join(out_cut_dirs, im)
        binary = getBinayPix(path)
        feature = np.array(binary).reshape(1, -1)
        print 'word is: ', clf.predict(feature)
        #os.remove(path)


if __name__ == '__main__':
    #train()
    captcha = os.path.abspath('.') + '/input/ico3/1503570774853382.jpg'
    predict(captcha)
