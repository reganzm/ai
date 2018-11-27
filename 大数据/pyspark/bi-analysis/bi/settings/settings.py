# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-24
@Content: 全局配置信息
"""

import os
from os.path import dirname, join

# 项目根目录
BASE = dirname(dirname(dirname(__file__)))
LOG_PATH = join(BASE, "logs/")
OUTPUT_PATH = join(BASE, "output_data/")

# 薪资最大值与最小值
SALARY_MIN = 1000
SALARY_MAX = 100000

# 最小年龄
MIN_AGE = 18
# 最大年龄
MAX_AGE = 70

# 毕业多少年内作为有效数据
LATEST_YEAR = 5
# 最近多少年更新简历作为活跃简历
ACTIVE_YEAR = 3

# 聚合后的NULL值默认为不限
NA = "不限"
# 数据筛选最小数必须大于
MIN_NUM = 3
# 筛选最小薪资
MIN_SALARY = 1000
# 字符串最大长度
MAX_LENGTH = 50
# 字符串最小长度
MIN_LENGTH = 1

# spark 安装目录
SPARK_HOME = "/home/bigdata/tools/spark-2.3.0-bin-hadoop2.7"

# python3环境目录
os.environ["PYSPARK_PYTHON"] = "/home/bigdata/.virtualenvs/bi-analysis/bin/python3"

# 数据目录配置
HOME = "/home/bigdata/data/BI/BI_TEST"

# json文件路径
JPROFILE_PATH = "{}/resume_profile.json".format(HOME)
JEDUCATION_PATH = "{}/resume_educations.json".format(HOME)
JWORK_PATH = "{}/resume_works.json".format(HOME)
JJOB_PATH = "{}/feed_job.json".format(HOME)
JCERTIFICATE_PATH = "{}/resume_certificates.json".format(HOME)

# 预处理文件路径
PROFILE_PATH = "{}/resume_profile.parquet".format(HOME)
EDUCATION_PATH = "{}/resume_educations.parquet".format(HOME)
WORK_PATH = "{}/resume_works.parquet".format(HOME)
JOB_PATH = "{}/feed_job.parquet".format(HOME)
RESUME_PATH = "{}/resume.parquet".format(HOME)

# 存储数据库信息
MYSQL_URL = "jdbc:mysql://localhost:3306/BI_V1?user=root&password=123456&autoReconnect=true&useUnicode=false&characterEncoding=gbk&useSSL=false"
