# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 

spark-submit 
--master yarn-client 
--num-executors 6 
--executor-cores 1 
--executor-memory 5G 
--driver-memory 5G 
bi/preprocess/resume_works.py  
--input_path hdfs://192.168.0.214:8020/user/bigdata/BI/resume_flatten_v1/resume_works.json 
--output_path hdfs://192.168.0.214:8020/user/bigdata/BI/resume_flatten_v1/resume_works.parquet
"""

import re
from argparse import ArgumentParser

from pinbot_clean.normalization import get_position_level1, normalization_company_name, normalization_industry, \
    normalization_position_name
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F
from pyspark.sql.types import FloatType

from bi.settings import JWORK_PATH

OUTPUT_PATH = JWORK_PATH.replace("json", "parquet")
format_date = re.compile("[./]")


def preprocess_works(df, output_path):
    """
    简历工作经历信息预处理
    :param df: 工作经历数据，DataFrame数据类型
    :param output_path: 输出文件路径
    :return: 
    """

    # 预处理后输出字段
    output_columns = ["resume_id",
                      "company_name", "industry", "position_name", "position_title", "position_category",
                      "work_start_date", "work_end_date", "work_start_year", "work_end_year",
                      "work_index", "salary_min", "salary_max"]

    # 归一化处理公司名称，公司行业，职位名称
    df = df.withColumn("company_name", F.lower(F.trim(F.udf(normalization_company_name)(df.company_name))))
    df = df.withColumn("industry", F.lower(F.trim(F.udf(normalization_industry)(df.industry_category))))
    df = df.withColumn("position_name", F.lower(F.trim(F.udf(normalization_position_name)(df.position_title))))
    df = df.withColumn("position_category", F.lower(F.trim(F.udf(get_position_level1)(df.position_name))))
    df = df.withColumn("start_time", F.udf(lambda x: format_date.sub("-", x))(df.start_time))
    df = df.withColumn("end_time", F.udf(lambda x: format_date.sub("-", x))(df.end_time))
    df = df.withColumn("work_start_date", F.date_format(df.start_time, "yyy-MM"))
    df = df.withColumn("work_end_date", F.date_format(df.end_time, "yyy-MM"))
    df = df.withColumn("work_start_year", F.year(df.start_time))
    df = df.withColumn("work_end_year", F.year(df.end_time))
    df = df.withColumn("work_index", df.index)

    # 过滤公司、行业、职位全为空的字段
    df = df.dropna(how="all", subset=["company_name", "industry", "position_name"])

    # 将简历基本信息预处理后的结果保存至指定文件
    df.select(output_columns).write.mode('overwrite').save(output_path)


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历基本信息预处理"
    parser.add_argument('-i', '--input_path', action='store', dest='input_path', default=JWORK_PATH,
                        help='简历基本信息文件路径，json格式')
    parser.add_argument('-o', '--output_path', action='store', dest='output_path', default=OUTPUT_PATH,
                        help='简历基本信息处理后的文件保存路径， parquet格式')

    # 运行参数
    args = parser.parse_args()
    if args.input_path is None:
        parser.print_help()

    # spark 环境初始化
    conf = SparkConf().set("spark.ui.port", "44040")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # 加载数据
    profile_df = sqlContext.read.json(args.input_path)
    preprocess_works(profile_df, args.output_path)
