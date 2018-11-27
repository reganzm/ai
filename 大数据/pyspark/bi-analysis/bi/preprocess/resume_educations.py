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
bi/preprocess/resume_educations.py  
--input_path hdfs://192.168.0.214:8020/user/bigdata/BI/resume_flatten_v1/resume_educations.json 
--output_path hdfs://192.168.0.214:8020/user/bigdata/BI/resume_flatten_v1/resume_educations.parquet
"""

import re
from argparse import ArgumentParser

from pinbot_clean.marker.school_area import mark_school_area
from pinbot_clean.normalization import normalization_degree, normalization_major, \
    normalization_school_name, normalized_major_tuple
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F
from pyspark.sql.types import *

from bi.settings import JEDUCATION_PATH

OUTPUT_PATH = JEDUCATION_PATH.replace("json", "parquet")
format_date = re.compile("[./]")


def preprocess_educations(df, output_path):
    """
    简历教育经历信息预处理
    :param df: 教育经历数据，DataFrame数据类型
    :param output_path: 输出文件路径
    :return: 
    """

    # 预处理后输出字段
    output_columns = ["resume_id", "school_name", "school_area", "major", "category", "subcategory", "edu_start_date",
                      "edu_end_date", "edu_start_year", "edu_end_year", "degree", "edu_index"]

    # 归一化处理学校名，学历
    df = df.withColumn("school_name", F.udf(normalization_school_name)(df.school))
    df = df.withColumn("school_area", F.udf(mark_school_area)(df.school_name))
    df = df.withColumn("major", F.udf(normalization_major)(df.major))
    df = df.withColumn("degree", F.udf(normalization_degree)(df.degree))
    # df = df.withColumn("major_category", F.udf(get_major_level2)(df.major, df.degree))
    df = df.withColumn("subjects",
                       F.udf(normalized_major_tuple, ArrayType(ArrayType(StringType())))(df.major, df.degree))
    df = df.withColumn("subjects", F.explode("subjects")) \
        .withColumn("category", F.col("subjects")[0]) \
        .withColumn("subcategory", F.col("subjects")[1]) \
        .withColumn("major", F.col("subjects")[2])
    # 标准化日期格式
    df = df.withColumn("start_time", F.udf(lambda x: format_date.sub("-", x))(df.start_time))
    df = df.withColumn("end_time", F.udf(lambda x: format_date.sub("-", x))(df.end_time))
    df = df.withColumn("edu_start_date", F.date_format(df.start_time, "yyy-MM"))
    df = df.withColumn("edu_end_date", F.date_format(df.end_time, "yyy-MM"))
    df = df.withColumn("edu_end_date", F.when(df.edu_end_date.isNotNull(), df.edu_end_date)
                       .otherwise(F.date_format(F.add_months(df.edu_start_date, 48), "yyy-MM")))
    df = df.withColumn("edu_start_year", F.year(df.start_time))
    df = df.withColumn("edu_end_year", F.year(df.end_time))
    df = df.withColumn("edu_index", df.index)

    # 过滤条件
    df = df.dropna(how="all", subset=["school_name", "major", "degree"])

    # 将简历基本信息预处理后的结果保存至指定文件
    df.select(output_columns).write.mode('overwrite').save(output_path)


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历基本信息预处理"
    parser.add_argument('-i', '--input_path', action='store', dest='input_path', default=JEDUCATION_PATH,
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
    preprocess_educations(profile_df, args.output_path)
