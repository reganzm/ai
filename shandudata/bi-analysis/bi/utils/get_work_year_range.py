# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""


def get_work_year_range(work_year):
    """得到工作年限区间"""
    if work_year is None:
        return None
    if work_year < 1:
        work_year_str = "1年以下"
    elif work_year < 3:
        work_year_str = "1-3年"
    elif work_year < 5:
        work_year_str = "3-5年"
    elif work_year < 10:
        work_year_str = "5-10年"
    else:
        work_year_str = "10年以上"
    return work_year_str
