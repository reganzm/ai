# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 21/08/2018 09:38
:File    : median.py
"""

from pyspark.sql import Window, functions as F
from bi.settings import MIN_NUM, NA, MIN_SALARY
from bi.core.save_to_mysql import write_mysql
from bi.core.filter import filter_cube_num
from bi.utils.filter import filter_invalid_value


def statistic_dimension(df, mysql_url, parameters, func):
    """各维度简历数据分析"""
    # 当前工作的最小薪资必须大于MIN_SALARY, 且区间最大值大于最小值
    df = df.filter((df.salary_min > MIN_SALARY)).filter(df.salary_max >= df.salary_min) \
        .filter(df.avg_salary.isNotNull())
    result_tables = dict()
    df.persist()
    for groups, na_field, values in parameters:
        result_tables[values[0]] = func(df, groups, na_field, *values[1:])
    write_mysql(mysql_url, result_tables)
    df.unpersist()


def sort(sort_field):
    return F.col(sort_field[1:]).desc() if sort_field.startswith("-") else F.col(sort_field)


def add_median_salary(df, *groups, sort_field="-avg_salary"):
    window = Window.partitionBy(*groups)
    rank_spec = window.orderBy(sort(sort_field))
    df = df.withColumn("percent_rank", F.percent_rank().over(rank_spec))
    # 按中位数排序
    median_spec = window.orderBy(F.pow(df.percent_rank - 0.5, 2))
    df = df.withColumn("avg_salary", F.first("avg_salary").over(median_spec))
    return df


def add_rank(df, *groups, sort_field="-avg_salary"):
    """
    添加排序字段， 默认是以薪资逆序排列 
    """
    rank_spec = Window.partitionBy(*groups).orderBy(sort(sort_field))
    df = df.withColumn("rank", F.row_number().over(rank_spec))
    return df


def add_total(df, *groups, sum_field="person_num"):
    """
    添加total字段， 默认是人数求和
    """
    win_spec = Window.partitionBy(*groups)
    df = df.withColumn("total", F.sum(sum_field).over(win_spec))
    return df


def statistic_cube(df, groups, na_field, fields, is_sa=True, filter_num=True):
    """
    cube分析
    """
    all_fields = groups + na_field + fields
    # 过滤掉样本少的数据
    if filter_num:
        all_df = filter_cube_num(df, *all_fields)

    if is_sa:
        all_df = add_median_salary(all_df, *all_fields)
        cube_df = all_df.cube(*all_fields).agg(F.count("*").alias("person_num"),
                                               F.avg("avg_salary").alias("avg_salary"))
    else:
        cube_df = all_df.cube(*all_fields).agg(F.count("*").alias("person_num"))

    # 不能同时为空
    if fields:
        cube_df = cube_df.dropna(how="all", subset=fields)

    # 均不能为空
    # for field in fields:
    #     cube_df = cube_df.filter(cube_df[field].isNotNull())

    cube_df = cube_df.dropna(how="all", subset=groups + na_field)
    cube_df = cube_df.fillna(NA)
    return cube_df


def statistic_groups(df, groups, na_field, fields, is_sa=True, filter_num=True):
    """
    group分析
    """
    all_fields = groups + na_field + fields
    if is_sa:
        df = add_median_salary(df, *all_fields)
        all_df = df.groupby(*all_fields).agg(F.count("*").alias("person_num"),
                                             F.first("avg_salary").alias("avg_salary"))
        # 过滤掉样本少的数据
        if filter_num:
            all_df = all_df.filter(all_df.person_num > MIN_NUM)
        if na_field:
            na_df = all_df.groupby(groups + fields).agg(F.sum("person_num").alias("person_num"),
                                                        F.avg("avg_salary").alias("avg_salary"))
            na_df = na_df.withColumn(na_field[0], F.lit(NA))
            all_df = all_df.unionByName(na_df)
    else:
        all_df = df.groupby(all_fields).agg(F.count("*").alias("person_num"))
        # 过滤掉样本少的数据
        if filter_num:
            all_df = all_df.filter(all_df.person_num > MIN_NUM)
        if na_field:
            na_df = all_df.groupby(groups + fields).agg(F.sum("person_num").alias("person_num"))
            na_df = na_df.withColumn(na_field[0], F.lit(NA))
            all_df = all_df.unionByName(na_df)
    return all_df
