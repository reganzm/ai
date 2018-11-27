# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

from pyspark.sql import functions as F

from bi.core.filter import filter_min
from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_SALARY, NA


def statistic_industry_position_address(df, mysql_url):
    """
    行业相关维度分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    # 数据过滤
    df = df.filter(df.industry.isNotNull()).filter(df.position_name.isNotNull()).filter(df.address.isNotNull())
    df.persist()
    # 分析结果表
    result_tables = dict()
    result_tables["industry__position__address__work_year"] = statistic_industry_position_address_work_year(df)
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)
    df.unpersist()


@filter_min
def statistic_industry_position_address_work_year(df):
    """
    行业对应职位分布
    :param df: 
    :return: 
    """
    df = df.filter((df.avg_salary > MIN_SALARY))
    mdf = df.groupby("industry", "position_name", "address", "work_year").agg(F.count("*").alias("person_num"),
                                                                              F.avg(df.avg_salary).alias("avg_salary"))
    sdf = mdf.groupby("industry", "position_name", "work_year").agg(F.sum("person_num").alias("person_num"),
                                                                    F.avg(mdf.avg_salary).alias("avg_salary"))
    sdf = sdf.withColumn("address", F.udf(lambda: NA)())
    return mdf.unionByName(sdf)
