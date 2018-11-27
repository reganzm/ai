# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 21/08/2018 15:05
:File    : flat_work_year.py
"""

import datetime

from pyspark.sql import Window, functions as F
from pyspark.sql.types import *

from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_SALARY, NA, MIN_NUM
from bi.utils.flat_work_year_salary import flat_work_year_salary
from bi.utils.get_years import get_work_year
from bi.core.common import add_median_salary

CURRENT_YEAR = datetime.datetime.now().year

work_year_schema = StructType([
    StructField("work_year", IntegerType()),
    StructField("salary", IntegerType())
])


def flat_work_year(df):
    # 最近5年毕业的人才
    # df = df.filter(df.edu_end_year >= CURRENT_YEAR - 5)
    # 当前工作的最小薪资必须大于MIN_SALARY, 且区间最大值大于最小值
    df = df.filter((df.salary_min > MIN_SALARY)).filter(df.salary_max >= df.salary_min) \
        .filter(df.avg_salary.isNotNull())
    # 计算毕业到现在的工作时长
    df = df.withColumn("work_month_min", F.months_between(df.work_start_date, df.edu_end_date))
    df = df.withColumn("work_month_max", F.months_between(df.work_end_date, df.edu_end_date))
    df = df.withColumn("work_month_duration", F.months_between(df.work_end_date, df.work_start_date))
    # 将工作月份转换成年数
    df = df.withColumn("work_year_min", F.udf(get_work_year, IntegerType())(df.work_month_min))
    df = df.withColumn("work_year_max", F.udf(get_work_year, IntegerType())(df.work_month_max))
    # 第一份工作入职时间在毕业5年内（0-1.5年都归为1年），工作时长大于0且小于10年
    df = df.filter(df.work_year_min > 0).filter(df.work_year_min <= 5) \
        .filter(df.work_month_duration >= 0).filter(df.work_month_duration < 120)
    # 将薪资摊平到工作年限上
    df = df.withColumn("work_years", F.udf(flat_work_year_salary, ArrayType(work_year_schema))(
        df.work_year_min, df.work_year_max,
        df.salary_min, df.salary_max))
    # 工作年限对应薪资
    df = df.withColumn("work_years", F.explode(df.work_years))
    df = df.withColumn("work_year", F.col("work_years")["work_year"]) \
        .withColumn("avg_salary", F.col("work_years")["salary"])
    return df


def statistic_work_year(df, mysql_url):
    df = flat_work_year(df)
    df.persist()
    result_tables = dict()
    parameters = [
        {"name": "major__work_year", "groups": ["major", "work_year", "degree"]},
        {"name": "school__work_year", "groups": ["school_name", "work_year", "degree"]},
        {"name": "company__work_year", "groups": ["company_name", "work_year", "position_category"]},
        {"name": "industry__address__work_year", "groups": ["industry", "work_year", "address"]},
        {"name": "position__address__work_year", "groups": ["position_name", "work_year", "address"]},
        {"name": "school__major__work_year", "groups": ["school_name", "major", "work_year", "degree"]},
    ]
    for param in parameters:
        result_tables[param["name"]] = statistic_work_year_dimension(df, param["groups"])

    write_mysql(mysql_url, result_tables)
    df.unpersist()


def statistic_work_year_dimension(df, groups):
    """
    各维度对应的年限分布和薪资情况, 薪资为中位数薪资
    :param df: 
    :param groups
    :return: 
    """
    # 按薪资，百分比排序
    for field in groups[:-2]:
        df = df.filter(df[field].isNotNull())
    df = df.filter(df[groups[-1]].isNotNull())
    # 添加中位数薪资
    df = add_median_salary(df, groups, sort_field="avg_salary")
    # 分组分析
    median_df = df.groupby(groups).agg(F.count("*").alias("person_num"), F.first("avg_salary").alias("avg_salary"))

    median_df = median_df.filter(median_df.person_num > MIN_NUM)
    # 分组分析，学历不限
    median_one_df = median_df.groupby(groups[:-1]).agg(F.sum("person_num").alias("person_num"),
                                                       F.avg("avg_salary").alias("avg_salary"))
    median_one_df = median_one_df.withColumn(groups[-1], F.lit(NA))

    median_df = median_df.unionByName(median_one_df)
    return median_df
