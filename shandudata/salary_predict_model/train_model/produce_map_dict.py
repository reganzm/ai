# coding:utf-8
'''
Created on 2014年12月23日

@author: likaiguo
'''

# 将表格中各种文本转换为数字
data_all_marked_position_title.columns.tolist()
feature_columns = [
    u'age',
#             u'birthday',
    u'city',
#             u'company_cate',
    u'edu_degree',
    u'gender',
#             u'industry_cate',
    u'lower_salary',
#             u'position_title',
#             u'school',
    u'upper_salary',
    u'work_len',
    'school_level',
#             '2nd_class',
#             '3rd_class',
    'first_class',
#             'full_cut',
#             'raw_text',
#             'unknown'
]


# 构造映射字典
feature_columns_dict = {}

for feature in feature_columns:
    feature_values = data_all_marked_position_title[feature].unique().tolist()
    feature_reduce_set = set([simplify_value(value) for value in feature_values])
    feature_dict = {}
    for i, value in enumerate(feature_reduce_set):
        try:
            feature_dict[value] = int(value)
        except:
            feature_dict[value] = i
    feature_columns_dict[feature] = feature_dict

print json.dumps(feature_columns_dict, ensure_ascii=False, indent=2, sort_keys=True)

if __name__ == '__main__':
    pass
