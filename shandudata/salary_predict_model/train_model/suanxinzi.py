# coding:utf-8
'''
Created on 2014年12月12日

@author: likaiguo
@summary:
#1.读取数据载入pandas,以后的数据都统一通过csv存取
a.数据标注非常复杂

关于职位:
分大类,关键词,大小写,同义中英文

关于学校:
海归

985
211
普通二本
三本

培训类学院

500 400  300  200 100  50


关于学历:
初中,高中,职业技术中学,
大专,专升本,成人教育,网络教育,成考,自考,
本科,双学位,
硕士,工程,专业,在职,MBA,EMBA
博士,在职博士

赋值:10  100   200  300 400

#2.将原始数据转换为数值向量数据  scikit-learn pandas
#3.训练模型 scikit-learn
#4.测试集
#5.保存训练结果
'''
from __future__ import unicode_literals

import cPickle as pickle
import json

import codecs
import numpy as np
import os
import pandas as pd
from datetime import datetime
from pandas import concat
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.grid_search import GridSearchCV

from data_to_vector import data_to_numuber
from pre_mark_job_title import mark_job_cls
from school_cate_mark import mark_school_cls


def simplify_value(value):
    if type(value) == unicode:
        if '|' in value:
            value = value.split('|')[0]
        elif '-' in value:
            value = value.split('-')[0]
        elif len(value) >= 1:
            value = value.split()[0]
    else:
        print value, type(value)

    return value


def mark_data(data, out_path='data_all_marked_school_job.csv'):
    # 然后是数据转换,将所有字段数值化
    # 较为复杂的是职位和学校类型的转换,都用查表的方式
    # 标记学校
    all_school_dict_list = []
    for school in data['school']:
        #         print school, type(school), not school
        if type(school) != unicode:
            school_dict = {}
        else:
            school_dict = mark_school_cls(school)
        all_school_dict_list.append(school_dict)

    all_schools_df = pd.DataFrame(all_school_dict_list)

    # 标记职位名称
    mark_position_titles_list = []
    for position_title in data['position_title']:
        mark_position_titles_list.append(mark_job_cls(position_title))

    position_title_marked_df = pd.DataFrame(mark_position_titles_list)

    # 合并原始数据和标记数据
    data_all_marked_position_title = concat(
        [data, all_schools_df, position_title_marked_df], axis=1)
    data_all_marked_position_title['city'].apply(simplify_value)

    data_all_marked_position_title.to_csv(out_path, encoding='utf-8')
    print 'write to %s' % out_path

    return data_all_marked_position_title


def get_json_data(input_path='/media/likaiguo/disk7/github/salary_predict_model/offline/data/salary.json', ):
    lines = codecs.open(input_path, 'r', 'utf-8').readlines()
    dict_into_list = [json.loads(line) for line in lines]
    data_frame = pd.DataFrame(dict_into_list)
    data_frame.to_csv('old_data_works.csv', encoding='utf-8')
    return data_frame


def train(persisit_dir='.', prefix=''):
    model_min_fpath = persisit_dir + '/model_min_%s.model' % prefix
    model_max_fpath = persisit_dir + '/model_max_%s.model' % prefix
    model_median_fpath = persisit_dir + '/model_median_%s.model' % prefix
    print model_min_fpath
    if os.path.exists(model_min_fpath):
        t_now = datetime.now()
        print 'load model start!!!', t_now
        model_min_f = open(model_min_fpath, 'rb')
        model_max_f = open(model_max_fpath, 'rb')
        model_median_f = open(model_median_fpath, 'rb')
        model_min = pickle.load(model_min_f)
        model_max = pickle.load(model_max_f)
        model_median = pickle.load(model_median_f)
        delta = datetime.now() - t_now
        print 'load model success!!!', datetime.now(), delta.seconds
    else:
        n_estimators = 200
        max_features = 0.5
        max_depth = 10
        model_min = RandomForestRegressor(
            n_estimators=n_estimators,
            max_features=max_features,
            max_depth=max_depth)
        model_min = model_min.fit(X_train, y_train_min)

        n_estimators = 200
        max_features = 0.5
        max_depth = 10
        model_max = RandomForestRegressor(
            n_estimators=n_estimators,
            max_features=max_features,
            max_depth=max_depth)
        model_max = model_max.fit(X_train, y_train_max)

        n_estimators = 200
        max_features = 0.5
        max_depth = 10
        model_median = RandomForestRegressor(
            n_estimators=n_estimators,
            max_features=max_features,
            max_depth=max_depth)

        model_median = model_median.fit(X_train, y_train_median)

        model_min_f = open(model_min_fpath, 'wb')
        model_max_f = open(model_max_fpath, 'wb')
        model_median_f = open(model_median_fpath, 'wb')

        pickle.dump(model_min, model_min_f)
        pickle.dump(model_max, model_max_f)
        pickle.dump(model_median, model_median_f)
        print 'dump model success!!!'
    return model_min, model_median, model_max


