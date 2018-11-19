# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 26/08/2018 22:53
:File    : graduate.py
"""

from bi.statistic.rank import statistic_rank

from bi.statistic.number import statistic_number
from bi.statistic.salary import statistic_salary
from bi.statistic.special import statistic_special


def statistic_graduate_first_work(df, mysql_url):
    """毕业后第一份工作分析"""
    # 排名分析
    statistic_rank(df, mysql_url)
    # 薪酬分析
    statistic_salary(df, mysql_url)
    # 人数（权重）分析
    statistic_number(df, mysql_url)
    # 特殊情况分析
    statistic_special(df, mysql_url)
