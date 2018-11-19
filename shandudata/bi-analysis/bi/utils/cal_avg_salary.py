# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""
from bi.settings import SALARY_MAX, SALARY_MIN


def cal_avg_salary(expect_salary_min, expect_salary_max, latest_salary_min=0, latest_salary_max=0):
    """
    计算每个人（每份简历）的平均薪资，当期望薪资没有值时用当前信息，如果都没有，则返回0
    :param expect_salary_min: 期望薪资最小值
    :type expect_salary_min: int
    :param expect_salary_max: 期望薪资最大值
    :type expect_salary_max: int
    :param latest_salary_min: 当前薪资最小值
    :type latest_salary_min: int
    :param latest_salary_max: 当前薪资最大值
    :type latest_salary_max: int
    :return: 平均薪资
    :rtype: int
    
    >>> cal_avg_salary(3000, 5000, 0, 0)
    4000.0
    >>> cal_avg_salary(0, 0, 3000, 5000)
    4000.0
    """
    avg_salary = 0
    try:
        expect_salary_min = int(expect_salary_min)
        expect_salary_max = int(expect_salary_max)
        latest_salary_min = int(latest_salary_min)
        latest_salary_max = int(latest_salary_max)
        if int(SALARY_MIN) < expect_salary_min <= expect_salary_max < int(SALARY_MAX):
            avg_salary = (expect_salary_min + expect_salary_max) / 2
        elif int(SALARY_MIN) < latest_salary_min <= latest_salary_max < int(SALARY_MAX):
            avg_salary = (latest_salary_min + latest_salary_max) / 2
    except Exception as e:
        print(str(e))

    return avg_salary
