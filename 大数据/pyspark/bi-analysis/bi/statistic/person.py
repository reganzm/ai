# -*- coding: utf-8 -*-
"""
@Time    : 2018/6/15
@Author   : huanggangyu
"""

from pyspark.sql import functions as F

from bi.core.common import add_median_salary, filter_cube_num
from bi.core.filter import filter_age, filter_min
from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_SALARY, NA


def statistic_person(df, mysql_url):
    """
    个人维度分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    # 数据过滤
    df = df.filter(df.avg_salary > MIN_SALARY)
    df.persist()
    # 分析结果表
    result_tables = dict()
    result_tables["person__rank"] = statistic_person_rank(df)
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)
    df.unpersist()


def statistic_person_rank(df):
    """
    人员排行
    :param df: 
    :return: 
    """
    df = df.filter(df.address.isNotNull())
    df = df.filter(df.gender.isNotNull())
    groups = ("address", "age", "gender")
    df = filter_cube_num(df, *groups)
    df = add_median_salary(df, groups)
    df = filter_age(df).withColumn("age", F.udf(str)(df.age))
    aag_df = df.cube(*groups).agg(F.count("*").alias("person_num"),
                                  F.avg(df.avg_salary).alias("avg_salary"))
    aag_df = aag_df.filter(aag_df.age.isNotNull())
    aag_df = aag_df.fillna({"address": NA, "gender": NA})
    return aag_df
