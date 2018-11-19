# -*- coding: utf-8 -*-
"""
@Time    : 2018/9/22
@Author   : huanggangyu
"""

from bi.core.common import statistic_dimension, statistic_cube, statistic_groups


def statistic_major_position(profile_df, education_df, work_df, mysql_url):
    """
    专业对口职位统计
    :param df:
    :param mysql_url:
    :return:
    """
    # 最后一份教育经历
    latest_education_df = education_df.filter(education_df.edu_index == 1).filter(education_df.school_area == "中国")
    resume_df = profile_df.join(latest_education_df, "resume_id").join(work_df, "resume_id")
    # 第一份工作经历
    first_work_df = resume_df.filter(resume_df.work_index == resume_df.work_len)

    parameters = [
        (["major"], "degree", ("major__position__relation", "position_name")),
    ]

    statistic_dimension(first_work_df, mysql_url, parameters, statistic_number_dimension)


def statistic_number_dimension(df, groups, na_field, fields, is_sa=False, is_cube=False):
    """
    人数（权重）分析
    :param df:
    :return:
    """
    na_field = [na_field] if na_field else []
    fields = fields.split(',') if fields else []
    all_fields = groups + na_field + fields
    for f in all_fields:
        df = df.filter(df[f].isNotNull())
    if is_cube:
        md_df = statistic_cube(df, groups, na_field, fields, is_sa)
    else:
        md_df = statistic_groups(df, groups, na_field, fields, is_sa)

    return md_df
