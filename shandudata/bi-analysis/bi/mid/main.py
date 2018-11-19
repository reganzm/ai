# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 21/07/2018 09:40
:File    : main.py
"""

from argparse import ArgumentParser

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

from bi.settings import EDUCATION_PATH, WORK_PATH
from .education2connect import education2connect
from .work2connect import work2connect


def output_file(df, output_path):
    path = output_path + ".json"
    print("当前写入文件：{}".format(path))
    output = open(path, 'w')
    output.close()

    def write2local(rdd):
        output = open(path, 'w')
        for line in rdd:
            output.write(line + "\n")
        output.close()

    df.toJSON().coalesce(10).foreachPartition(write2local)


def modify_path(path):
    words = path.split(".")
    words.insert(-1, "mid")
    return ".".join(words)


def statistic_main(education_path=None, work_path=None):
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

    # 加载简历教育经历，工作经历
    education_df = sqlContext.read.parquet(education_path)
    work_df = sqlContext.read.parquet(work_path)
    education2connect(education_df).write.mode('overwrite').save(modify_path(education_path))
    work2connect(work_df).write.mode('overwrite').save(modify_path(work_path))


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "工作经历和教育经历的连接分析， 连接两份工作经历和教育经历。"
    parser.add_argument('-e', action='store', dest='education_path', default=EDUCATION_PATH,
                        help='简历教育经历文件路径，parquet格式')
    parser.add_argument('-w', action='store', dest='work_path', default=WORK_PATH,
                        help='简历工作经历文件路径，parquet格式')

    # 运行参数
    args = vars(parser.parse_args())
    if not all(args.values()):
        parser.print_help()

    # 简历和职位预处理主函数
    statistic_main(**args)
