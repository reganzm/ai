# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""


def get_years(months):
    """
    将月数转换成年, 假定大学四年，在上大学之前就在工作的人
    :param months: 
    :return: 
    """
    if months:
        years = months / 12
        if years > 0:
            years = round(years)
        elif years > -4:
            years = 0
        else:
            years = -1
    else:
        years = -1
    return years


def get_year(months, is_int=False):
    year = -1
    if months:
        year = months / 12

    if is_int:
        year = round(year)

    return year


def get_work_year(months):
    """
    将工作月份转换成工作年份,
    :param months: 工作月数
    :type months: int
    :return: 年数
    :rtype: int
    """
    years = -1

    if months:
        year = months / 12
        if 0.0 <= year < 1.5:
            years = 1
        else:
            years = round(year)

    return years
