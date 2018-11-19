# -*- coding: utf-8 -*-
"""
@Time    : 2018/6/11
@Author   : huanggangyu
"""
from pyspark.sql.types import *
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql import functions as F


def get_position_alias(df):
    """
    获取职位别名
    :param df:
    :return:
    """

    df = df.withColumn("position_title", F.lower(F.trim(df.position_title)))
    pdf = df.groupby("position_name", "position_title").agg(F.count("*").alias("total"))
    pdf = pdf.groupby("position_name").apply(filter_position)
    pdf = pdf.groupby("position_name").agg(F.collect_set("position_title").alias("position_set"))
    pdf = pdf.withColumn("position_alias", F.udf(lambda x: "/".join(x))(pdf.position_set))
    pdf = pdf.select("position_name", "position_alias")
    return pdf


def get_position_industry(df):
    """
    获取职位对应的行业
    :param df:
    :return:
    """

    idf = df.groupby("position_name", "industry").agg(F.count("*").alias("total"))
    idf = idf.groupby("position_name").apply(filter_industry)
    idf = idf.groupby("position_name").agg(F.collect_set("industry").alias("industry_set"))
    idf = idf.withColumn("industry_alias", F.udf(lambda x: "/".join(x))(idf.industry_set))
    idf = idf.select("position_name", "industry_alias")
    return idf


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
