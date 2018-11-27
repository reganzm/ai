# -*- coding: utf-8 -*-
"""
@author: zhangmin
@Date: 2018-10-08
@Content: 配置信息
"""

import os
from os.path import dirname, join

#数据HDFS根路径
HOME='/user/bigdata/BI/resume_flatten_v1_20180813/'


# 薪资最大值与最小值
SALARY_MIN = 2000
SALARY_MAX = 30000


# python3环境目录
os.environ["PYSPARK_PYTHON"] = "/home/bigdata/.virtualenvs/bi-analysis/bin/python3"


#输入文件路径
INPUT_PATH_0 = "{}/resume_educations_with_codes_v2.parquet".format(HOME)
INPUT_PATH_1 = "{}/resume_works_zhimeli_locations_v2.parquet".format(HOME)
INPUT_PATH_2 = '/data/datasets/salary_predict/v2/university.csv'

OUTPUT_PATH = "{}/salary_predict_features_v2.parquet".format(HOME)

#最小薪资均值和方差
SALARY_MIN_MEAN=8.225222333689228
SALARY_MIN_STD =0.6178012919149061

#最大薪资均值和方差
SALARY_MAX_MEAN=8.757867197348704
SALARY_MAX_STD =0.48041340283925144


#阻尼系数
DAMP_COEF=0.8
#薪资增长速率,来自2016年全国平均薪资增长率
SALARY_GROWTH_RATE = 0.067


