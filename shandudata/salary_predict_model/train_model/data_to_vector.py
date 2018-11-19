# coding:utf-8
'''
Created on 2014年12月26日

@author: likaiguo
'''
import pandas as pd

from global_values import feature_columns_dict
from pre_mark_job_title import job_cate_tree


def map_work_len(work_len):
    """
    @summary: 将工作年限进行归约
    """
    try:
        work_len = int(work_len)
    except:
        work_len = 10

    if work_len <= 1:
        work_len = 1
    elif work_len <= 3:
        work_len = 3
    elif work_len <= 5:
        work_len = 5
    else:
        work_len = 10

    return work_len


def data_to_numuber(data_all_marked_position_title,
                    feature_columns=[
                        'city', 'degree',
                        'gender', 'school_level', 'first_class',
                        #             '2nd_class',
                        #             '3rd_class',
                    ]):
    """
    @summary: 将文本特征矢量化
    """
    data_all_feature_numeric_pd = pd.DataFrame()
    columns = data_all_marked_position_title.columns

    for feature in columns:
        if 'class' in feature:
            data_all_feature_numeric_pd[feature] = data_all_marked_position_title[feature].map(job_cate_tree)
        elif feature in feature_columns:
            data_all_feature_numeric_pd[feature] = data_all_marked_position_title[
                feature].map(feature_columns_dict[feature])  # .astype(int)
        #             data_all_feature_numeric_pd[feature] = data_all_marked_position_title[feature].map(test_lambda).astype(int)
        else:
            data_all_feature_numeric_pd[feature] = data_all_marked_position_title[feature].astype(int)

    return data_all_feature_numeric_pd


if __name__ == '__main__':
    pass
