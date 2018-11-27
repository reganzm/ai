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
from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_SALARY, MIN_NUM


def statistic_industry(df, mysql_url):
    """
    行业相关维度分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    # 数据过滤
    df = df.filter(df.industry.isNotNull())
    df.persist()
    # 分析结果表
    result_tables = dict()
    result_tables["industry__rank"] = statistic_industry_rank(df)
    result_tables["industry__address"] = statistic_industry_address(df)
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)
    df.unpersist()


def statistic_industry_rank(df):
    """
    行业排行
    :param df: 
    :return: 
    """
    df = df.filter((df.avg_salary > MIN_SALARY))
    df = add_median_salary(df, ("industry",))
    mdf = df.groupby("industry").agg(F.count("*").alias("person_num"), F.first(df.avg_salary).alias("avg_salary"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    mdf = add_rank(mdf)
    return mdf


def statistic_industry_address(df):
    """
    行业对应地域分布
    :param df: 
    :return: 
    """
    df = df.filter(df.address.isNotNull())
    df = df.groupby("industry", "address").agg(F.count("*").alias("person_num"))
    df = df.filter(df.person_num > MIN_NUM)
    return df


industry_rank_schema = StructType([
    StructField("industry", StringType()),
    StructField("person_num", IntegerType()),
    StructField("avg_salary", FloatType()),
    StructField("rank", IntegerType()),
])


@pandas_udf(industry_rank_schema, PandasUDFType.GROUPED_MAP)
def industry_rank(pdf):
    count = 0
    pdf['rank'] = 0
    pdf = pdf.sort_values(by="avg_salary", ascending=False)
    for index, row in pdf.iterrows():
        count += 1
        pdf.at[index, "rank"] = count
    # 和schema顺序一致
    return pdf.loc[:, ["industry", "person_num", "avg_salary", "rank"]]
