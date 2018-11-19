# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 24/08/2018 15:11
:File    : statistic_dimension.py
"""

from pyspark.sql import Window, functions as F

from bi.core.save_to_mysql import write_mysql
from bi.settings import LATEST_YEAR, MIN_NUM, MIN_SALARY, NA
from bi.core.common import add_median_salary


#
# def statistic_dimension(df, groups, salary=None, ranks=None):
#     if salary == "median":
#         statistic_median_salary(df, groups, ranks)
#     elif salary == "avg":
#         statistic_avg_salary(df, groups, ranks)
#     else:
#         statistic(df, groups, ranks)


def statistic(df, groups, is_rank=False):
    mdf = df.cube(groups).agg(F.count("*").alias("person_num"))
    mdf = mdf.dropna(how="all", subset=groups[-1:])
    for field in groups[:-1]:
        mdf = mdf.withColumn(field, F.lit(NA))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    return add_rank(mdf, groups, is_rank)


def statistic_avg_salary(df, groups, is_rank=False):
    mdf = df.cube(groups).agg(F.count("*").alias("person_num"), F.avg("avg_salary").alias("avg_salary"))
    mdf = mdf.dropna(how="all", subset=groups[-1:])
    for field in groups[:-1]:
        mdf = mdf.withColumn(field, F.lit(NA))
    return add_rank(mdf, groups, is_rank)


def statistic_median_salary(df, groups, is_rank=False):
    df = add_median_salary(df, groups, sort_field="avg_salary")
    # 分组分析
    median_df = df.groupby(groups).agg(F.count("*").alias("person_num"), F.first("avg_salary").alias("avg_salary"))
    # 分组分析，学历不限
    median_one_df = df.groupby(groups[:-1]).agg(F.count("*").alias("person_num"),
                                                F.avg("avg_salary").alias("avg_salary"))
    median_one_df = median_one_df.withColumn(groups[-1], F.lit(NA))

    median_df = median_df.unionByName(median_one_df)
    return add_rank(median_df, groups, is_rank)


def add_rank(df, groups, is_rank, sort_field="-avg_salary"):
    """
    添加排序字段， 默认是以薪资逆序排列 
    """
    if is_rank:
        sort = F.col(sort_field[1:]).desc() if sort_field.startswith("-") else F.col(sort_field)
        salary_rank_spec = Window.partitionBy(groups[:-1]).orderBy(sort)
        df = df.withColumn("rank", F.row_number().over(salary_rank_spec))
    return df


def statistic_dimension(df, mysql_url):
    # 薪资类型(salary category)
    common = statistic
    median = statistic_median_salary
    avg = statistic_avg_salary
    parameters = [
        # 专业维度相关分析
        (["major", "degree"], [
            ("major__rank", None, median),
            ("major__gender", "gender", median),
            ("major__address", "address", median),
            ("major__company", "company_name", median),
            ("major__industry", "industry", median),
            ("major__position", "position_name", median),
        ]),

        # ("major__rank", ["major", "degree"], sc, True),
        # ("major__gender", ["major", "degree","gender"], sc),
        # ("major__address", ["major", "degree","address"], sc),
        # ("major__company", ["major", "degree", "company_name"], sc),
        # ("major__industry", ["major", "degree", "industry"], sc),
        # ("major__position", ["major", "degree","position_name"], sc),
        #
        # # 学校维度相关分析
        # ("school__rank", ["school_name", "degree"], sc, True),
        # ("school__gender", ["school_name", "degree", "gender"], sc),
        # ("school__address", ["school_name", "degree", "address"], sc),
        # ("school__company", ["school_name", "degree", "company_name"], sc),
        # ("school__industry", ["school_name", "degree", "industry"], sc),
        # ("school__position", ["school_name", "degree", "position_name"], sc),
        #
        # # 学校 + 专业  相关维度的分析
        # ("school__major__rank", ["school_name", "major", "degree"], sc, True),
        # ("school__major__position", ["school_name", "major", "degree", "position_name"], sc),
        # ("school__major__industry", ["school_name", "major", "degree", "industry"], sc),
        # ("school__major__company", ["school_name", "major", "degree", "company_name"], sc),
        # ("school__major__flow", ["school_name", "major", "degree", "company_name", "industry"], sc),
        # ("school__major__position__rank", ["school_name", "major", "degree", "position_name"], sc, True),

    ]

    for groups, values in parameters:
        result_tables = dict()
        mdf = df
        for field in groups:
            mdf = df.filter(df[field].isNotNull())
        mdf.persist()
        for table, result_field, func in values:
            if not result_field:
                result_field = []
            if isinstance(result_field, str):
                result_field = [result_field]
                result_df = mdf.filter(mdf[result_field].isNotNull())
                fields = groups + [result_field]
            result_tables[table] = func(result_df, fields, "rank" in table)
        write_mysql(mysql_url, result_tables)
        mdf.unpersist()


if __name__ == "__main__":
    statistic_dimension()
