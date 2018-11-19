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


def statistic_school(df, mysql_url):
    """
    学校相关分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    # 数据过滤
    df = df.filter(df.avg_salary > MIN_SALARY)
    df = df.filter(df.school_name.isNotNull()).filter(df.degree.isNotNull())
    latest_work_df = df.filter(df.work_index == df.work_len)
    # 持续化数据
    df.persist()
    latest_work_df.persist()
    # 分析结果表
    result_tables = dict()
    result_tables["school__rank"] = statistic_school_rank(latest_work_df)
    result_tables["school__gender"] = statistic_school_gender(latest_work_df)
    result_tables["school__address"] = statistic_school_address(latest_work_df)
    result_tables["school__company"] = statistic_school_company(df)
    result_tables["school__industry"] = statistic_school_industry(df)
    result_tables["school__position"] = statistic_school_position(df)
    # result_tables["school__work_year"] = statistic_school_work_year(df)
    # 删除持续化数据
    df.unpersist()
    latest_work_df.unpersist()
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)


@filter_min
def statistic_school_rank(df):
    """
    专业排名
    :param df: 
    :return: 
    """
    groups = ("school_name", "degree")
    df = add_median_salary(df, groups)
    sd_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                    F.first("avg_salary").alias("avg_salary"))
    sd_df = sd_df.filter(sd_df.person_num > MIN_NUM)
    # 不限degree分析
    s_df = sd_df.groupby("school_name").agg(F.sum("person_num").alias("person_num"),
                                            F.avg("avg_salary").alias("avg_salary"))
    s_df = s_df.withColumn("degree", F.lit(NA))
    sd_df = sd_df.unionByName(s_df)
    sd_df = sd_df.filter(sd_df.person_num > MIN_NUM)
    sd_df = add_rank(sd_df, "degree")
    return sd_df


@filter_min
def statistic_school_gender(df):
    """
    学校和性别对应的分析
    :param df: 
    :return: 
    """
    df = df.filter(df.gender.isNotNull())
    groups = ("school_name", "degree", "gender")
    df = add_median_salary(df, groups)
    sdg_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                     F.first("avg_salary").alias("avg_salary"))
    sdg_df = sdg_df.filter(sdg_df.person_num > MIN_NUM)
    sg_df = sdg_df.groupby("school_name", "gender").agg(F.sum("person_num").alias("person_num"),
                                                        F.avg("avg_salary").alias("avg_salary"))
    sg_df = sg_df.withColumn("degree", F.lit(NA))
    sdg_df = sdg_df.unionByName(sg_df)
    return sdg_df


@filter_min
def statistic_school_address(df):
    """
    学校和工作地对应的分析
    :param df: 
    :return: 
    """
    df = df.filter(df.address.isNotNull())
    groups = ("school_name", "degree", "address")
    df = add_median_salary(df, groups)
    sda_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                     F.first("avg_salary").alias("avg_salary"))
    sda_df = sda_df.filter(sda_df.person_num > MIN_NUM)
    # 不限degree分析
    sa_df = sda_df.groupby("school_name", "address").agg(F.sum("person_num").alias("person_num"),
                                                         F.avg("avg_salary").alias("avg_salary"))
    sa_df = sa_df.withColumn("degree", F.lit(NA))
    sda_df = sda_df.unionByName(sa_df)
    return sda_df


@filter_min
def statistic_school_company(df):
    """
    学校和公司对应的分析
    :param df: 
    :return: 
    """
    df = df.filter(df.company_name.isNotNull())
    groups = ("school_name", "degree", "company_name")
    df = add_median_salary(df, groups)
    sdc_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                     F.first("avg_salary").alias("avg_salary"))
    sdc_df = sdc_df.filter(sdc_df.person_num > MIN_NUM)
    sc_df = sdc_df.groupby("school_name", "company_name").agg(F.sum("person_num").alias("person_num"),
                                                              F.avg("avg_salary").alias("avg_salary"))
    sc_df = sc_df.withColumn("degree", F.lit(NA))
    sc_df = sdc_df.unionByName(sc_df)
    return sc_df


@filter_min
def statistic_school_industry(df):
    """
    学校和行业对应的分析
    :param df: 
    :return: 
    """
    df = df.filter(df.industry.isNotNull())
    groups = ("school_name", "degree", "industry")
    df = add_median_salary(df, groups)
    sdi_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                     F.first("avg_salary").alias("avg_salary"))
    sdi_df = sdi_df.filter(sdi_df.person_num > MIN_NUM)
    si_df = sdi_df.groupby("school_name", "industry").agg(F.sum("person_num").alias("person_num"),
                                                          F.avg("avg_salary").alias("avg_salary"))
    si_df = si_df.withColumn("degree", F.lit(NA))
    si_df = sdi_df.unionByName(si_df)
    return si_df


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


def statistic_school_position(df):
    """
    学校和职位对应的分析
    :param df: 
    :return: 
    """
    df = df.filter(df.position_name.isNotNull())
    groups = ("school_name", "degree", "position_name")
    df = add_median_salary(df, groups)
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
    sdp_df = df.groupby(*groups).agg(F.count("*").alias("person_num"),
                                     F.first("avg_salary").alias("avg_salary"))
    sdp_df = sdp_df.filter(sdp_df.person_num > MIN_NUM)
    # 不限degree分析
    sp_df = sdp_df.groupby("school_name", "position_name").agg(F.sum("person_num").alias("person_num"),
                                                               F.avg("avg_salary").alias("avg_salary"))
    sp_df = sp_df.withColumn("degree", F.lit(NA))
    sdp_df = sdp_df.unionByName(sp_df)
    # 融合职位别名
    sdp_df = sdp_df.join(pdf, "position_name")
    # 融合职位对应的行业
    sdp_df = sdp_df.join(idf, "position_name")
    return sdp_df


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


school_rank_schema = StructType([
    StructField("school_name", StringType()),
    StructField("degree", StringType()),
    StructField("person_num", IntegerType()),
    StructField("avg_salary", FloatType()),
    StructField("rank", IntegerType()),
])


def statistic_school_work_year(df):
    """
    学校和工作年限对应的分析
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

    df = filter_cube_num(df, "school_name", "degree", "work_year")
    # 各学校对应工作年限的平均薪资
    sdw_df = df.cube("school_name", "degree", "work_year").agg(F.count("*").alias("person_num"),
                                                               F.avg(df.avg_salary).alias("avg_salary"))
    sdw_df = sdw_df.filter(sdw_df.work_year.isNotNull())
    sdw_df = sdw_df.fillna({"school_name": NA, "degree": NA})
    return sdw_df


@pandas_udf(school_rank_schema, PandasUDFType.GROUPED_MAP)
def school_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="avg_salary", ascending=False, na_position='last')
    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf.loc[:, ["school_name", "degree", "person_num", "avg_salary", "rank"]]
