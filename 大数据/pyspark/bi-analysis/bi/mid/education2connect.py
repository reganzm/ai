# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 21/07/2018 09:30
:File    : education2connect.py
"""

from pyspark.sql.functions import PandasUDFType, pandas_udf
from pyspark.sql.types import *


def education2connect(education_df):
    """
    留学、考研、就业分析
    :param education_df: 简历教育经历
    :return: 
    """
    education_df = education_df.filter(education_df.school_name.isNotNull()) \
        .filter(education_df.major.isNotNull()) \
        .filter(education_df.degree.isNotNull())
    education_df = education_df.select("resume_id", "school_name", "school_area", "major", "degree", "edu_index",
                                       "edu_end_date")
    education_df = education_df.groupby("resume_id").apply(cal_postgraduate)
    education_df = education_df.filter(education_df.postgraduate.isNotNull())
    return education_df


cal_postgraduate_schema = StructType([
    StructField("resume_id", StringType()),
    StructField("school_name", StringType()),
    StructField("major", StringType()),
    StructField("degree", StringType()),
    StructField("postgraduate", StringType()),
    StructField("edu_index", IntegerType()),
    StructField("edu_end_date", StringType()),
])


@pandas_udf(cal_postgraduate_schema, PandasUDFType.GROUPED_MAP)
def cal_postgraduate(pdf):
    """教育经历连接，教育经历是逆序排列的，并计算深造情况"""
    pdf["postgraduate"] = None
    pdf = pdf.sort_values(by="edu_index")
    count = 0
    next_area = ""
    next_degree = ""
    for index, row in pdf.iterrows():
        count += 1
        if count == 1:
            pdf.at[index, "postgraduate"] = "就业"
        else:
            if next_area == "国外" and next_degree in ["硕士", "博士"]:
                pdf.at[index, "postgraduate"] = "留学"
            elif next_area == "中国":
                if next_degree == "本科" and row.degree == "大专及以下":
                    pdf.at[index, "postgraduate"] = "专升本"
                elif next_degree == "硕士" and row.degree == "本科":
                    pdf.at[index, "postgraduate"] = "考研"
                elif next_degree == "博士" and row.degree == "硕士":
                    pdf.at[index, "postgraduate"] = "考博"
                else:
                    pdf.at[index, "postgraduate"] = None
            else:
                pdf.at[index, "postgraduate"] = None
        next_area = row.school_area
        next_degree = row.degree
    return pdf.loc[:, ["resume_id", "school_name", "major", "degree", "postgraduate", "edu_index", "edu_end_date"]]
