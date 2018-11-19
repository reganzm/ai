# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""
import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql.functions import PandasUDFType, pandas_udf
from pyspark.sql.types import *

from bi.core.common import add_median_salary, add_rank
from bi.core.filter import filter_min
from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_NUM, MIN_SALARY


def statistic_position(df, mysql_url):
    """
    职位相关维度分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    # 数据过滤
    df = df.filter(df.position_name.isNotNull())
    df.persist()
    # 分析结果表
    result_tables = dict()
    result_tables["position__rank"] = statistic_position_rank(df)
    result_tables["position__address"] = statistic_position_address(df)
    result_tables["position__industry__rank"] = statistic_position_industry_rank(df)
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)
    df.unpersist()


@filter_min
def statistic_position_rank(df):
    """
    职位排行
    :param df: 
    :return: 
    """
    df = df.filter((df.avg_salary > MIN_SALARY))
    df = add_median_salary(df, ("position_name",))
    # 计算当前工作的平均薪资，毕业到当前工作的年限
    mdf = df.groupby("position_name").agg(F.count("*").alias("person_num"), F.avg(df.avg_salary).alias("avg_salary"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    mdf = add_rank(mdf)
    return mdf


def statistic_position_address(df):
    """职位对应地域分布"""
    df = df.filter(df.address.isNotNull())
    df = df.groupby("position_name", "address").agg(F.count("*").alias("person_num"))
    df = df.filter(df.person_num > MIN_NUM)
    return df


position_rank_schema = StructType([
    StructField("position_name", StringType()),
    StructField("person_num", IntegerType()),
    StructField("avg_salary", FloatType()),
    StructField("rank", IntegerType()),
])


@pandas_udf(position_rank_schema, PandasUDFType.GROUPED_MAP)
def position_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="avg_salary", ascending=False)
    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf.loc[:, ["position_name", "person_num", "avg_salary", "rank"]]


position_industry_rank_schema = StructType([
    StructField("position_name", StringType()),
    StructField("industry", StringType()),
    StructField("rank", IntegerType()),
    StructField("person_num", IntegerType()),
    StructField("avg_salary", FloatType()),
])


@pandas_udf(position_industry_rank_schema, PandasUDFType.GROUPED_MAP)
def position_industry_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="person_num", ascending=False)
    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf.loc[:, ["position_name", "industry", "rank", "person_num", "avg_salary"]]


def statistic_position_industry_rank(df):
    """职位和行业对应人数排名"""
    groups = ("position_name", "industry")
    df = df.filter(df.industry.isNotNull()).filter((df.avg_salary > MIN_SALARY))
    df = add_median_salary(df, groups)
    pi_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                    F.avg(df.avg_salary).alias("avg_salary"))
    pi_df = pi_df.filter(pi_df.person_num > MIN_NUM)
    pi_df = pi_df.groupby("position_name").apply(position_industry_rank)
    return pi_df