def score(y_prediction, y_test, y_test_median, alpha=0.1):
    print len(y_prediction), len(y_test), len(y_test_median)
    # 绝对等于
    print "绝对等于:prediction accuracy:", np.sum(y_test == y_prediction) * 1. / len(y_test)
    # 在一定区间
    true_vlaues = (
                      y_prediction * (1 - alpha) < y_test) & (y_test < y_prediction * (1 + alpha))
    print "在区间内:prediction accuracy:", np.sum(true_vlaues) * 1. / len(y_test)
    # 距离平均值
    true_median = (y_prediction * (1 - alpha) <
                   y_test_median) & (y_test_median < y_test_median * (1 + alpha))
    print "区间内距离平均值:prediction accuracy:", np.sum(true_median) * 1. / len(y_test)

    print '**' * 50


def test_score(model_min, model_max, model_median):
    y_prediction_min = model_min.predict(X_test)
    y_prediction_median = model_median.predict(X_test)
    y_prediction_max = model_max.predict(X_test)

    y_prediction_median_max_min = (y_prediction_min + y_prediction_max) / 2

    score(y_prediction_min, y_test_min, y_test_median)

    score(y_prediction_max, y_test_max, y_test_median)

    score(y_prediction_median, y_test_median, y_test_median)

    score(y_prediction_median_max_min, y_test_median, y_test_median)

    y_result_df = pd.DataFrame()
    y_result_df['y_prediction_min'] = y_prediction_min
    y_result_df['y_test_min'] = y_test_min

    y_result_df['y_prediction_max'] = y_prediction_max
    y_result_df['y_test_max'] = y_test_max

    y_result_df['y_prediction_median'] = y_prediction_median
    y_result_df['y_test_median'] = y_test_median

    y_result_df['y_prediction_median_max_min'] = y_prediction_median_max_min

    # y_result_df['y_test_median'] = y_test_median


def parameter_tuning(X, y):
    """
    @summary: 参数调试
    """
    parameter_grid = {
        'max_features': [0.1, 0.5],
        'max_depth': [5., 10., 20., None]
    }
    grid_search = GridSearchCV(RandomForestClassifier(n_estimators=200), parameter_grid,
                               cv=5, verbose=3)

    grid_search.fit(X, y)
    sorted(grid_search.grid_scores_, key=lambda x: x.mean_validation_score)
    print grid_search.best_score_
    print grid_search.best_params_


sorted_columns = [
    'lower_salary',
    'upper_salary',
    #                   'expect_min',
    #                   'expect_max',
    #                 u'age',
    'city',
    'degree',
    'gender',
    'work_len',
    'first_class_1',
    'first_class_2',
    '2nd_class_1',
    '2nd_class_2',
    '3rd_class_1',
    '3rd_class_2',
    '3rd_class_3',
    #                   u'2nd_class',
    #                   'school_level',
    #                   'scale_max',
    #                   'scale_min'
]


def salary_predict(model_min, model_max, model_median, test_data_df):
    test_all_feature_numeric_pd = data_to_numuber(test_data_df)

    test_all_feature_numeric_pd = test_all_feature_numeric_pd.fillna(0)
    predict_data = test_all_feature_numeric_pd[sorted_columns]

    train_data = predict_data.values[:15000]

    X = train_data[:, 2:]
    #     y_min = train_data[:, 0]
    #     y_max = train_data[:, 1]
    # print 'train_data', train_data[0],
    # print y_min, y_max, '|', X[0]

    parameter = 1.5

    y_min = model_min.predict(X) * parameter
    y_max = model_median.predict(X) * parameter
    y_median = model_max.predict(X) * parameter
    # print y_min[0], y_max[0], y_median[0]
    return y_min[0], y_max[0], y_median[0]


