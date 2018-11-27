# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-24
@Content: 简历基本信息预处理

spark-submit 
--master yarn-client 
--num-executors 6 
--executor-cores 1 
--executor-memory 5G 
--driver-memory 5G 
bi/preprocess/resume_profile.py  
--input_path hdfs://192.168.0.214:8020/user/bigdata/BI/resume_flatten_v1/resume_profile.json 
--output_path hdfs://192.168.0.214:8020/user/bigdata/BI/resume_flatten_v1/resume_profile.parquet
"""
import datetime
from argparse import ArgumentParser

from pinbot_clean.normalization import normalization_area_name, normalization_position_name, normalized_area_tuple
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F
from pyspark.sql.types import *

from bi.settings import JPROFILE_PATH, LATEST_YEAR, ACTIVE_YEAR
from bi.utils import cal_avg_salary

OUTPUT_PATH = JPROFILE_PATH.replace("json", "parquet")


def format_str(value):
    value = value.strip()
    if not value:
        value = None
    return value


def format_gender(gender):
    gender = format_str(gender)
    if gender in ["男", "先生", "male", "男士"]:
        return "男"
    elif gender in ["女", "女生", "女士", "female"]:
        return "女"
    else:
        return None


def preprocess_resume_profile(df, output_path):
    """
    简历基本信息预处理
    :param df: 简历基本信息数据，DataFrame数据类型
    :param output_path: 输出文件路径
    :return: 
    """
    # 预处理后输出字段
    output_columns = ["resume_id", "age", "address", "gender", "expect_career", "expect_area", "avg_salary",
                      "update_date", "province", "district", "education_len", "work_len"]

    # 计算平均薪资，如果期望薪资没有值则用最近薪资
    df = df.withColumn("avg_salary", F.udf(cal_avg_salary, FloatType())(df.expect_salary_min, df.expect_salary_max,
                                                                        df.latest_salary_min, df.latest_salary_max))
    # 将更新时间转换为年
    df = df.withColumn("update_time", F.date_format(df.update_time, "yyy-MM-dd"))
    df = df.withColumn("update_date", F.date_format(df.update_time, "yyy-MM"))
    df = df.withColumn("update_year", F.year(df.update_time))
    # 标准化现居地
    df = df.withColumn("gender", F.udf(format_gender)(df.gender))
    # df = df.withColumn("address", F.lower(F.trim(F.udf(normalization_area_name)(df.address))))
    df = df.withColumn("areas", F.udf(normalized_area_tuple, ArrayType(ArrayType(StringType())))(df.address))
    df = df.withColumn("areas", F.explode("areas")) \
        .withColumn("province", F.col("areas")[0]) \
        .withColumn("city", F.col("areas")[1]) \
        .withColumn("district", F.col("areas")[2]) \
        .withColumn("address", F.col("city"))
    # 标准化期望工作地
    df = df.withColumn("expect_area", F.udf(normalization_area_name)(df.expect_area))
    # 标准化期望职位
    df = df.withColumn("expect_career", F.lower(F.trim(F.udf(normalization_position_name)(df.expect_career))))
    # 最近（3年）更新简历（活跃简历）
    df = df.filter(df.update_year >= datetime.datetime.now().year - ACTIVE_YEAR)
    # 将简历基本信息预处理后的结果保存至指定文件
    df.select(output_columns).write.parquet(output_path, mode='overwrite')


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历基本信息预处理"
    parser.add_argument('-i', '--input_path', action='store', dest='input_path', default=JPROFILE_PATH,
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
    preprocess_resume_profile(profile_df, args.output_path)
