# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

import datetime
from dateutil.parser import parse


def date_standard(date, fm="%Y-%m"):
    """
    将不同格式的日期标准化成统一格式
    :param date: 
    :param fm: 日期格式
    :return: 
    
    >>> date_standard("2018.07")
    '2018-07'
    >>> date_standard("2018.7")
    '2018-07'
    >>> date_standard("2017-06-01")
    '2017-06'
    >>> date_standard("2017-6-1")
    '2017-06'
    >>> date_standard("2018/5")
    '2018-05'
    >>> date_standard("2018/05")
    '2018-05'
    """
    try:
        date = date.replace(".", "-")
        return parse(date).strftime(fm)
    except:
        return None


def date_to_year(date):
    """
    将日期转换为日期对应的那一年
    :param date: 日期
    :return: 
    
    >>> date_to_year("2018.07")
    '2018'
    >>> date_to_year("2018.7")
    '2018'
    >>> date_to_year("2017-06-01")
    '2017'
    >>> date_to_year("2017-6-1")
    '2017'
    >>> date_to_year("2018/5")
    '2018'
    >>> date_to_year("2018/05")
    '2018'
    """
    try:
        date = date.replace(".", "-")
        return parse(date).strftime("%Y")
    except:
        return None


def get_duration_month(start_time, end_time):
    """
    计算两个日期之间持续的月数
    :param start_time: 开始日期
    :param end_time: 结束日期
    :return: 返回之间相差的月数
    
    >>> get_duration_month("2017-9", "2018-04")
    7
    """
    start_time = date_standard(start_time)
    end_time = date_standard(end_time)
    duration_month = 0
    if start_time and end_time:
        start_date = parse(start_time)
        end_date = parse(end_time)
        years = end_date.year - start_date.year
        months = end_date.month - start_date.month
        duration_month = years * 12 + months
    return duration_month
