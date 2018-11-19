# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 22/07/2018 16:55
:File    : education.py
"""

from __future__ import unicode_literals

import json

import codecs
from os.path import join

from settings import RESOURCES

SCHOOL_PATH = join(RESOURCES, "education/school_rank.json")
MAJOR_PATH = join(RESOURCES, "education/school_major_evaluation.json")

school_rank = {}
for line in codecs.open(SCHOOL_PATH, encoding="utf-8"):
    data = json.loads(line)
    data.pop("_id")
    school_name = data.pop("school_name")
    school_rank[school_name] = data

school_major_evaluation = json.load(codecs.open(MAJOR_PATH, encoding="utf-8"))

school_rank_map = {
    "1星级": 1,
    "2星级": 2,
    "3星级": 3,
    "4星级": 4,
    "5星级": 5,
    "6星级": 6,
    "7星级": 7,
    "8星级": 8,
}

major_evaluation_map = {
    "A+": -1,
    "A": -2,
    "A-": -3,
    "B+": -4,
    "B": -5,
    "B-": -6,
    "C+": -7,
    "C": -8,
    "C-": -9,
}


def education_score(school, major=None):
    """
    教育经历综合评分
    :param school: 学校名称
    :type school: str
    :param major: 专业名称
    :type major: str
    :return: 综合评分
    :rtype: int
    
    >>> education_score("清华大学")
    8
    >>> education_score("不存在学校")
    0
    >>> education_score("清华大学", "化学")
    17
    >>> education_score("北京大学", "戏剧与影视学")
    11
    >>> education_score("北京大学", "不存在专业")
    8
    """
    # 学校评分
    school_score = 0
    school_data = school_rank.get(school, None)
    if school_data:
        school_score = school_rank_map.get(school_data.get("star_rank"), 0)

    # 学校对应专业评分
    major_score = 0
    school_major = school_major_evaluation.get(school, None)
    if school_major:
        major_score = major_evaluation_map.get(school_major.get(major, None), -10) + 10

    mix_score = school_score + major_score
    return mix_score


if __name__ == "__main__":
    import doctest

    doctest.testmod()
