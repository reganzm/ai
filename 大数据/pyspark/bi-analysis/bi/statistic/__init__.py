# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

from bi.statistic.postgraduate import postgraduate
from bi.statistic.job import statistic_job
from bi.statistic.graduate_first_work import statistic_graduate_first_work
from bi.statistic.graduate_all_work import statistic_graduate_all_work
from bi.statistic.history import history_analysis
from bi.statistic.major_position_relation import statistic_major_position

__all__ = [
    # 学校+专业+深造相关维度统计
    "postgraduate",
    # 学校+专业+深造相关维度统计
    "statistic_job",
    "statistic_graduate_first_work",
    "statistic_graduate_all_work",
    "history_analysis",
    "statistic_major_position",
]
