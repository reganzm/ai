# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

from argparse import ArgumentParser
from os.path import join

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F

from bi.settings import JEDUCATION_PATH, JPROFILE_PATH, JWORK_PATH, OUTPUT_PATH


def output_file(results, output_path):
    for filename, df in results.items():
        df = df.filter(df.person_num > 2).filter(F.length(df[filename]) > 1) \
            .select(filename, df.person_num.cast("string")).sort(filename)
        path = join(output_path, filename + ".txt")
        print("当前写入文件：{}".format(path))
        output = open(path, 'w')
        output.close()

        def write2local(df):
            output = open(path, 'w')
            for row in df:
                output.write("\t".join(row.asDict().values()) + "\n")
            output.close()

        df.coalesce(10).foreachPartition(write2local)

        # for row in df.sort(filename).collect():
        #     output.write("\t".join(row.asDict().values()) + "\n")
        output.close()


def statistic_profile(df, results):
    """统计各个搜索字段的值与权重"""


def statistic_work(df, results):
    # df = df.withColumn("company_name", F.udf(normaliztion_str)(df.company_name))
    df = df.withColumn("industry", df.industry_category)
    # df = df.withColumn("industry", F.udf(normaliztion_str)(df.industry_category))
    df = df.withColumn("position_name", df.position_title)
    # df = df.withColumn("position_name", F.udf(normaliztion_str)(df.position_title))
    results['company_name'] = df.filter(df.company_name.isNotNull()).groupby("company_name").agg(
        F.count("*").alias("person_num"))
    results['industry'] = df.filter(df.industry.isNotNull()).groupby("industry").agg(
        F.count("*").alias("person_num"))
    results['position_name'] = df.filter(df.position_name.isNotNull()).groupby("position_name").agg(
        F.count("*").alias("person_num"))


def statistic_education(df, results):
    df = df.withColumn("school_name", df.school)
    # df = df.withColumn("school_name", F.udf(normaliztion_str)(df.school))
    df = df.withColumn("major", df.major)
    # df = df.withColumn("major", F.udf(normaliztion_str)(df.major))
    results['school_name'] = df.filter(df.school_name.isNotNull()).groupby("school_name").agg(
        F.count("*").alias("person_num"))
    results['major'] = df.filter(df.major.isNotNull()).groupby("major").agg(F.count("*").alias("person_num"))


def statistic_main(profile_path=None, education_path=None, work_path=None, output_path=None):
    """
    简历和职位预处理
    :param profile_path: 简历基本信息文件路径， parquet格式
    :param education_path: 简历教育经历文件路径， parquet格式
    :param work_path: 简历工作经历文件路径， parquet格式
    :param output_path: 数据库路径，parquet 格式
    :return: 
    """

    # spark 环境初始化
    conf = SparkConf().set("spark.ui.port", "44040")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # 加载简历基本信息，教育经历，工作经历
    results = dict()
    # statistic_profile(sqlContext.read.json(profile_path), results)
    statistic_education(sqlContext.read.json(education_path), results)
    # statistic_work(sqlContext.read.json(work_path), results)
    output_file(results, output_path)


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历和职位数据预处理"
    parser.add_argument('-p', action='store', dest='profile_path', default=JPROFILE_PATH,
                        help='简历基本信息文件路径，parquet格式')
    parser.add_argument('-e', action='store', dest='education_path', default=JEDUCATION_PATH,
                        help='简历教育经历文件路径，parquet格式')
    parser.add_argument('-w', action='store', dest='work_path', default=JWORK_PATH,
                        help='简历工作经历文件路径，parquet格式')
    parser.add_argument('-o', action='store', dest='output_path', default=OUTPUT_PATH,
                        help='预处理后的数据输出路径')

    # 运行参数
    args = vars(parser.parse_args())
    if not all(args.values()):
        parser.print_help()

    # 简历和职位预处理主函数
    statistic_main(**args)
