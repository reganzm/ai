# -*- coding: utf-8 -*-
"""
@Time    : 2018/9/11
@Author   : huanggangyu
"""

from bi.core.save_to_mysql import write_mysql
from bi.settings import MIN_SALARY, NA, MIN_NUM, MIN_AGE
from bi.core.common import sort, statistic_cube, add_rank, filter_cube_num
from pyspark.sql import functions as F, Window
from bi.utils.filter import filter_invalid_value


def statistic_special(df, mysql_url):
    """
    特殊情况分析
    :param df:
    :param mysql_url:
    :return:
    """

    config = {
        "company__age": [
            (["company_name"], "position_category", ("company__age", None, False, True)),
        ],
        "company__duration": [
            (["company_name"], "position_category", ("company__duration", None)),
        ],
        "position__address__duration": [
            (["position_name"], "address", ("position__address__duration", None, False, True))
        ],
        "address__flow": [
            (["industry"], None, ("industry__address__flow", "address,expect_area")),
            (["position_name"], None, ("position__address__flow", "address,expect_area"))
        ],
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
            if type == 'company__age':
                result_df = statistic_company_age(df)
            elif type == 'company__duration':
                result_df = statistic_company_duration(df)
            elif type == 'position__address__duration':
                result_df = statistic_position_address_duration(df)
            elif type == 'address__flow':
                result_df = statistic_address_flow(df, groups, na_field, *values[1:])
            # 过滤掉某些字段中的不合法值
            result_tables[values[0]] = filter_invalid_value(result_df)
        write_mysql(mysql_url, result_tables)
        df.unpersist()


def statistic_company_age(df):
    """
    公司对应年龄分布
    :param df:
    :return:
    """
    df = df.filter(df.age >= MIN_AGE)
    df = filter_cube_num(df, "company_name", "position_category")
    mdf = df.cube("company_name", "position_category").agg(F.count("*").alias("person_num"),
                                                           F.avg(df.age).alias("avg_age"))
    mdf = mdf.fillna(NA)
    return mdf


def statistic_company_duration(df):
    """
    当前工作的工作时长（年）
    :param df:
    :return:
    """
    df = df.filter(df.work_duration_year.isNotNull()).filter(df.company_name.isNotNull()).filter(
        df.position_category.isNotNull())
    df = df.filter(df.age >= MIN_AGE)
    df = df.withColumn('avg_duration', df.work_duration_year)
    mdf = df.groupby("company_name", "position_category").agg(F.count("*").alias("person_num"),
                                                              F.avg("avg_duration").alias("avg_duration"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    sdf = mdf.groupby("company_name").agg(F.sum("person_num").alias("person_num"),
                                          F.avg("avg_duration").alias("avg_duration"))
    sdf = sdf.withColumn("position_category", F.lit(NA))
    mdf = mdf.unionByName(sdf)
    return mdf


def statistic_position_address_duration(df):
    """
    职位+地点对应单次在职时长
    :param df:
    :return:
    """
    df = df.filter(df.work_duration_month.isNotNull()).filter(df.work_duration_month > 0) \
        .filter(df.work_duration_month < 240).filter(df.position_name.isNotNull()).filter(df.address.isNotNull())
    df = df.withColumn('avg_duration', df.work_duration_month)

    df = filter_cube_num(df, "position_name", "address")
    md_df = df.cube("position_name", "address").agg(F.count("*").alias("person_num"),
                                                    F.avg(df.avg_duration).alias("avg_duration"))
    md_df = md_df.filter(md_df["position_name"].isNotNull())
    md_df = md_df.fillna(NA)

    md_df = add_rank(md_df, "address", sort_field='-avg_duration')
    return md_df


def statistic_address_flow(df, groups, na_field, field):
    """
    地点对应地区人才流动
    :param df:
    :return:
    """
    na_field = [na_field] if na_field else []
    fields = field.split(',') if field else []
    all_fields = groups + na_field + fields
    for field in all_fields:
        df = df.filter(df[field].isNotNull())

    mdf = df.select(groups[0], "address",
                    F.explode(F.split(df.expect_area, ",")).alias("expect_area"))
    mdf = mdf.groupby(groups[0], "address", "expect_area").agg(F.count("*").alias("person_num"))
    mdf = mdf.filter(mdf.person_num > MIN_NUM)
    return mdf



