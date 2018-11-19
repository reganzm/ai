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

from bi.core.common import add_median_salary
from bi.core.filter import filter_min, filter_cube_num
from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_SALARY, NA, MIN_NUM


def statistic_position_address(df, mysql_url):
    """
    职位相关维度分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    # 数据过滤
    df = df.filter(df.position_name.isNotNull()).filter(df.address.isNotNull())
    df.persist()
    # 分析结果表
    result_tables = dict()
    result_tables["position__address__compare"] = statistic_position_address_compare(df)
    result_tables["position__address__flow"] = statistic_position_address_flow(df)
    result_tables["position__address__salary_range"] = statistic_position_address_salary_range(df)
    result_tables["position__address__age_range"] = statistic_position_address_age_range(df)
    result_tables["position__address__gender"] = statistic_position_address_gender(df)
    result_tables["position__address__work_year_range"] = statistic_position_address_work_year_range(df)
    result_tables["position__address__degree"] = statistic_position_address_degree(df)
    result_tables["position__address__duration"] = statistic_position_address_duration(df)
    result_tables["position__address__industry"] = statistic_position_address_industry(df)
    result_tables["position__address__salary_work_year"] = statistic_position_address_salary_work_year(df)
    result_tables["position__address__prev_position"] = statistic_position_address_prev_position(df)
    result_tables["position__address__next_position"] = statistic_position_address_next_position(df)
    result_tables["position__address__change"] = statistic_position_address_change(df)
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)
    df.unpersist()


@filter_min
def statistic_position_address_compare(df):
    """
    职位与地区对比
    :param df: 
    :return: 
    """
    df = df.filter(df.avg_salary > MIN_SALARY)
    groups = ("position_name", "address")
    df = filter_cube_num(df, groups)
    df = add_median_salary(df, groups)
    mdf = df.cube(*groups).agg(F.count("*").alias("person_num"),
                               F.avg("avg_salary").alias("avg_salary"))
    return mdf.fillna({"position_name": NA, "address": NA})


def statistic_position_address_flow(df):
    """
    职位+地点对应地区人才流动
    :param df: 
    :return: 
    """
    df = df.filter(df.expect_area.isNotNull())
    mdf = df.select("position_name", "address",
                    F.explode(F.split(df.expect_area, ",")).alias("expect_area"))
    mdf = mdf.groupby("position_name", "address", "expect_area").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    return mdf


def statistic_position_address_salary_range(df):
    """
    职位+地点对应薪资区间分布
    :param df: 
    :return: 
    """
    df = df.filter(df.salary_range.isNotNull())
    mdf = df.groupby("position_name", "address", "salary_range").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("position_name", "salary_range").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_position_address_age_range(df):
    """
    职位+地点对应年龄分布
    :param df: 
    :return: 
    """
    df = df.filter(df.age_range.isNotNull()).filter(df.avg_salary > MIN_SALARY)
    mdf = df.groupby("position_name", "address", "age_range").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("position_name", "age_range").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


@filter_min
def statistic_position_address_gender(df):
    """
    职位+地点对应性别分布
    :param df: 
    :return: 
    """
    df = df.filter(df.gender.isNotNull()).filter(df.avg_salary > MIN_SALARY)
    groups = ("position_name", "address", "gender")
    df = add_median_salary(df, groups)
    mdf = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                  F.avg("avg_salary").alias("avg_salary"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("position_name", "gender").agg(F.sum("person_num").alias("person_num"),
                                                     F.avg("avg_salary").alias("avg_salary"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


@filter_min
def statistic_position_address_work_year_range(df):
    """
    职位+地点对应的工作年限分布
    :param df: 
    :return: 
    """
    df = df.filter(df.work_year_range.isNotNull()).filter((df.avg_salary > MIN_SALARY))
    groups = ("position_name", "address", "work_year_range")
    df = add_median_salary(df, groups)
    mdf = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                  F.avg("avg_salary").alias("avg_salary"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("position_name", "work_year_range").agg(F.sum("person_num").alias("person_num"),
                                                              F.avg("avg_salary").alias("avg_salary"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


@filter_min
def statistic_position_address_degree(df):
    """
    职位+地点对应的学历分布
    :param df: 
    :return: 
    """
    df = df.filter(df.degree.isNotNull()).filter((df.avg_salary > MIN_SALARY))
    groups = ("position_name", "address", "degree")
    df = add_median_salary(df, groups)
    mdf = df.groupby("position_name", "address", "degree").agg(F.count("*").alias("person_num"),
                                                               F.avg("avg_salary").alias("avg_salary"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("position_name", "degree").agg(F.sum("person_num").alias("person_num"),
                                                     F.avg("avg_salary").alias("avg_salary"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_position_address_duration(df):
    """
    职位+地点对应单次在职时长
    :param df:
    :return:
    """
    df = df.filter(df.work_duration_month.isNotNull()).filter(df.work_duration_month > 0) \
        .filter(df.work_duration_month < 240)
    pa_df = df.groupby("position_name", "address").agg(F.count("*").alias("person_num"),
                                                       F.avg(df.work_duration_month).alias("avg_duration"))
    pa_df = pa_df.filter(pa_df.person_num > MIN_NUM)
    pa_df = pa_df.groupby("address").apply(duration_rank)
    p_df = pa_df.groupby("position_name").agg(F.sum("person_num").alias("person_num"),
                                              F.avg(pa_df.avg_duration).alias("avg_duration"))
    p_df = p_df.withColumn("address", F.lit(NA))
    p_df = p_df.groupby().apply(duration_rank)
    return pa_df.unionByName(p_df)


def statistic_position_address_industry(df):
    """
    职位+地点对应行业分布
    :param df:
    :return:
    """
    df = df.filter(df.industry.isNotNull())
    # 限制address分析
    pai_df = df.groupby("position_name", "address", "industry").agg(F.count("*").alias("person_num"))
    pai_df = pai_df.filter(pai_df.person_num > MIN_NUM)
    pai_df = pai_df.groupby("position_name", "address").apply(industry_rank)
    # 不限address分析
    pi_df = pai_df.groupby("position_name", "industry").agg(F.sum("person_num").alias("person_num"))
    pi_df = pi_df.withColumn("address", F.lit(NA))
    # 每个职位各行业人数占比排序，升序
    pi_df = pi_df.groupby("position_name").apply(industry_rank)
    # 比其他行业比例高，即比例比当前职位高的职位数量
    return pai_df.unionByName(pi_df)


def statistic_position_address_salary_work_year(df):
    """
    职位+地点+年限+薪资对应的人数分布
    :param df:
    :return:
    """
    df = df.filter(df.work_year_range.isNotNull()).filter(df.salary_range.isNotNull())
    mdf = df.groupby("position_name", "address", "work_year_range", "salary_range").agg(
        F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("position_name", "work_year_range", "salary_range").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_position_address_change(df):
    """
    职位延续性分析
    :param df:
    :return:
    """
    df = df.select("position_name", "address", "resume_id", "work_index")
    # 筛选下份工作未改变职位的数据
    mdf = df.groupby("resume_id").apply(next_same_position)
    # 职位相同人数
    pa_df = mdf.groupby("position_name", "address").agg(F.count("*").alias("person_num"))
    pa_df = pa_df.filter(pa_df.person_num > MIN_NUM)
    # 所有职位人数
    pa_df = pa_df.groupby("address").apply(change_rank)
    # 职位相同人数
    p_df = pa_df.groupby("position_name").agg(F.sum("person_num").alias("person_num"))
    p_df = p_df.withColumn("address", F.lit(NA))
    p_df = p_df.groupby().apply(change_rank)
    return pa_df.unionByName(p_df)


def statistic_position_address_prev_position(df):
    """
    当前职位的上一份职位分布
    :param df:
    :return:
    """
    df = df.select("position_name", "address", "resume_id", "work_index")
    mdf = df.groupby("resume_id").apply(prev_position)
    mdf = mdf.groupby("position_name", "prev_position", "address").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("position_name", "prev_position").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_position_address_next_position(df):
    """
    当前职位的下一份职位分布
    :param df:
    :return:
    """
    df = df.select("position_name", "address", "resume_id", "work_index")
    mdf = df.groupby("resume_id").apply(next_position)
    mdf = mdf.groupby("position_name", "next_position", "address").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("position_name", "next_position").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("address", F.lit(NA))
    return mdf.unionByName(sdf)


prev_position_schema = StructType([
    StructField("position_name", StringType()),
    StructField("prev_position", StringType()),
    StructField("address", StringType()),
])


@pandas_udf(prev_position_schema, PandasUDFType.GROUPED_MAP)
def prev_position(pdf):
    position_list = []
    prev_position_list = []
    address_list = []
    rows, columns = pdf.shape
    if rows > 1:
        pdf = pdf.sort_values(by="work_index", ascending=False)
        for i in range(1, rows):
            if pdf.iloc[i, 0] == pdf.iloc[i - 1, 0]:
                continue
            position_list.append(pdf.iloc[i, 0])
            prev_position_list.append(pdf.iloc[i - 1, 0])
            address_list.append(pdf.iloc[i, 1])
    data = {
        "position_name": position_list,
        "prev_position": prev_position_list,
        "address": address_list,
    }
    return pd.DataFrame(data=data).loc[:, ["position_name", "prev_position", "address"]]


next_position_schema = StructType([
    StructField("position_name", StringType()),
    StructField("next_position", StringType()),
    StructField("address", StringType()),
])


@pandas_udf(next_position_schema, PandasUDFType.GROUPED_MAP)
def next_position(pdf):
    position_list = []
    next_position_list = []
    address_list = []
    rows, columns = pdf.shape
    if rows > 1:
        pdf = pdf.sort_values(by="work_index", ascending=False)
        for i in range(rows - 1):
            if pdf.iloc[i, 0] == pdf.iloc[i + 1, 0]:
                continue
            position_list.append(pdf.iloc[i, 0])
            next_position_list.append(pdf.iloc[i + 1, 0])
            address_list.append(pdf.iloc[i, 1])
    data = {
        "position_name": position_list,
        "next_position": next_position_list,
        "address": address_list,
    }
    return pd.DataFrame(data=data).loc[:, ["position_name", "next_position", "address"]]


next_same_position_schema = StructType([
    StructField("position_name", StringType()),
    StructField("address", StringType()),
])


@pandas_udf(next_same_position_schema, PandasUDFType.GROUPED_MAP)
def next_same_position(pdf):
    position_list = []
    address_list = []
    pdf = pdf.sort_values(by="work_index", ascending=False)
    rows, columns = pdf.shape
    if rows > 1:
        for i in range(rows - 1):
            # 如果下一份工作没有变化
            if pdf.iloc[i, 0] == pdf.iloc[i + 1, 0] and pdf.iloc[i, 0] not in position_list:
                position_list.append(pdf.iloc[i, 0])
                address_list.append(pdf.iloc[i, 1])
    data = {
        "position_name": position_list,
        "address": address_list,
    }
    return pd.DataFrame(data=data).loc[:, ["position_name", "address"]]


change_rank_schema = StructType([
    StructField("position_name", StringType()),
    StructField("address", StringType()),
    StructField("rank", IntegerType()),
    StructField("person_num", IntegerType()),
])


@pandas_udf(change_rank_schema, PandasUDFType.GROUPED_MAP)
def change_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="person_num", ascending=False)

    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf[["position_name", "address", "rank", "person_num"]]


industry_rank_schema = StructType([
    StructField("position_name", StringType()),
    StructField("address", StringType()),
    StructField("industry", StringType()),
    StructField("rank", IntegerType()),
    StructField("person_num", IntegerType()),
])


@pandas_udf(industry_rank_schema, PandasUDFType.GROUPED_MAP)
def industry_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="person_num", ascending=False)

    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf[
        ["position_name", "address", "industry", "rank", "person_num"]]


duration_rank_schema = StructType([
    StructField("position_name", StringType()),
    StructField("address", StringType()),
    StructField("avg_duration", FloatType()),
    StructField("rank", IntegerType()),
    StructField("person_num", IntegerType()),
])


@pandas_udf(duration_rank_schema, PandasUDFType.GROUPED_MAP)
def duration_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="avg_duration", ascending=False)
    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf[["position_name", "address", "avg_duration", "rank", "person_num"]]
