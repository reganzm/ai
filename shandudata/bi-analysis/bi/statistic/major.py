# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

import datetime

from pyspark.sql import functions as F
from pyspark.sql.functions import PandasUDFType, pandas_udf
from pyspark.sql.types import *

from bi.core.common import add_median_salary, add_rank, filter_cube_num
from bi.core.filter import filter_min
from bi.core.save_to_mysql import write_mysql
from bi.settings import LATEST_YEAR, MIN_NUM, MIN_SALARY, NA


def statistic_major(df, mysql_url):
    """
    专业相关分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    # 数据过滤
    df = df.filter(df.major.isNotNull()).filter(df.degree.isNotNull())
    df = df.filter((df.salary_min > MIN_SALARY)).filter(df.salary_max >= df.salary_min)
    # 最近5年本专业应届毕业生去向
    latest_work_df = df.filter(df.work_index == df.work_len) \
        .filter(df.edu_end_year >= datetime.datetime.now().year - LATEST_YEAR)

    # 持续化数据
    df.persist()
    latest_work_df.persist()

    # 分析结果表
    result_tables = dict()
    result_tables["major__rank"] = statistic_major_rank(latest_work_df)
    result_tables["major__gender"] = statistic_major_gender(latest_work_df)
    result_tables["major__address"] = statistic_major_address(latest_work_df)
    result_tables["major__company"] = statistic_major_company(latest_work_df)
    result_tables["major__industry"] = statistic_major_industry(latest_work_df)
    result_tables["major__position"] = statistic_major_position(latest_work_df)
    # result_tables["major__work_year"] = statistic_major_work_year(df)
    # 删除持续化数据
    df.unpersist()
    latest_work_df.unpersist()
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)


@filter_min
def statistic_major_rank(df):
    """
    专业排名
    :param df: 
    :return: 
    """
    groups = ("major", "degree")
    df = add_median_salary(df, groups)
    md_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                    F.first("avg_salary").alias("avg_salary"))
    md_df = md_df.filter(md_df.person_num > MIN_NUM)
    # 不限degree分析
    m_df = md_df.groupby("major").agg(F.sum("person_num").alias("person_num"),
                                      F.avg("avg_salary").alias("avg_salary"))
    m_df = m_df.withColumn("degree", F.lit(NA))
    md_df = md_df.unionByName(m_df)
    md_df = md_df.filter(md_df.person_num > MIN_NUM)
    md_df = add_rank(md_df, "degree")
    return md_df


@filter_min
def statistic_major_gender(df):
    """
    专业对应的
    :param df: 
    :return: 
    """
    groups = ("major", "degree", "gender")
    df = df.filter(df.gender.isNotNull())
    df = add_median_salary(df, groups)
    mdf1 = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                   F.first(df.avg_salary).alias("avg_salary"))
    mdf1 = mdf1.filter(mdf1.person_num > MIN_NUM)
    mdf2 = mdf1.groupby("major", "gender").agg(F.sum("person_num").alias("person_num"),
                                               F.avg("avg_salary").alias("avg_salary"))
    mdf2 = mdf2.withColumn("degree", F.lit(NA))
    mdf2 = mdf1.unionByName(mdf2)
    return mdf2


@filter_min
def statistic_major_address(df):
    """
    专业和工作地分析
    :param df: 
    :return: 
    """
    groups = ("major", "degree", "address")
    df = df.filter(df.address.isNotNull())
    df = add_median_salary(df, groups)
    mda_pdf = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                      F.first(df.avg_salary).alias("avg_salary"))
    mda_pdf = mda_pdf.filter(mda_pdf.person_num > MIN_NUM)
    ma_pdf = mda_pdf.groupby("major", "address").agg(F.sum("person_num").alias("person_num"),
                                                     F.avg("avg_salary").alias("avg_salary"))
    ma_pdf = ma_pdf.withColumn("degree", F.lit(NA))
    ma_pdf = mda_pdf.unionByName(ma_pdf)
    return ma_pdf


@filter_min
def statistic_major_company(df):
    """
    最近5年本专业毕业生公司去向分布
    :param df: 
    :return: 
    """
    groups = ("major", "degree", "company_name")
    df = df.filter(df.company_name.isNotNull())
    df = add_median_salary(df, groups)
    mdc_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                     F.first(df.avg_salary).alias("avg_salary"))
    mdc_df = mdc_df.filter(mdc_df.person_num > MIN_NUM)
    mc_df = mdc_df.groupby("major", "company_name").agg(F.sum("person_num").alias("person_num"),
                                                        F.avg("avg_salary").alias("avg_salary"))
    mc_df = mc_df.withColumn("degree", F.lit(NA))
    mc_df = mdc_df.unionByName(mc_df)
    return mc_df


@filter_min
def statistic_major_industry(df):
    """
    专业对应的
    :param df:
    :return: 
    """
    groups = ("major", "degree", "industry")
    df = df.filter(df.industry.isNotNull())
    mdi_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                     F.first(df.avg_salary).alias("avg_salary"))
    mdi_df = mdi_df.filter(mdi_df.person_num > MIN_NUM)
    mi_df = mdi_df.groupby("major", "industry").agg(F.sum("person_num").alias("person_num"),
                                                    F.avg("avg_salary").alias("avg_salary"))
    mi_df = mi_df.withColumn("degree", F.lit(NA))
    mdi_df = mdi_df.unionByName(mi_df)
    return mdi_df


def statistic_major_position(df):
    """
    专业对应的
    :param df: 
    :return: 
    """
    groups = ("major", "degree", "position_name")
    df = df.filter(df.position_name.isNotNull())
    # 职位别名
    df = df.withColumn("position_title", F.lower(F.trim(df.position_title)))
    pdf = df.groupby("position_name", "position_title").agg(F.count("*").alias("total"))
    pdf = pdf.groupby("position_name").apply(filter_position)
    pdf = pdf.groupby("position_name").agg(F.collect_set("position_title").alias("position_set"))
    pdf = pdf.withColumn("position_alias", F.udf(lambda x: "/".join(x))(pdf.position_set))
    pdf = pdf.select("position_name", "position_alias")
    # 职位对应行业
    idf = df.groupby("position_name", "industry").agg(F.count("*").alias("total"))
    idf = idf.groupby("position_name").apply(filter_industry)
    idf = idf.groupby("position_name").agg(F.collect_set("industry").alias("industry_set"))
    idf = idf.withColumn("industry_alias", F.udf(lambda x: "/".join(x))(idf.industry_set))
    idf = idf.select("position_name", "industry_alias")
    # 限制degree分析
    df = add_median_salary(df, groups)
    mdp_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                     F.first(df.avg_salary).alias("avg_salary"))
    mdp_df = mdp_df.filter(mdp_df.person_num > MIN_NUM)
    # 不限degree分析
    mp_df = mdp_df.groupby("major", "position_name").agg(F.sum("person_num").alias("person_num"),
                                                         F.avg("avg_salary").alias("avg_salary"))
    mp_df = mp_df.withColumn("degree", F.lit(NA))
    mdp_df = mdp_df.unionByName(mp_df)

    # 融合职位别名
    mdp_df = mdp_df.join(pdf, "position_name")
    # 融合职位对应的行业
    mdp_df = mdp_df.join(idf, "position_name")
    return mdp_df


position_schema = StructType([
    StructField("position_name", StringType()),
    StructField("position_title", StringType()),
    StructField("total", IntegerType()),
])

industry_schema = StructType([
    StructField("position_name", StringType()),
    StructField("industry", StringType()),
    StructField("total", IntegerType()),
])


@pandas_udf(position_schema, PandasUDFType.GROUPED_MAP)
def filter_position(pdf):
    pdf = pdf[pdf["total"] > 2]
    pdf = pdf.sort_values(by="total")
    # 和schema顺序一致
    return pdf[:10]


@pandas_udf(industry_schema, PandasUDFType.GROUPED_MAP)
def filter_industry(pdf):
    pdf = pdf[pdf["total"] > 2]
    pdf = pdf.sort_values(by="total")
    # 和schema顺序一致
    return pdf[:3]


major_rank_schema = StructType([
    StructField("major", StringType()),
    StructField("degree", StringType()),
    StructField("person_num", IntegerType()),
    StructField("avg_salary", FloatType()),
    StructField("rank", IntegerType()),
])


@filter_min
def statistic_major_work_year(df):
    """
    专业对应的
    :param df: 
    :return: 
    """
    # 过滤出有效数据
    df = df.filter((df.salary_min > MIN_SALARY)) \
        .filter(df.work_year >= 0) \
        .filter(df.work_year <= 40) \
        .filter(df.work_end_year >= (datetime.datetime.now().year - LATEST_YEAR))
    # 计算当前工作的平均薪资，毕业到当前工作的年限
    df = df.withColumn("avg_salary", F.udf(lambda x, y: (x + y) / 2, FloatType())(df.salary_min, df.salary_max))
    # 先过滤掉样本不足的情况
    df = filter_cube_num(df, "major", "degree", "work_year")
    # 各专业对应工作年限的平均薪资
    mdw_df = df.cube("major", "degree", "work_year").agg(F.count("*").alias("person_num"),
                                                         F.avg(df.avg_salary).alias("avg_salary"))
    mdw_df = mdw_df.filter(mdw_df.work_year.isNotNull())
    mdw_df = mdw_df.fillna({"major": NA, "degree": NA})
    return mdw_df


@pandas_udf(major_rank_schema, PandasUDFType.GROUPED_MAP)
def major_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="avg_salary", ascending=False)

    for index, row in pdf.iterrows():
        if row.major == NA:
            pdf.at[index, "rank"] = row.person_num
        else:
            count += 1
            pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf.loc[:, ["major", "degree", "person_num", "avg_salary", "rank"]]
