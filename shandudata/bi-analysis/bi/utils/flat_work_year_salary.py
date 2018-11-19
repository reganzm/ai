# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 21/08/2018 17:38
:File    : flat_work_year_salary.py
"""


def flat_work_year_salary(work_year_min, work_year_max, salary_min, salary_max):
    """
    将工作年限区间和薪资区间扁平对应
    :param work_year_min: 工作年限最小值
    :type work_year_min: int
    :param work_year_max: 工作年限最大值
    :type work_year_max: int
    :param salary_min: 薪资最小值
    :type salary_min: int
    :param salary_max: 薪资最大值
    :type salary_max: int
    :return: 字典列表
    :rtype: list

    >>> flat_work_year_salary(1, 1, 6000, 8000)
    [{'work_year': 1, 'salary': 7000}]
    >>> flat_work_year_salary(1, 2, 6000, 8000)
    [{'work_year': 1, 'salary': 6667}, {'work_year': 2, 'salary': 7334}]
    >>> flat_work_year_salary(1, 3, 6000, 8000)
    [{'work_year': 1, 'salary': 6500}, {'work_year': 2, 'salary': 7000}, {'work_year': 3, 'salary': 7500}]
    >>> flat_work_year_salary(3, 6, 6000, 8000)
    [{'work_year': 3, 'salary': 6400}, {'work_year': 4, 'salary': 6800}, {'work_year': 5, 'salary': 7200}]
    >>> flat_work_year_salary(4, 5, 6000, 8000)
    [{'work_year': 4, 'salary': 6667}, {'work_year': 5, 'salary': 7334}]
    >>> flat_work_year_salary(5, 3, 6000, 8000)
    []
    >>> flat_work_year_salary(1, 3, 8000, 6000)
    []
    """
    results = []
    if work_year_max < work_year_min or salary_max < salary_min:
        return results
    val = work_year_max - work_year_min + 2
    sub_salary = salary_max - salary_min
    sa = round(sub_salary / val)
    max_num = work_year_max if work_year_max <= 5 else 5
    for work_year in range(work_year_min, max_num + 1):
        salary_min += sa
        results.append({
            "work_year": work_year,
            "salary": salary_min
        })
    return results
