# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

import pandas as pd
from pyspark.sql.functions import PandasUDFType, pandas_udf
from pyspark.sql.types import *

from bi.core.common import add_median_salary, add_rank
from bi.core.filter import *
from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_AGE, MIN_SALARY, NA, MIN_NUM


def statistic_company(df, mysql_url):
    """
    公司相关维度分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    # 数据过滤
    df = df.filter(df.company_name.isNotNull()).filter(df.position_category.isNotNull())
    latest_work_df = df.filter(df.work_index == df.work_len)
    # 持续化数据
    df.persist()
    latest_work_df.persist()
    # 分析结果表
    result_tables = dict()
    result_tables["company__rank"] = statistic_company_rank(df)
    result_tables["company__salary"] = statistic_company_salary(df)
    result_tables["company__gender"] = statistic_company_gender(df)
    result_tables["company__age"] = statistic_company_age(df)
    result_tables["company__address"] = statistic_company_address(df)
    # result_tables["company__work_year"] = statistic_company_work_year(df)
    result_tables["company__school"] = statistic_company_school(df)
    result_tables["company__major"] = statistic_company_major(df)
    result_tables["company__degree"] = statistic_company_degree(df)
    result_tables["company__prev_company"] = statistic_company_prev_company(df)
    result_tables["company__next_company"] = statistic_company_next_company(df)
    result_tables["company__duration"] = statistic_company_duration(df)
    # 删除持续化数据
    df.unpersist()
    latest_work_df.unpersist()
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)


@filter_min
def statistic_company_rank(df):
    """
    公司排名
    :param df: 
    :return: 
    """
    df = df.filter((df.avg_salary > MIN_SALARY))
    df = add_median_salary(df, ("company_name",))
    # 计算当前工作的平均薪资，毕业到当前工作的年限
    mdf = df.groupby("company_name").agg(F.count("*").alias("person_num"), F.first("avg_salary").alias("avg_salary"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    mdf = add_rank(mdf)
    return mdf


def statistic_company_salary(df):
    """
    薪资区间分布
    :param df: 
    :return: 
    """
    df = df.filter(df.salary_range.isNotNull())
    mdf = df.groupby("company_name", "position_category", "salary_range").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name", "salary_range").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_company_age(df):
    """
    公司对应年龄分布
    :param df: 
    :return: 
    """
    df = df.filter(df.age >= MIN_AGE)
    df = filter_cube_num(df, "company_name", "position_category")
    mdf = df.cube("company_name", "position_category").agg(F.count("*").alias("person_num"),
                                                           F.avg(df.age).alias("avg_age"))
    mdf = mdf.fillna({"company_name": NA, "position_category": NA})
    return mdf


def statistic_company_gender(df):
    """
    公司对应性别分布
    :param df: 
    :return: 
    """
    df = df.filter(df.gender.isNotNull())
    mdf = df.groupby("company_name", "position_category", "gender").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name", "gender").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_company_address(df):
    """
    公司对应地区分布
    :param df: 
    :return: 
    """
    df = df.filter(df.address.isNotNull())
    mdf = df.groupby("company_name", "position_category", "address").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name", "address").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_company_work_year(df):
    """
    公司对应工作年限分布
    :param df: 
    :return: 
    """
    df = df.filter(df.work_year >= 0).filter(df.work_year <= 40)
    mdf = df.groupby("company_name", "position_category").agg(F.count("*").alias("person_num"),
                                                              F.avg(df.work_year).alias("avg_work_year"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name").agg(F.sum("person_num").alias("person_num"),
                                          F.avg(mdf.avg_work_year).alias("avg_work_year"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_company_school(df):
    """
    公司对应学校分布
    :param df: 
    :return: 
    """
    df = df.filter(df.school_name.isNotNull())
    mdf = df.groupby("company_name", "position_category", "school_name").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name", "school_name").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_company_major(df):
    """
    公司对应专业分布
    :param df: 
    :return: 
    """
    df = df.filter(df.major.isNotNull())
    mdf = df.groupby("company_name", "position_category", "major").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name", "major").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_company_degree(df):
    """
    公司对应学历分布
    :param df: 
    :return: 
    """
    df = df.filter(df.degree.isNotNull())
    mdf = df.groupby("company_name", "position_category", "degree").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name", "degree").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_company_prev_company(df):
    """
    当前职位的上一份职位分布
    :param df: 
    :return: 
    """
    df = df.select("company_name", "position_category", "resume_id", "work_index")
    mdf = df.groupby("resume_id").apply(company_prev_company)
    mdf = mdf.groupby("company_name", "prev_company", "position_category").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name", "prev_company").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_company_next_company(df):
    """
    当前职位的下一份职位分布
    :param df: 
    :return: 
    """
    df = df.select("company_name", "position_category", "resume_id", "work_index")
    mdf = df.groupby("resume_id").apply(company_next_company)
    mdf = mdf.groupby("company_name", "next_company", "position_category").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name", "next_company").agg(F.sum("person_num").alias("person_num"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


def statistic_company_duration(df):
    """
    当前工作的工作时长（年）
    :param df: 
    :return: 
    """
    df = df.filter(df.work_duration_year.isNotNull())
    df = df.filter(df.age >= MIN_AGE)
    mdf = df.groupby("company_name", "position_category").agg(F.count("*").alias("person_num"),
                                                              F.avg(df.work_duration_year).alias("avg_duration"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name").agg(F.sum("person_num").alias("person_num"),
                                          F.avg(mdf.avg_duration).alias("avg_duration"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    return mdf.unionByName(sdf)


company_rank_schema = StructType([
    StructField("company_name", StringType()),
    StructField("person_num", IntegerType()),
    StructField("avg_salary", FloatType()),
    StructField("rank", IntegerType()),
])

company_prev_company_schema = StructType([
    StructField("company_name", StringType()),
    StructField("prev_company", StringType()),
    StructField("position_category", StringType()),
])

company_next_company_schema = StructType([
    StructField("company_name", StringType()),
    StructField("next_company", StringType()),
    StructField("position_category", StringType()),
])


@pandas_udf(company_rank_schema, PandasUDFType.GROUPED_MAP)
def company_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="avg_salary", ascending=False)
    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf.loc[:, ["company_name", "person_num", "avg_salary", "rank"]]


@pandas_udf(company_prev_company_schema, PandasUDFType.GROUPED_MAP)
def company_prev_company(pdf):
    company_list = []
    prev_company_list = []
    position_category_list = []
    rows, columns = pdf.shape
    if rows > 1:
        pdf = pdf.sort_values(by="work_index", ascending=False)
        for i in range(1, rows):
            if pdf.iloc[i, 0] == pdf.iloc[i - 1, 0]:
                continue
            company_list.append(pdf.iloc[i, 0])
            prev_company_list.append(pdf.iloc[i - 1, 0])
            position_category_list.append(pdf.iloc[i, 1])
    data = {
        "company_name": company_list,
        "prev_company": prev_company_list,
        "position_category": position_category_list,
    }
    return pd.DataFrame(data=data).loc[:, ["company_name", "prev_company", "position_category"]]


@pandas_udf(company_next_company_schema, PandasUDFType.GROUPED_MAP)
def company_next_company(pdf):
    company_list = []
    next_company_list = []
    position_category_list = []
    rows, columns = pdf.shape
    if rows > 1:
        pdf = pdf.sort_values(by="work_index", ascending=False)
        for i in range(rows - 1):
            if pdf.iloc[i, 0] == pdf.iloc[i + 1, 0]:
                continue
            company_list.append(pdf.iloc[i, 0])
            next_company_list.append(pdf.iloc[i + 1, 0])
            position_category_list.append(pdf.iloc[i, 1])
    data = {
        "company_name": company_list,
        "next_company": next_company_list,
        "position_category": position_category_list,
    }
    return pd.DataFrame(data=data).loc[:, ["company_name", "next_company", "position_category"]]
