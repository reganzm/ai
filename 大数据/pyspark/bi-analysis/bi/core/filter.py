# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

from functools import wraps

from pyspark.sql import functions as F

from bi.settings import *


def filter_count(df, alias, *cols):
    df = df.groupby(*cols).agg(F.count("*").alias(alias))
    return df.filter(df[alias] > MIN_NUM)


def filter_salary(df, col="avg_salary"):
    return df.filter(df[col] > MIN_SALARY)


def filter_str(df, col, filter_null=True, limit_length=True):
    if filter_null:
        df = df.filter(df[col].isNotNull() & (~ df[col].endswith("\s*")))
    if limit_length:
        df = df.filter(F.length(df[col]) < MAX_LENGTH).filter(F.length(df[col]) > MIN_LENGTH)
    return df


def filter_age(df, col="age"):
    return df.filter(df[col] >= MIN_AGE).filter(df[col] <= MAX_AGE)


def filter_address(df, col="address", max_length=20):
    return df.filter(df[col].isNotNull()) \
        .filter(F.length(df[col]) < max_length).filter(F.length(df[col]) > MIN_LENGTH).filter(df[col] != NA)


def filter_min(func):
    @wraps(func)
    def __filter_min(df):
        df = func(df)
        df = df.filter(df.person_num > MIN_NUM)
        return df

    return __filter_min


def filter_cube_num(df, *groups):
    """cube分析前过滤掉样本少的数据"""
    cdf = df.groupby(*groups).agg(F.count("*").alias("person_num"))
    cdf = cdf.filter(cdf.person_num > MIN_NUM)
    cdf = df.join(cdf, on=list(groups), how='inner')
    return cdf