def test_salay_predict(model_min, model_max, model_median):
    test_data = [

        {
            u'lower_salary': 1000,
            u'upper_salary': 2000,
            u'age': 28,
            u'city': u'北京',
            u'degree': u'硕士',
            u'gender': u'男',
            u'work_len': 2,
            u'first_class': u'技术',
            u'school_level': u"中国一流大学",
            "2nd_class": u"后端开发|工程师",
            "3rd_class_4": "",
            "3rd_class_2": "",
            "3rd_class_3": "",
            "3rd_class_1": u"Java",
            "second_class_2": u"工程师",
            "second_class_1": u"后端开发",
            "first_class": u"技术",
            "3rd_class": u"Java",
            "third_class_1": u"Java",

            "first_class_2": u"技术",
            "first_class_1": u"技术",
            "2nd_class_3": "",
            "2nd_class_2": "",
            "2nd_class_1": u"后端开发"
        }
    ]
    test_data_df = pd.DataFrame(test_data)
    salary_predict(model_min, model_max, model_median, test_data_df)


if __name__ == '__main__':

    input_path = 'old_data_works.csv'
    out_path = '%s_output_marked_data.csv' % input_path

    if os.path.exists(out_path):
        data_all_marked_position_title = pd.read_csv(
            out_path, encoding='utf-8')
    else:
        data_frame = pd.read_csv(input_path, encoding='utf-8')
        if 'edu_degree' in data_frame:
            data_frame['degree'] = data_frame['edu_degree']
        data_all_marked_position_title = mark_data(data_frame, out_path)

    print data_all_marked_position_title.columns
    if 'salary_min' in data_all_marked_position_title.columns:
        data_all_marked_position_title['lower_salary'] = data_all_marked_position_title['salary_min']
        data_all_marked_position_title['upper_salary'] = data_all_marked_position_title['salary_max']

    if 'companyscale_min' in data_all_marked_position_title.columns:
        data_all_marked_position_title['scale_min'] = data_all_marked_position_title['companyscale_min']
        data_all_marked_position_title['scale_max'] = data_all_marked_position_title['companyscale_max']
    # # 取合理的标记数据

    job_type = [
        u"游戏",
        u"设计",
        u"技术",
        u"职能",
        u"市场与销售",
        u"运营",
        u"产品",
        u"电商"
    ]
    job_type_1_index = data_all_marked_position_title['first_class_1'].isin(job_type)
    job_type_2_index = data_all_marked_position_title['first_class_2'].isin(job_type)
    data_all_marked_position_title = data_all_marked_position_title[job_type_1_index | job_type_2_index]

    citys = [
        u'北京',
        u'成都',
        u'上海',
        u'广州',
        u'深圳',
        u'杭州',
        u'西安',
        u'武汉',
        u'重庆',
    ]
    citys_index = data_all_marked_position_title['city'].isin(citys)
    data_all_marked_position_title = data_all_marked_position_title[
        citys_index]

    data_all_marked_position_title = data_all_marked_position_title[
        sorted_columns]
    # data_all_marked_position_title = data_all_marked_position_title.dropna()
    # data_all_marked_position_title['work_len'] = data_all_marked_position_title['work_len'] / 12
    data_all_feature_numeric_pd = data_to_numuber(
        data_all_marked_position_title)

    data_all_feature_numeric_pd = data_all_feature_numeric_pd[
        data_all_feature_numeric_pd['lower_salary'] > 0]
    data_all_feature_numeric_pd = data_all_feature_numeric_pd.fillna(0)
    print data_all_feature_numeric_pd.columns
    print sorted_columns
    data_all_feature_numeric_pd = data_all_feature_numeric_pd[sorted_columns]

    df = data_all_feature_numeric_pd[sorted_columns]
    train_data = df.values[:75000]

    X = train_data[:, 2:]
    y_min = train_data[:, 0]
    y_max = train_data[:, 1]
    y_median = (y_min + y_max) / 2

    n = len(X) * 5 / 10

    X_train = X[:n, :]

    y_train_min = y_min[:n]
    y_train_max = y_max[:n]
    y_train_median = y_median[:n]

    X_test = X[n:, :]

    y_test_min = y_min[n:]
    y_test_max = y_max[n:]
    y_test_median = y_median[n:]

    print len(train_data), len(X), n, len(df)
    model_min, model_median, model_max = train()
    test_score(model_min, model_max, model_median)
    test_salay_predict(model_min, model_max, model_median)
