# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 24/08/2018 14:59
:File    : rank.py
"""

from pyspark.sql import Window, functions as F
from bi.core.common import sort, statistic_groups, statistic_dimension
from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_SALARY, NA, MIN_NUM, MIN_AGE
from bi.core.common import sort, statistic_cube, add_rank, filter_cube_num
from pyspark.sql import functions as F, Window
from bi.utils.filter import filter_invalid_value


def statistic_neighbour(df, mysql_url):
    """
    当前职位（公司）的上（下）一份职位（公司）分布
    :param df: 
    :param mysql_url: 
    :return: 
    """

    parameters = [
        (["company_name"], "position_category", ("company__prev_company", "prev_company")),
        (["company_name"], "position_category", ("company__next_company", "next_company")),
        (["position_name"], "address", ("position__address__prev_position", "prev_position")),
        (["position_name"], "address", ("position__address__next_position", "next_position")),
    ]

    statistic_dimension(df, mysql_url, parameters, statistic_neighbour_dimension)

    statistic_neighbour_special(df, mysql_url)


def statistic_neighbour_dimension(df, groups, na_field, fields, is_sa=False):
    """
    前后相邻值分析
    :param df: 
    :return: 
    """
    na_field = [na_field] if na_field else []
    fields = [fields] if fields else []
    all_fields = groups + na_field + fields
    df = df.select(all_fields[0], all_fields[1], "resume_id", "work_index")
    df = add_prev_or_next(df, groups[0], fields[0])
    for f in all_fields:
        df = df.filter(df[f].isNotNull())
    md_df = statistic_groups(df, groups, na_field, fields, is_sa, filter_num=True)
    return md_df


def add_prev_or_next(df, old_field, new_field, partition_field='resume_id', sort_field='-work_index'):
    """为某一字段的每一行添加其前一个或后一个值"""
    window_spec = Window.partitionBy(partition_field).orderBy(sort(sort_field))
    if 'prev' in new_field:
        # 取前一行
        df = df.withColumn(new_field, F.lag(df[old_field], 1).over(window_spec))
    elif 'next' in new_field:
        # 取后一行
        df = df.withColumn(new_field, F.lead(df[old_field], 1).over(window_spec))
    # 过滤掉相同的或为空的
    df = df.filter(df[old_field] != df[new_field]).filter(df[new_field].isNotNull())
    # df = df.filter(df[new_field].isNotNull())

    return df


def statistic_neighbour_special(df, mysql_url):
    config = {
        "address_change": [
            (["position_name"], "address", ("position__address__change", None)),
        ]
    }

    # 当前工作的最小薪资必须大于MIN_SALARY, 且区间最大值大于最小值
    df = df.filter((df.salary_min > MIN_SALARY)).filter(df.salary_max >= df.salary_min)
    for type, parameters in config.items():
        result_tables = dict()
        df.persist()
        for groups, na_field, values in parameters:
            result_df = statistic_position_address_change(df, groups, na_field, *values[1:])
            # 过滤掉某些字段中的不合法值
            result_tables[values[0]] = filter_invalid_value(result_df)
        write_mysql(mysql_url, result_tables)
        df.unpersist()


def statistic_position_address_change(df, groups, na_field, fields, is_sa=False):
    """
    职位延续性分析
    :param df:
    :return:
    """
    na_field = [na_field] if na_field else []
    fields = [fields] if fields else []
    all_fields = groups + na_field + fields
    df = df.select(all_fields[0], all_fields[1], "resume_id", "work_index")

    df = next_same(df, groups[0])
    md_df = statistic_cube(df, groups, na_field, fields, is_sa)
    md_df = add_rank(md_df, *(groups[1:] + na_field), sort_field='-person_num')
    return md_df


def next_same(df, field, partition_field='resume_id', sort_field='-work_index'):
    """获取 下一个值与当前行该字段的值相等的数据 """
    window_spec = Window.partitionBy(partition_field).orderBy(sort(sort_field))
    new_field = f"next_{field}"
    df = df.withColumn(new_field, F.lead(df[field], 1).over(window_spec))
    # 过滤掉不同的或为空
    df = df.filter(df[field] == df[new_field]).filter(df[new_field].isNotNull())
    df = df.drop(new_field)
    return df
