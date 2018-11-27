# -*- coding: utf-8 -*-
"""
@Time    : 2018/9/9
@Author   : huanggangyu
"""

from bi.core.common import statistic_cube, statistic_groups, statistic_dimension
from pyspark.sql import functions as F
from bi.core.filter import filter_age
from bi.core.alias import get_position_alias, get_position_industry


def statistic_salary(df, mysql_url):
    """
    薪资分析
    :param df:
    :param mysql_url:
    :return:
    """

    parameters = [
        # 专业维度相关分析
        (["major"], "degree", ("major__gender", "gender")),
        (["major"], "degree", ("major__address", "address")),
        (["major"], "degree", ("major__company", "company_name")),
        (["major"], "degree", ("major__industry", "industry")),

        # 学校维度相关分析
        (["school_name"], "degree", ("school__gender", "gender")),
        (["school_name"], "degree", ("school__address", "address")),
        (["school_name"], "degree", ("school__company", "company_name")),
        (["school_name"], "degree", ("school__industry", "industry")),

        # 学校 + 专业  相关维度的分析
        (["school_name", "major"], "degree", ("school__major__position", "position_name", True, True)),
        (["school_name", "major"], "degree", ("school__major__industry", "industry", True, True)),
        (["school_name", "major"], "degree", ("school__major__company", "company_name", True, True)),
        (["school_name", "major"], "degree", ("school__major__flow", "company_name,industry", True, True)),

        (["industry"], "address", ("industry__address__compare", None, True, True)),
        (["industry"], "address", ("industry__address__age", "age_range")),
        (["industry"], "address", ("industry__address__degree", "degree")),

        # 职位 + 地点 相关维度分析
        (["position_name"], "address", ("position__address__compare", None, True, True)),
        (["position_name"], "address", ("position__address__gender", "gender")),
        (["position_name"], "address", ("position__address__work_year_range", "work_year_range")),
        (["position_name"], "address", ("position__address__degree", "degree")),
        (["address"], "gender", ("person__rank", "age", True, True, True)),

        # 含职位别名
        (["major"], "degree", ("major__position", "position_name", True, False, False, True)),
        (["school_name"], "degree", ("school__position", "position_name", True, False, False, True))
    ]

    statistic_dimension(df, mysql_url, parameters, statistic_salary_dimension)


def statistic_salary_dimension(df, groups, na_field, fields, is_sa=True, is_cube=False, is_age=False, need_alias=False):
    """
    薪资分析
    :param df:
    :return:
    """
    na_field = [na_field] if na_field else []
    fields = fields.split(',') if fields else []
    all_fields = groups + na_field + fields
    for f in all_fields:
        df = df.filter(df[f].isNotNull())
    if is_age:
        df = filter_age(df).withColumn("age", F.udf(str)(df.age))
    if is_cube:
        md_df = statistic_cube(df, groups, na_field, fields, is_sa)
    else:
        md_df = statistic_groups(df, groups, na_field, fields, is_sa)

    if need_alias:
        md_df = md_df.join(get_position_industry(df), "position_name")
        md_df = md_df.join(get_position_alias(df), "position_name")
    return md_df
