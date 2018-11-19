# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

import re

from pyspark.sql import functions as F

from bi.core.save_to_mysql import write_mysql
from bi.settings.settings import MIN_SALARY

emoji_p = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", flags=re.UNICODE)

emoji_pattern = re.compile(
    "(\ud83d[\ude00-\ude4f])|"  # emoticons
    "(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    "(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    "(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    "(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)


# emoji_p = re.compile(
#     "["
#     "\U0001F600-\U0001F64F"  # emoticons
#     "\U0001F300-\U0001F5FF"  # symbols & pictographs
#     "\U0001F680-\U0001F6FF"  # transport & map symbols
#     "\U0001F1E0-\U0001F1FF"  # flags (iOS)
#     "\U00002702-\U000027B0"
#     "\U000024C2-\U0001F251"
#     "]+", flags=re.UNICODE)

def filter_emoji(desstr, restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def statistic_job(position_df, job_df, mysql_url):
    """
    招聘职位相关分析
    :param df: 
    :param mysql_url: 
    :return: 
    """
    job_df = job_df.filter(job_df.position_name.isNotNull())
    # position_df = filter_str(position_df, "expect_career")

    # position_df = position_df.withColumnRenamed("expect_career", "position_name") \
    #     .withColumnRenamed("update_date", "date_time").withColumnRenamed("address", "area") \
    #     .withColumnRenamed("expect_area", "address").withColumnRenamed("avg_salary", "job_avg_salary")
    #
    result_tables = dict()
    # 分析详情表
    result_tables["position__jd"] = statistic_job_jd(job_df)
    # 分析关系表
    # result_tables["job__position__relation"] = statistic_job_position_relation(job_df, position_df)

    # 将专业相关的分析结果写入数据库
    write_mysql(mysql_url, result_tables)


def statistic_job_jd(df):
    """
    职位jd分析
    :param df: 
    :return: 
    """
    df = df.filter(df.job_desc.isNotNull()).filter(F.length(df.job_desc) > 60).filter(F.length(df.job_desc) < 2000)
    # 去重
    df = df.dropDuplicates(subset=['position_name', "job_desc"])
    # df = df.withColumn("job_desc", F.udf(lambda x: emoji_pattern.sub(r'', x))(df.job_desc))
    # df = df.withColumn("job_desc", F.udf(lambda x: emoji_p.sub(r'', x))(df.job_desc))
    df = df.withColumn("job_desc", F.udf(filter_emoji)(df.job_desc))

    df = df.select("position_name", "job_desc")
    return df


def statistic_job_position_relation(job_df, position_df):
    """
    工作和职位关系分析
    :param df:
    :return:
    """
    columns = ["position_name", "address", "date_time", "position_num", "job_num", "position_avg_salary",
               "job_avg_salary"]

    job_df = job_df.filter(job_df.avg_salary != '面议').filter(job_df.avg_salary > MIN_SALARY)
    position_df = position_df.filter(position_df.job_avg_salary > MIN_SALARY)

    job_df = job_df.filter(job_df.recruit_num.isNotNull())
    job_df = job_df.groupby("position_name", "address", "date_time") \
        .agg(F.sum("recruit_num").alias("position_num"), F.avg(job_df.avg_salary).alias("position_avg_salary"))

    position_df = position_df.groupby("position_name", "address", "date_time") \
        .agg(F.count("*").alias("job_num"), F.avg(position_df.job_avg_salary).alias("job_avg_salary"))

    # 分析求职情况
    job_position_df = job_df.join(position_df, ["position_name", "address", "date_time"], how="inner")
    return job_position_df.select(columns)
