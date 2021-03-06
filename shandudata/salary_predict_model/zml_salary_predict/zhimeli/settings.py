# -*- coding: utf-8 -*-
"""
@author: zhangmin
@Date: 2018-10-10
@Content: 配置信息
"""

import os

# 数据HDFS根路径
HOME = '/user/bigdata/BI/resume_flatten_v1_20180813/'

# 薪资最大值与最小值
SALARY_MIN = 1000
SALARY_MAX = 30000

# 从resume_works中计算得出，注意薪资log放缩，薪资要乘以薪酬的增长率

# +-------+-------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------------------------------+
# |summary|LOG((POWER(1.067, (year(current_date()) - year(end_time))) * salary_min))|LOG((POWER(1.067, (year(current_date()) - year(end_time))) * salary_max))|(year(current_date()) - year(end_time))|
# +-------+-------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------------------------------+
# |  count|                                                                  8839243|                                                                  8839243|                                8839243|
# |   mean|                                                        8.225222333689228|                                                        8.757867197348704|                      3.381645916963704|
# | stddev|                                                       0.6178012919149061|                                                      0.48041340283925144|                     1.8417804634863966|
# |    min|                                                       6.9726062513017535|                                                        7.067916431106078|                                      1|
# |    max|                                                        10.65754895122378|                                                       10.752859131028105|                                      7|
# +-------+-------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------------------------------+


# 最小薪资均值和方差
SALARY_MIN_MEAN = 8.225222333689228
SALARY_MIN_STD = 0.6178012919149061

# 最大薪资均值和方差
SALARY_MAX_MEAN = 8.757867197348704
SALARY_MAX_STD = 0.48041340283925144

# python3环境目录
os.environ["PYSPARK_PYTHON"] = "/home/bigdata/.virtualenvs/bi-analysis/bin/python3"

# 输入文件路径
INPUT_PATH = "{}/resume_works.json".format(HOME)
OUTPUT_PATH = "{}/resume_works_zhimeli.parquet".format(HOME)

# 阻尼系数
DAMP_COEF = 0.8
# 薪资增长速率,来自2016年全国平均薪资增长率
SALARY_GROWTH_RATE = 0.067
