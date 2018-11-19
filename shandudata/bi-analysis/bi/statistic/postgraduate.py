# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

from pyspark.sql import functions as F
from pyspark.sql.functions import PandasUDFType, pandas_udf
from pyspark.sql.types import *

from bi.core.filter import filter_min
from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_SALARY, NA
from bi.utils import cal_avg_salary, get_years


def postgraduate(profile_df, education_df, work_df, mysql_url):
    """
    留学、考研、就业分析
    :param profile_df: 简历基本信息
    :param education_df: 简历教育经历
    :param work_df: 简历工作经历
    :param mysql_url: 数据库路径
    :return: 
    """
    education_df = education_df.filter(education_df.school_name.isNotNull()) \
        .filter(education_df.major.isNotNull()) \
        .filter(education_df.degree.isNotNull())
    education_df = education_df.select("resume_id", "school_name", "school_area", "major", "degree", "edu_index",
                                       "edu_end_date")
    education_df = education_df.groupby("resume_id").apply(cal_postgraduate)
    education_df = education_df.filter(education_df.postgraduate.isNotNull()).filter(education_df.flag.isNull())
    education_df.persist()

    # 计算每份工作平均薪资
    work_df = work_df.withColumn("avg_salary",
                                 F.udf(cal_avg_salary, FloatType())(work_df.salary_min, work_df.salary_max))
    work_df = work_df.filter(work_df.avg_salary > MIN_SALARY)

    # # 过滤掉只有简历概要信息的所有数据（工作经历分数大于等于2）
    # wc_df = work_df.filter(work_df.work_index == 2).select("resume_id")
    # edu_df = wc_df.join(education_df, "resume_id")

    # 组合教育经历和工作经历
    df = education_df.join(work_df, "resume_id")
    df = df.withColumn("work_month", F.months_between(df.work_end_date, df.edu_end_date))
    df = df.withColumn("work_year", F.udf(get_years, IntegerType())(df.work_month))
    df = df.filter(df.work_year >= 0).filter(df.work_year <= 40)

    # 分析结果表
    result_tables = dict()
    result_tables["school__major__postgraduate__ratio__v1"] = postgraduate_ratio(education_df)
    result_tables["school__major__postgraduate__work_year__v1"] = postgraduate_work_year(df)
    # 删除持续化数据
    education_df.unpersist()
    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)


def postgraduate_ratio(df):
    """
    学校毕业后留学、考研、就业比例分析
    :param df:
    :return:
    """
    sdf = df.cube("school_name", "major", "degree", "postgraduate").agg(F.count("*").alias("person_num"))
    sdf = sdf.dropna(subset=["postgraduate"])
    sdf = sdf.dropna(how="all", subset=["school_name", "major", "degree"])
    sdf = sdf.fillna({"school_name": NA, "major": NA, "degree": NA})
    return sdf


@filter_min
def postgraduate_work_year(df):
    """
    学校毕业后留学、考研、就业薪酬增长分析
    :param df:
    :return:
    """
    sdf = df.cube("school_name", "major", "degree", "postgraduate", "work_year") \
        .agg(F.count("*").alias("person_num"), F.avg(df.avg_salary).alias("avg_salary"))
    sdf = sdf.dropna(subset=["postgraduate"])
    sdf = sdf.dropna(subset=["work_year"])
    sdf = sdf.dropna(how="all", subset=["school_name", "major", "degree"])
    sdf = sdf.fillna({"school_name": NA, "major": NA, "degree": NA})
    return sdf


cal_postgraduate_schema = StructType([
    StructField("resume_id", StringType()),
    StructField("school_name", StringType()),
    StructField("major", StringType()),
    StructField("degree", StringType()),
    StructField("postgraduate", StringType()),
    StructField("edu_index", IntegerType()),
    StructField("edu_end_date", StringType()),
    StructField("flag", StringType()),
])


@pandas_udf(cal_postgraduate_schema, PandasUDFType.GROUPED_MAP)
def cal_postgraduate(pdf):
    pdf["postgraduate"] = None
    pdf["flag"] = None
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
    if count == 1 and pdf.iloc[0].degree in ["硕士", "博士"]:
        pdf["flag"] = "true"
    return pdf.loc[:, ["resume_id", "school_name", "major", "degree", "postgraduate", "edu_index",
                       "edu_end_date", "flag"]]
