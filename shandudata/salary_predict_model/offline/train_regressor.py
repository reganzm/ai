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
    for e in elems[2:8]:
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


def get_label_vector(path, is_lower_salary=True):
    if is_lower_salary:
        label_index = 0
    else:
        label_index = 1
    Y = []
    for line in open(path):
        label = line.strip().split('\t')[label_index]
        y = int(label)
        Y.append(y)
    return Y


def get_predict_class_and_prob(clf, X):
    y = clf.predict(X)
    return y, 1.0


class PrecStat(object):

    def __init__(self):
        self.tot_error = 0.0
        self.tot_error_ratio = 0.0
        self.tot_num = 0

    def add_instance(self, pred_value, tag_value):
        self.tot_error += abs(pred_value - tag_value)
        self.tot_error_ratio += abs(pred_value - tag_value) * 1.0 / (tag_value + 0.000001)
        self.tot_num += 1

    def output(self):
        print "mean_error=%f" % (self.tot_error / self.tot_num)
        print "mean_error_ratio=%f" % (self.tot_error_ratio / self.tot_num)


def test_model(lower_clf, upper_clf, test_data_path):
    lower_prec_stat = PrecStat()
    upper_prec_stat = PrecStat()
    lower_prec_num = 0
    upper_prec_num = 0
    tot_num = 0
    for line in open(test_data_path):
        elems = line.strip().split('\t')
        lower_test_label = int(elems[0])
        upper_test_label = int(elems[1])
        X_test = get_fts_vector(line)
        pred_y_lower, p = get_predict_class_and_prob(lower_clf, X_test)
        pred_y_upper, p = get_predict_class_and_prob(upper_clf, X_test)
        # lower_prec_stat.add_instance(pred_y_lower[0],lower_test_label)
        # upper_prec_stat.add_instance(pred_y_upper[0],upper_test_label)
        lower_prec_stat.add_instance(pred_y_lower, lower_test_label)
        upper_prec_stat.add_instance(pred_y_upper, upper_test_label)
        print line.strip(), pred_y_lower, pred_y_upper
        if pred_y_lower > lower_test_label and pred_y_lower < upper_test_label:
            lower_prec_num += 1
        if pred_y_upper > lower_test_label and pred_y_upper < upper_test_label:
            upper_prec_num += 1
        tot_num += 1
    lower_prec_stat.output()
    upper_prec_stat.output()
    print "lower prec=%f" % (lower_prec_num * 1.0 / tot_num)
    print "upper prec=%f" % (upper_prec_num * 1.0 / tot_num)

if __name__ == '__main__':
    train_data_path = sys.argv[1]
    test_data_path = sys.argv[2]
    feature_space = FeatureSpace(train_data_path)

    if os.path.exists('model/lower.model'):
        with open('model/lower.model', 'rb') as fid:
            lower_clf = cPickle.load(fid)
        with open('model/upper.model', 'rb') as fid:
            upper_clf = cPickle.load(fid)
        logging.info("load regression model from file.")
    else:
        # lower_clf=GradientBoostingRegressor(loss='lad',n_estimators=1000)
        # upper_clf=GradientBoostingRegressor(loss='lad',n_estimators=1000)
        lower_clf = RandomForestRegressor(n_estimators=100)
        upper_clf = RandomForestRegressor(n_estimators=100)
        # lower_clf=ExtraTreeRegressor()
        # upper_clf=ExtraTreeRegressor()
        # lower_clf,upper_clf=RandomForestRegressor(n_estimators=100)
        X = feature_space.get_train_input_matrix()
        Y_lower = get_label_vector(train_data_path, is_lower_salary=True)
        lower_clf.fit(X, Y_lower)
        Y_upper = get_label_vector(train_data_path, is_lower_salary=False)
        upper_clf.fit(X, Y_upper)
        with open('model/lower.model', 'wb') as fid:
            cPickle.dump(lower_clf, fid)
        with open('model/upper.model', 'wb') as fid:
            cPickle.dump(upper_clf, fid)

    test_model(lower_clf, upper_clf, test_data_path)
