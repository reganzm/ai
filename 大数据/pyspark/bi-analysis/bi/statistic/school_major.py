# -*- coding: utf-8 -*-
"""
@Time    : 2018/6/11
@Author   : huanggangyu
"""

import datetime

from bi.core.alias import *
from bi.core.common import add_median_salary, filter_cube_num
from bi.core.filter import *
from bi.core.save_to_mysql import write_mysql
from bi.settings import LATEST_YEAR, MIN_NUM, MIN_SALARY, NA


def statistic_school_major(df, mysql_url):
    """
    学校+专业相关分析
    :param df:
    :param mysql_url:
    :return:
    """
    # 数据过滤
    df = df.filter(df.avg_salary > MIN_SALARY)
    df = df.filter(df.school_name.isNotNull()).filter(df.major.isNotNull()).filter(df.degree.isNotNull())
    latest_work_df = df.filter(df.work_index == df.work_len)
    # 持续化数据
    df.persist()
    latest_work_df.persist()
    # 分析结果表
    result_tables = dict()
    result_tables["school__major__rank"] = statistic_school_major_rank(latest_work_df)
    result_tables["school__major__position"] = statistic_school_major_position(df)
    # result_tables["school__major__work_year"] = statistic_school_major_work_year(df)
    result_tables["school__major__industry"] = statistic_school_major_industry(df)
    result_tables["school__major__company"] = statistic_school_major_company(df)
    result_tables["school__major__flow"] = statistic_school_major_flow(df)
    result_tables["school__major__position__rank"] = statistic_school_major_position_rank(df)
    # 删除持续化数据
    df.unpersist()
    latest_work_df.unpersist()
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)


@filter_min
def statistic_school_major_rank(df):
    """
    各学校各专业排名
    :param df:
    :return:
    """
    # 计算当前工作的平均薪资，毕业到当前工作的年限
    groups = ("school_name", "major", "degree")
    df = filter_cube_num(df, *groups)
    df = add_median_salary(df, groups)
    smd_df = df.cube(*groups).agg(F.count("*").alias("person_num"),
                                  F.avg(df.avg_salary).alias("avg_salary"))
    smd_df = smd_df.fillna({"school_name": NA, "major": NA, "degree": NA})
    smd_df = smd_df.cube("major", "degree").apply(school_major_rank)
    return smd_df


@filter_min
def statistic_school_major_position(df):
    """
    学校、专业维度下的职位人数和薪酬分析
    :param df:
    :return:
    """
    df = df.filter(df.position_name.isNotNull())
    groups = ("school_name", "major", "degree", "position_name")
    df = filter_cube_num(df, *groups)
    df = add_median_salary(df, groups)
    smdp_df = df.cube(*groups).agg(F.count("*").alias("person_num"),
                                   F.avg(df.avg_salary).alias("avg_salary"))
    smdp_df = smdp_df.filter(smdp_df.position_name.isNotNull())
    smdp_df = smdp_df.dropna(how="all", subset=["school_name", "major", "degree"])
    smdp_df = smdp_df.fillna({"school_name": NA, "major": NA, "degree": NA})
    return smdp_df


@filter_min
def statistic_school_major_work_year(df):
    """
    学校、专业和工作年限对应的分析
    :param df:
    :return:
    """
    # 过滤出有效信息
    df = df.filter(df.salary_min > MIN_SALARY) \
        .filter(df.work_year >= 0) \
        .filter(df.work_year <= 40) \
        .filter(df.work_end_year >= (datetime.datetime.now().year - LATEST_YEAR))
    # 计算当前工作的平均薪资，毕业到当前工作的年限
    df = df.withColumn("avg_salary", F.udf(lambda x, y: (x + y) / 2, FloatType())(df.salary_min, df.salary_max))
    df = filter_cube_num(df, "school_name", "major", "degree", "work_year")
    smdw_df = df.cube("school_name", "major", "degree", "work_year").agg(F.count("*").alias("person_num"),
                                                                         F.avg(df.avg_salary).alias("avg_salary"))
    smdw_df = smdw_df.filter(smdw_df.work_year.isNotNull())
    smdw_df = smdw_df.dropna(how="all", subset=["school_name", "major", "degree"])
    smdw_df = smdw_df.fillna({"school_name": NA, "major": NA, "degree": NA})
    return smdw_df


