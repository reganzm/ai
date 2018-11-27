# -*- coding: utf-8 -*-
"""
@Time    : 2018/9/9
@Author   : huanggangyu
"""

from bi.core.common import statistic_dimension, statistic_cube, statistic_groups


def statistic_number(df, mysql_url):
    """
    人数（权重）分析
    :param df:
    :param mysql_url:
    :return:
    """

    parameters = [
        (["company_name"], "position_category", ("company__salary", "salary_range")),
        (["company_name"], "position_category", ("company__gender", "gender")),
        (["company_name"], "position_category", ("company__address", "address")),
        (["company_name"], "position_category", ("company__school", "school_name")),
        (["company_name"], "position_category", ("company__major", "major")),
        (["company_name"], "position_category", ("company__degree", "degree")),

        (["industry"], None, ("industry__address", "address")),
        (["industry"], "address", ("industry__address__salary", "salary_range")),
        (["industry"], "address", ("industry__address__gender", "gender")),
        (["industry"], "address", ("industry__address__salary_work_year", "work_year_range,salary_range")),

        (["position_name"], None, ("position__address", "address")),
        (["position_name"], "address", ("position__address__salary_range", "salary_range")),
        (["position_name"], "address", ("position__address__age_range", "age_range")),
        (["position_name"], "address", ("position__address__salary_work_year", "work_year_range,salary_range")),

    ]

    statistic_dimension(df, mysql_url, parameters, statistic_number_dimension)


def statistic_number_dimension(df, groups, na_field, fields, is_sa=False, is_cube=False):
    """
    人数（权重）分析
    :param df:
    :return:
    """
    na_field = [na_field] if na_field else []
    fields = fields.split(',') if fields else []
    all_fields = groups + na_field + fields
    for f in all_fields:
        df = df.filter(df[f].isNotNull())
    if is_cube:
        md_df = statistic_cube(df, groups, na_field, fields, is_sa)
    else:
        md_df = statistic_groups(df, groups, na_field, fields, is_sa)

    return md_df
