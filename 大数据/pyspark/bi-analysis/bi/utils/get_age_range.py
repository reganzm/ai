# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""


def get_age_range(age):
    if age is None:
        return None
    if age < 22:
        age_str = "22岁以下"
    elif age < 30:
        age_str = "22-30岁"
    elif age < 40:
        age_str = "30-40岁"
    else:
        age_str = "40岁以上"
    return age_str
