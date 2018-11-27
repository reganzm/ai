# -*- coding: utf-8 -*-
"""
@Time    : 2018/9/20
@Author   : huanggangyu
"""
from bi.statistic.major import statistic_major
from bi.statistic.school import statistic_school
from bi.statistic.company import statistic_company
from bi.statistic.industry import statistic_industry
from bi.statistic.position import statistic_position
from bi.statistic.industry_address import statistic_industry_address
from bi.statistic.position_address import statistic_position_address
from bi.statistic.school_major import statistic_school_major
from bi.statistic.person import statistic_person


def history_analysis(first_work_df, mysql_url):
    # 各维度的统计分析
    statistic_major(first_work_df, mysql_url)
    statistic_school(first_work_df, mysql_url)
    statistic_company(first_work_df, mysql_url)
    statistic_industry(first_work_df, mysql_url)
    statistic_industry_address(first_work_df, mysql_url)
    statistic_position(first_work_df, mysql_url)
    statistic_position_address(first_work_df, mysql_url)
    statistic_school_major(first_work_df, mysql_url)
    statistic_person(first_work_df, mysql_url)