# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 26/08/2018 22:43
:File    : combine_resume.py
"""

from argparse import ArgumentParser

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F
from pyspark.sql.types import *

from bi.settings import EDUCATION_PATH, PROFILE_PATH, RESUME_PATH, WORK_PATH
from bi.utils.get_years import get_work_year


def combine_resume(profile_path, education_path, work_path, output_path):
    # spark 环境初始化
    conf = SparkConf().set("spark.ui.port", "44040")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # 加载简历基本信息，教育经历，工作经历
    profile_df = sqlContext.read.parquet(profile_path)
    education_df = sqlContext.read.parquet(education_path)
    work_df = sqlContext.read.parquet(work_path)
    df = profile_df.join(education_df, "resume_id").join(work_df, "resume_id")
    # 计算单次工作的时长
    df = df.withColumn("work_end_date",
                       F.when(F.lower(F.trim(df.work_end_date)).isin("至今", "今", "present"), df.update_date)
                       .otherwise(df.work_end_date))
    df = df.withColumn("work_duration_month",
                       F.months_between(df.work_end_date, df.work_start_date))
    df = df.withColumn("work_duration_year",
                       F.udf(lambda x: x / 12 if x else -1, FloatType())(df.work_duration_month))
    # 计算毕业到现在的工作时长
    df = df.withColumn("work_month_min", F.months_between(df.work_start_date, df.edu_end_date))
    df = df.withColumn("work_month_max", F.months_between(df.work_end_date, df.edu_end_date))
    df = df.withColumn("work_month_duration", F.months_between(df.work_end_date, df.work_start_date))
    # 将工作月份转换成年数
    df = df.withColumn("work_year_min", F.udf(get_work_year, IntegerType())(df.work_month_min))
    df = df.withColumn("work_year_max", F.udf(get_work_year, IntegerType())(df.work_month_max))
    df.write.mode('overwrite').save(output_path)


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历信息组合"
    parser.add_argument('-p', action='store', dest='profile_path', default=PROFILE_PATH,
                        help='简历基本信息文件路径，parquet格式')
    parser.add_argument('-e', action='store', dest='education_path', default=EDUCATION_PATH,
                        help='简历教育经历文件路径，parquet格式')
    parser.add_argument('-w', action='store', dest='work_path', default=WORK_PATH,
                        help='简历工作经历文件路径，parquet格式')
    parser.add_argument('-o', action='store', dest='output_path', default=RESUME_PATH,
                        help='预处理后的数据输出路径')

    # 运行参数
    args = vars(parser.parse_args())
    if not all(args.values()):
        parser.print_help()

    # 简历和职位预处理主函数
    combine_resume(**args)
