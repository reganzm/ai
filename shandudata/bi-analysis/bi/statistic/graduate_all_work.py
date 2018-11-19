# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 26/08/2018 23:11
:File    : graduate_all_work.py
"""
from bi.statistic.neighbour import statistic_neighbour
from bi.statistic.work_year import statistic_work_year

def statistic_graduate_all_work(df, mysql_url):
    """毕业后多份工作分析"""
    # 薪酬随年限增长趋势分析
    statistic_work_year(df, mysql_url)
    # 相邻工作经历分析
    statistic_neighbour(df, mysql_url)