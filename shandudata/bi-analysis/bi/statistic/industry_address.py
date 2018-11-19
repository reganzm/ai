# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

from pyspark.sql import functions as F
from pyspark.sql.functions import PandasUDFType, pandas_udf
from pyspark.sql.types import *

from bi.core.common import add_median_salary, add_rank
from bi.core.filter import filter_min, filter_cube_num
from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_SALARY, NA, MIN_NUM


def statistic_industry_address(df, mysql_url):
    """
    行业相关维度分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    # 数据过滤
    df = df.filter(df.industry.isNotNull()).filter(df.address.isNotNull())
    df.persist()
    # 分析结果表
    result_tables = dict()
    result_tables["industry__address__compare"] = statistic_industry_address_compare(df)
    result_tables["industry__address__flow"] = statistic_industry_address_flow(df)
    result_tables["industry__address__salary"] = statistic_industry_address_salary_range(df)
    result_tables["industry__address__age"] = statistic_industry_address_age_range(df)
    result_tables["industry__address__gender"] = statistic_industry_address_gender(df)
    # result_tables["industry__address__work_year"] = statistic_industry_address_work_year_range(df)
    result_tables["industry__address__degree"] = statistic_industry_address_degree(df)
    result_tables["industry__address__salary_work_year"] = statistic_industry_address_salary_work_year(df)
    result_tables["industry__address__rank"] = statistic_industry_address_rank(df)
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)
    df.unpersist()


@filter_min
def statistic_industry_address_rank(df):
    """
    行业、地区排行
    :param df:
    :return:
    """
    df = df.filter((df.avg_salary > MIN_SALARY))
    groups = ("industry", "address")
    df = add_median_salary(df, groups)
    ia_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                    F.avg("avg_salary").alias("avg_salary"))
    ia_df = ia_df.filter(ia_df.person_num > MIN_NUM)
    i_df = ia_df.groupby("industry").agg(F.sum("person_num").alias("person_num"),
                                         F.avg("avg_salary").alias("avg_salary"))
    i_df = i_df.withColumn("address", F.lit(NA))
    ia_df = ia_df.unionByName(i_df)
    return add_rank(ia_df, "address")


@filter_min
def statistic_industry_address_compare(df):
    """
    行业与地区对比
    :param df: 
    :return: 
    """
    df = df.filter(df.avg_salary.isNotNull())
    groups = ("industry", "address")
    df = add_median_salary(df, groups)
    df = filter_cube_num(df, "industry", "address")
    mdf = df.cube("industry", "address").agg(F.count("*").alias("person_num"), F.avg("avg_salary").alias("avg_salary"))
    return mdf.fillna({"industry": NA, "address": NA})


def statistic_industry_address_flow(df):
    """
    行业对应地区人才流动
    :param df: 
    :return: 
    """
    df = df.filter(df.expect_area.isNotNull())
    mdf = df.select("industry", "address",
                    F.explode(F.split(df.expect_area, ",")).alias("expect_area"))
    mdf = mdf.groupby("industry", "address", "expect_area").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    return mdf


def statistic_industry_address_salary_range(df):
    """
    行业对应薪资区间分布
    :param df: 
    :return: 
    """
    df = df.filter(df.salary_range.isNotNull())
    mdf = df.groupby("industry", "address", "salary_range").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("industry", "salary_range").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


@filter_min
def statistic_industry_address_age_range(df):
    """
    行业对应年龄分布
    :param df: 
    :return: 
    """
    df = df.filter(df.age_range.isNotNull()).filter((df.avg_salary > MIN_SALARY))
    groups = ("industry", "address", "age_range")
    df = add_median_salary(df, groups)
    mdf = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                  F.avg("avg_salary").alias("avg_salary"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("industry", "age_range").agg(F.sum("person_num").alias("person_num"),
                                                   F.avg("avg_salary").alias("avg_salary"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_industry_address_gender(df):
    """
    行业对应性别分布
    :param df: 
    :return: 
    """
    df = df.filter(df.gender.isNotNull())
    mdf = df.groupby("industry", "address", "gender").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("industry", "gender").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_industry_address_work_year_range(df):
    """
    行业对应的工作年限分布
    :param df: 
    :return: 
    """
    df = df.filter(df.work_year_range.isNotNull()).filter(df.avg_salary > MIN_SALARY)
    groups = ("industry", "address", "work_year_range")
    df = add_median_salary(df, groups)
    mdf = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                  F.avg("avg_salary").alias("avg_salary"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("industry", "work_year_range").agg(F.sum("person_num").alias("person_num"),
                                                         F.avg("avg_salary").alias("avg_salary"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


@filter_min
def statistic_industry_address_degree(df):
    """
    行业对应的学历分布
    :param df: 
    :return: 
    """
    df = df.filter(df.degree.isNotNull()).filter(df.avg_salary > MIN_SALARY)
    groups = ("industry", "address", "degree")
    df = add_median_salary(df, groups)
    mdf = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                  F.avg("avg_salary").alias("avg_salary"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("industry", "degree").agg(F.sum("person_num").alias("person_num"),
                                                F.avg("avg_salary").alias("avg_salary"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_industry_address_salary_work_year(df):
    """
    行业+地点+年限+薪资对应的人数分布
    :param df:
    :return:
    """
    df = df.filter(df.work_year_range.isNotNull()).filter(df.salary_range.isNotNull())
    mdf = df.groupby("industry", "address", "work_year_range", "salary_range").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("industry", "work_year_range", "salary_range").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


industry_address_rank_schema = StructType([
    StructField("industry", StringType()),
    StructField("address", StringType()),
    StructField("person_num", IntegerType()),
    StructField("avg_salary", FloatType()),
    StructField("rank", IntegerType()),
])


@pandas_udf(industry_address_rank_schema, PandasUDFType.GROUPED_MAP)
def industry_address_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="avg_salary", ascending=False)
    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf[["industry", "address", "person_num", "avg_salary", "rank"]]
