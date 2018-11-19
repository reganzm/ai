# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-24
@Content: 
"""

import re
from argparse import ArgumentParser

from dateutil.parser import parse
from pinbot_clean.normalization import \
    (normalization_area_name, normalization_industry, normalization_position_name, normalization_job_detail)
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import udf
from pyspark.sql.types import *


def preprocess_job_profile(df, output_path):
    """
    :param df: type(DateFrame), 职位信息
    :param output_path: 输出文件路径
    :return:
    """
    columns = [
        "position_name",  # 职位名
        "industry",  # 行业
        "address",  # 工作地点
        "add_time",  # 发布时间
        "update_time",  # 更新时间
        "recruit_num",  # 招聘人数
        "expire_time",  # 过期时间
        "job_desc",  # 职位jd描述
        "avg_salary",  # 职位平均薪资
        "date_time",  # 职位更新时间
    ]

    df = df.withColumn("position_name", udf(normalization_position_name)(df.title))
    df = df.withColumn("industry", udf(normalization_industry)(df.industry))
    df = df.withColumn("address", udf(normalization_area_name)(df.expect_area))
    df = df.withColumn("avg_salary", udf(get_job_salary)(df.salary_text))
    df = df.withColumn("date_time", udf(get_publish_month, StringType())(df.update_time))
    df = df.withColumn('job_desc', udf(normalization_job_detail)(df.job_desc))

    # 过滤条件
    df = df.dropna(how="all", subset=["title", "job_desc"])
    #  将职位信息预处理后的结果保存至指定文件
    return df.select(columns).write.mode('overwrite').save(output_path)


re_salary = re.compile(r"(\d+)")


def get_job_salary(salary_text):
    """计算供职薪资"""
    salary = '面议'
    salary_list = re_salary.findall(salary_text)
    if salary_list:
        if len(salary_list) == 2:
            salary = (int(salary_list[0]) + int(salary_list[1])) / 2
        elif len(salary_list) == 1:
            salary = int(salary_list[0])
    return salary


def get_publish_month(tm):
    """获取发布时间"""
    date_time = parse(tm[0])
    format_time = date_time.strftime("%Y-%m")
    return format_time


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历基本信息预处理"
    parser.add_argument('-i', '--input_path', action='store', dest='input_path',
                        help='简历基本信息文件路径，json格式')
    parser.add_argument('-o', '--output_path', action='store', dest='output_path',
                        help='简历基本信息处理后的文件保存路径， parquet格式')

    # 运行参数
    args = parser.parse_args()
    if args.input_path is None:
        parser.print_help()

    # spark 环境初始化
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # 加载数据
    profile_df = sqlContext.read.json(args.input_path)
    preprocess_job_profile(profile_df, args.output_path)
