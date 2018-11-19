# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""


def get_salary_range(salary):
    """"""
    if salary is None:
        return None
    if salary < 5000:
        salary_str = "5k以下"
    elif salary < 8000:
        salary_str = "5-8K"
    elif salary < 10000:
        salary_str = "8-10k"
    elif salary < 15000:
        salary_str = "10-15k"
    elif salary < 25000:
        salary_str = "15-25k"
    else:
        salary_str = "25k以上"
    return salary_str
