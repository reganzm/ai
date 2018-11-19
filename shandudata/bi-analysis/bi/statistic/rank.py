# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 24/08/2018 14:59
:File    : rank.py
"""

from bi.core.common import add_rank, statistic_groups, statistic_cube, add_total, statistic_dimension


def statistic_rank(df, mysql_url):
    """
    排名相关分析
    :param df:
    :param mysql_url:
    :return:
    """

    parameters = [
        (["major"], "degree", ("major__rank", None)),
        (["school_name"], "degree", ("school__rank", None)),
        (["school_name", "major"], "degree", ("school__major__rank", None, True, True)),
        (["school_name", "major"], "degree",
         ("school__major__position__rank", "position_name", True, True, '-person_num', True)),
        (["company_name"], None, ("company__rank", None)),
        (["industry"], None, ("industry__rank", None),),
        (["industry"], "address", ("industry__address__rank", None)),
        (["position_name"], None, ("position__rank", None)),
        (["position_name"], None, ("position__industry__rank", "industry", True, False, '-person_num',)),

        (["position_name"], "address", ("position__address__industry", "industry", False, True, '-person_num')),
    ]

    statistic_dimension(df, mysql_url, parameters, statistic_rank_dimension)


def statistic_rank_dimension(df, groups, na_field, fields, is_sa=True, is_cube=False, sort_field='-avg_salary',
                             need_total=False):
    """
    排名
    """
    na_field = [na_field] if na_field else []
    fields = [fields] if fields else []
    all_fields = groups + na_field + fields
    for field in all_fields:
        df = df.filter(df[field].isNotNull())

    if is_cube:
        md_df = statistic_cube(df, groups, na_field, fields, is_sa)
    else:
        md_df = statistic_groups(df, groups, na_field, fields, is_sa)

    if need_total:
        md_df = add_total(md_df, *(groups + na_field))

    if fields:
        md_df = add_rank(md_df, *(groups + na_field), sort_field=sort_field)
    else:
        md_df = add_rank(md_df, *(groups[1:] + na_field), sort_field=sort_field)

    return md_df
