# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 26/08/2018 23:29
:File    : graduate.py
"""

from argparse import ArgumentParser

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

from bi.settings import MYSQL_URL, RESUME_PATH
from .graduate_all_work import graduate_all_work
from .graduate_first_work import graduate_first_work


def statistic_graduate(input_path=None, mysql_url=None):
    # spark 环境初始化
    conf = SparkConf().set("spark.ui.port", "44040")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # 加载简历信息
    resume_df = sqlContext.read.parquet(input_path)

    # 只分析国内学校
    education_df = resume_df.filter(resume_df.school_area == "中国")

    # 获取最近一份教育经历
    resume_df = education_df.filter(education_df.edu_index == 1)

    # 获取最近一份教育经历毕业后对应的第一份工作经历
    resume_first_work_df = resume_df.filter(resume_df.work_index == resume_df.work_len)

    graduate_all_work(resume_df, mysql_url)
    graduate_first_work(resume_first_work_df, mysql_url)


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历分析"
    parser.add_argument('-i', action='store', dest='input_path', default=RESUME_PATH,
                        help='简历信息文件路径，parquet格式')
    parser.add_argument('-o', action='store', dest='mysql_url', default=MYSQL_URL,
                        help='预处理后的数据输出路径')

    # 运行参数
    args = vars(parser.parse_args())
    if not all(args.values()):
        parser.print_help()

    # 简历和职位预处理主函数
    statistic_graduate(**args)
