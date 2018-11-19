# coding=utf-8
import cPickle
import codecs
import logging
import math
import os
import sys

from sklearn.ensemble import *
from sklearn.linear_model import *
from sklearn.svm import SVR
from sklearn.tree import *

import numpy as np


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_fts_vector(line):
    elems = line.strip().split('\t')
    fts = []
    for e in elems[2:5]:
        fts.append(int(e))
    return fts


class FeatureSpace(object):

    def __init__(self, train_data_path):
        self.train_data_path = train_data_path

    def get_train_input_matrix(self):
        points = []
        for line in open(self.train_data_path):
            fts = get_fts_vector(line)
            points.append(fts)
        return np.array(points)


def get_label_vector(path):
    Y = []
    for line in open(path):
        label = line.strip().split('\t')[0]
        y = int(label)
        Y.append(y)
    return Y


def get_predict_class_and_prob(clf, X):
    y = clf.predict(X)
    return y[0], 1.0


class PrecStat(object):

    def __init__(self):
        self.tot_prec_num = 0
        self.tot_num = 0

    def add_instance(self, pred_value, tag_value):
        if pred_value == tag_value:
            self.tot_prec_num += 1
        self.tot_num += 1

    def output(self):
        print "prec=%f" % (self.tot_prec_num * 1.0 / self.tot_num)


def test_model(clf, test_data_path):
    prec_stat = PrecStat()
    for line in open(test_data_path):
        elems = line.strip().split('\t')
        test_label = int(elems[0])
        X_test = get_fts_vector(line)
        pred_y, p = get_predict_class_and_prob(clf, X_test)
        prec_stat.add_instance(pred_y, test_label)
    prec_stat.output()

if __name__ == '__main__':
    train_data_path = sys.argv[1]
    test_data_path = sys.argv[2]
    feature_space = FeatureSpace(train_data_path)

    if os.path.exists('model/lower.model'):
        with open('model/lower.model', 'rb') as fid:
            clf = cPickle.load(fid)
        logging.info("load classify model from file.")
    else:
        clf = RandomForestClassifier(n_estimators=100)
        X = feature_space.get_train_input_matrix()
        Y = get_label_vector(train_data_path)
        clf.fit(X, Y)
        with open('model/salary.model', 'wb') as fid:
            cPickle.dump(clf, fid)

    test_model(clf, test_data_path)
