# -*- coding: utf-8 -*-
"""
@Time    : 2018/9/12
@Author   : huanggangyu
"""
invalid_value = {
    "company": [
        "达内"
    ],
    "school_name": [
        "达内"
    ],
}


def filter_invalid_value(df):
    """过滤掉dataframe中的含有不合法值的记录"""
    fields = df.columns
    for key, values in invalid_value.items():
        invalid_fields = []
        for field in fields:
            if key in field:
                invalid_fields.append(field)
        for field in invalid_fields:
            for value in values:
                df = df.filter(~ df[field].contains(value))
    return df