@filter_min
def statistic_school_major_industry(df):
    """
    学校、专业和行业对应的分析
    :param df:
    :return:
    """
    df = df.filter(df.industry.isNotNull())
    groups = ("school_name", "major", "degree", "industry")
    df = filter_cube_num(df, *groups)
    df = add_median_salary(df, groups)
    smdi_df = df.cube("school_name", "major", "degree", "industry").agg(F.count("*").alias("person_num"),
                                                                        F.avg(df.avg_salary).alias("avg_salary"))
    smdi_df = smdi_df.filter(smdi_df.industry.isNotNull())
    smdi_df = smdi_df.dropna(how="all", subset=["school_name", "major", "degree"])
    smdi_df = smdi_df.fillna({"school_name": NA, "major": NA, "degree": NA})
    return smdi_df


@filter_min
def statistic_school_major_company(df):
    """
    学校、专业和公司对应的分析
    :param df:
    :return:
    """
    df = df.filter(df.company_name.isNotNull())
    groups = ("school_name", "major", "degree", "company_name")
    df = filter_cube_num(df, *groups)
    df = add_median_salary(df, groups)
    smdc_df = df.cube("school_name", "major", "degree", "company_name").agg(F.count("*").alias("person_num"),
                                                                            F.avg(df.avg_salary).alias("avg_salary"))
    smdc_df = smdc_df.filter(smdc_df.company_name.isNotNull())
    smdc_df = smdc_df.dropna(how="all", subset=["school_name", "major", "degree"])
    smdc_df = smdc_df.fillna({"school_name": NA, "major": NA, "degree": NA})
    return smdc_df


@filter_min
def statistic_school_major_flow(df):
    """
    学校、专业流向分析

    :param df:
    :return:
    """
    df = df.filter(df.company_name.isNotNull()).filter(df.industry.isNotNull())
    df = filter_cube_num(df, "school_name", "major", "degree", "company_name", "industry")
    mdf = df.cube("school_name", "major", "degree", "company_name", "industry") \
        .agg(F.count("*").alias("person_num"), F.avg(df.avg_salary).alias("avg_salary"))
    mdf = mdf.dropna(how="all", subset=["company_name", "industry"])
    mdf = mdf.dropna(how="all", subset=["school_name", "major", "degree"])
    mdf = mdf.fillna({"school_name": NA, "major": NA, "degree": NA, "company_name": NA, "industry": NA})
    return mdf


school_major_rank_schema = StructType([
    StructField("school_name", StringType()),
    StructField("major", StringType()),
    StructField("degree", StringType()),
    StructField("person_num", IntegerType()),
    StructField("avg_salary", FloatType()),
    StructField("rank", IntegerType()),
])


@pandas_udf(school_major_rank_schema, PandasUDFType.GROUPED_MAP)
def school_major_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="avg_salary", ascending=False, na_position='last')
    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf.loc[:, ["school_name", "major", "degree", "person_num", "avg_salary", "rank"]]


school_major_position_schema = StructType([
    StructField("school_name", StringType()),
    StructField("major", StringType()),
    StructField("degree", StringType()),
    StructField("position_name", StringType()),
    StructField("person_num", IntegerType()),
    StructField("avg_salary", IntegerType()),
    StructField("rank", IntegerType()),
    StructField("total", IntegerType()),
])


@pandas_udf(school_major_position_schema, PandasUDFType.GROUPED_MAP)
def school_major_position_rank(pdf):
    pdf = pdf.sort_values(by="person_num", ascending=False)
    # pdf["rank"] = pd.Series(range(1, len(pdf) + 1))
    pdf["total"] = pdf.person_num.sum()
    pdf["rank"] = 0
    count = 0
    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    return pdf.loc[:, ["school_name", "major", "degree", "position_name", "person_num", "avg_salary",
                       "rank", "total"]]


def statistic_school_major_position_rank(df):
    """
    专业类别对应职位分布
    :param df:
    :return: 
    """
    df = df.filter(df.position_name.isNotNull())
    groups = ("school_name", "major", "degree", "position_name")
    df = filter_cube_num(df, *groups)
    df = add_median_salary(df, groups)
    scdp_df = df.cube(*groups).agg(F.count("*").alias("person_num"), F.avg(df.avg_salary).alias("avg_salary"))

    scdp_df = scdp_df.dropna(how="all", subset=["position_name"])
    scdp_df = scdp_df.dropna(how="all", subset=["school_name", "major"])
    scdp_df = scdp_df.fillna({"school_name": NA, "major": NA, "degree": NA})
    scdp_df = scdp_df.filter(scdp_df.person_num > MIN_NUM)
    scdp_df = scdp_df.groupby("school_name", "major", "degree").apply(school_major_position_rank)
    return scdp_df
