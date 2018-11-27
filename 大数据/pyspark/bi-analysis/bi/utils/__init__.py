# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

from bi.utils.cal_avg_salary import cal_avg_salary
from bi.utils.get_years import get_years, get_year
from bi.utils.get_age_range import get_age_range
from bi.utils.get_salary_range import get_salary_range
from bi.utils.get_work_year_range import get_work_year_range
from bi.utils.filter import filter_invalid_value

__all__ = [
    # 计算平均薪资
    "cal_avg_salary",
    # 根据月数计算年
    "get_year",
    "get_years",
    # 得到薪资区间
    "get_salary_range",
    # 得到年龄区间
    "get_age_range",
    # 得到工作年限钱
    "get_work_year_range",
    # 过滤掉某个字段中的不合法值
    "filter_invalid_value",
]
