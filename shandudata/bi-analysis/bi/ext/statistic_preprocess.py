# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

from argparse import ArgumentParser

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F

from bi.settings import EDUCATION_PATH, OUTPUT_PATH, PROFILE_PATH, WORK_PATH
from bi.ext.write2file import write2file


def statistic_profile(df, results):
    """统计各个搜索字段的值与权重"""


def statistic_work(df, results):
    results['company_name'] = df.filter(df.company_name.isNotNull()).groupby("company_name").agg(
        F.count("*").alias("person_num"))
    results['industry'] = df.filter(df.industry.isNotNull()).groupby("industry").agg(
        F.count("*").alias("person_num"))
    results['position_name'] = df.filter(df.position_name.isNotNull()).groupby("position_name").agg(
        F.count("*").alias("person_num"))


def statistic_education(df, results):
    results['school_name'] = df.filter(df.school_name.isNotNull()).groupby("school_name").agg(
        F.count("*").alias("person_num"))
    results['major'] = df.filter(df.major.isNotNull()).groupby("major").agg(F.count("*").alias("person_num"))


def statistic_main(profile_path=None, education_path=None, work_path=None, output_path=None, suggest=False):
    """
    简历和职位预处理
    :param profile_path: 简历基本信息文件路径， parquet格式
    :param education_path: 简历教育经历文件路径， parquet格式
    :param work_path: 简历工作经历文件路径， parquet格式
    :param output_path: 数据库路径，parquet 格式
    :param suggest: 是否输出成联想词
    :return: 
    """

    # spark 环境初始化
    conf = SparkConf().set("spark.ui.port", "44040")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # 加载简历基本信息，教育经历，工作经历
    results = dict()
    # statistic_profile(sqlContext.read.parquet(profile_path), results)
    # statistic_education(sqlContext.read.parquet(education_path), results)
    statistic_work(sqlContext.read.parquet(work_path), results)
    write2file(results, output_path, suggest)


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历和职位数据预处理"
    parser.add_argument('-p', action='store', dest='profile_path', default=PROFILE_PATH,
                        help='简历基本信息文件路径，parquet格式')
    parser.add_argument('-e', action='store', dest='education_path', default=EDUCATION_PATH,
                        help='简历教育经历文件路径，parquet格式')
    parser.add_argument('-w', action='store', dest='work_path', default=WORK_PATH,
                        help='简历工作经历文件路径，parquet格式')
    parser.add_argument('-s', action='store', dest='suggest', default=False, type=bool,
                        help='是否输出成联想词结果')
    parser.add_argument('-o', action='store', dest='output_path', default=OUTPUT_PATH,
                        help='预处理后的数据输出路径')

    # 运行参数
    args = vars(parser.parse_args())
    if not all(args.values()):
        parser.print_help()

    # 简历和职位预处理主函数
    statistic_main(**args)
