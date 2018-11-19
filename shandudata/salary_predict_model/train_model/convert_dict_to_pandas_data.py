# coding: utf-8
import json

import codecs
import jieba
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
from os.path import join
from pylab import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV

from pre_mark_job_title import mark_job_cls
from settings import RESOURCES

# user_dict_dir = '/media/likaiguo/disk7/github/TalentMiner/resources/user_dict'
# filenames = os.listdir(user_dict_dir)
# for filename in filenames:
#     seg_file_path = os.path.join(user_dict_dir, filename)
#     print seg_file_path
#     jieba.load_userdict(seg_file_path)
# In[3]:
lines = codecs.open('../data/salary.json', 'r', 'utf-8').readlines()

dict_into_list = [json.loads(line) for line in lines]
columns = [u'city',
           u'school',
           u'work_len',
           u'gender',
           u'age',
           u'edu_degree',
           u'birthday',
           u'company_cate',
           u'position_title',
           u'upper_salary',
           u'lower_salary',
           u'industry_cate']

data = pd.DataFrame(dict_into_list)
# 然后是数据转换,将所有字段数值化
# 较为复杂的是职位和学校类型的转换,都用查表的方式

data.to_csv("hello.csv", encoding='utf-8')

columns = data.columns.tolist()
group_degree = data.groupby("edu_degree").sum()
group_degree.index = ['unmarked', 'EMBA', 'MBA', 'zhongzhuan', 'zhongji', 'other', 'senior', 'doctor', 'dazhuan',
                      'bachelor', 'master', 'high school']
group_degree['upper_salary'].plot(kind='bar')
group_degree_median = data.groupby('edu_degree').median()
group_degree_median.index = ['unmarked', 'EMBA', 'MBA', 'zhongzhuan', 'zhongji', 'other', 'senior', 'doctor', 'dazhuan',
                             'bachelor', 'master', 'high school']
group_degree_median['upper_salary'].plot(kind='bar')
group_degree_median
data.head(2)

# In[15]:

shanghai = data[data['city'] == u'上海']
shanghai_degree_group_median = shanghai.groupby('edu_degree').median()

# shanghai_degree_group_median.index  = ['EMBA','MBA','zhongzhuan','zhongji','other','senior','doctor','dazhuan','bachelor','master','high school']

shanghai_degree_group_median.plot(kind='bar')
shanghai_degree_group_median

shanghai[shanghai['edu_degree'] == u'博士'].sort(['upper_salary'], ascending=[0])

position_title_median_df = data.groupby('position_title').median()

# position_title_median_df.to_csv('position_title_median.csv',encoding='utf-8')
position_title_median_df.head(10)

# In[23]:

# import jieba 
# from jieba import posseg as pseg
# keywords_sort_dict = {}

# for position_title in position_title_median_df['position_title']:
#     seg_words = pseg.cut(position_title)
#     for word in seg_words:
#         word_lower = word.word.lower()
#         idx = keywords_sort_dict.get(word_lower)
#         if not idx:
#             keywords_sort_dict[word_lower] = 1




school_group = data.groupby('school').median()

school_group.head(40)

school_group.to_csv('school_group_median.csv', encoding='utf-8')

# In[27]:

degree = data['edu_degree'].unique()
print(',\n'.join(degree))
data[data['edu_degree'] == u'其他']
# school_dict_path = '/media/likaiguo/disk7/github/TalentMiner/resources/user_dict/user_dict_school.txt'
school_dict_path = join(RESOURCES, "user_dict/user_dict_school.txt")
jieba.load_userdict(school_dict_path)

from school_cate_mark import mark_school_cls

all_school_dict_list = []
for school in data['school']:
    school_dict = mark_school_cls(school)
    all_school_dict_list.append(school_dict)

all_schools = pd.DataFrame(all_school_dict_list)

all_schools.to_csv('all_schools.csv', encoding='utf-8')
data['school_level'] = all_schools['level']
data.head(10)

data.to_csv('salary_marked_school_level.csv', encoding='utf-8')
data.groupby('school_level').median()

area_shanghai = data['city'] == u'北京'
degree_bachelor = data['edu_degree'] == u'博士'
data[area_shanghai & degree_bachelor].groupby('school_level').median()

area_shanghai = data['city'] == u'成都'
degree_bachelor = data['edu_degree'] == u'硕士'
data[area_shanghai & degree_bachelor].groupby('school_level').median()

data[area_shanghai & degree_bachelor].groupby('school_level').describe()

data.groupby('school_level').median()
mpl.rcParams['font.sans-serif'] = ['SimHei']
degree_group_median = data.groupby('edu_degree').median()
degree_group_median
ax = degree_group_median.plot(kind='bar')
data.groupby('city').median()
data.head(10)

pylab.rcParams['figure.figsize'] = 8, 6
font = FontProperties(fname="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", size=18)

# mpl.rcParams['font.sans-serif'] = ['Vera Sans']
t = arange(-4 * pi, 4 * pi, 0.01)
y = sin(t) / t
plt.plot(t, y)
plt.title(u'钟形函数', fontproperties=font)
plt.xlabel(u'时间', fontproperties=font)
plt.ylabel(u'幅度', fontproperties=font)
# plt.set_xlabel(u"這是x軸--这是简体中文",fontproperties = font)
# plt.set_ylabel(u"這是y軸",fontproperties = font)
plt.show()

pylab.rcParams['figure.figsize'] = 16, 12
font = FontProperties(fname="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", size=14)

x = np.linspace(0, 1, 101)

fig, ax = pylab.subplots(figsize=(10, 4))
ax.plot(x, np.sin(2 * np.pi * x))
ax.set_xlabel(u"這是x軸--这是简体中文", fontproperties=font)
ax.set_ylabel(u"這是y軸", fontproperties=font)

data.describe()

mark_position_titles_list = []

for position_title in data['position_title']:
    mark_position_titles_list.append(mark_job_cls(position_title))

position_title_marked_df = pd.DataFrame(mark_position_titles_list)

data_all_marked_position_title = (data.T.append(position_title_marked_df.T)).T
data_all_marked_position_title.head(5)
data_all_marked_position_title.to_csv('data_all_marked_position_title.csv', encoding='utf-8')

# 将表格中各种文本转换为数字
# data_all_marked_position_title.columns.tolist()
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

feature_columns_dict = {}


def simplify_value(value):
    if isinstance(value, unicode) or isinstance(value, str):
        value = value
        if '|' in value:
            value = value.split('|')[0]
        else:
            value = value.split('-')[0]
    return value


for feature in feature_columns:
    feature_values = data_all_marked_position_title[feature].unique().tolist()
    feature_reduce_set = set([simplify_value(value) for value in feature_values])
    feature_dict = {}
    for i, value in enumerate(feature_reduce_set):
        if isinstance(value, unicode) or isinstance(value, str):
            feature_dict[value] = i
        else:
            feature_dict[value] = value
    feature_columns_dict[feature] = feature_dict

data_all_feature_pd = pd.DataFrame()
data_all_feature_numeric_pd = pd.DataFrame()

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

job_type = [
    u"游戏",
    u"设计",
    u"技术",
    # u"职能",
    u"市场与销售",
    # u"",
    u"运营",
    u"产品",
    # u"电商"
]
job_type_index = data_all_marked_position_title['first_class'].isin(job_type)
data_all_marked_position_title = data_all_marked_position_title[job_type_index]

citys = [
    u'北京',
    u'成都',
    u'上海',
    u'广州',
    u'深圳',
    u'杭州',
    u'西安',
    u'武汉',
    u'重庆',
]
citys_index = data_all_marked_position_title['city'].isin(citys)
data_all_marked_position_title = data_all_marked_position_title[citys_index]

for feature in feature_columns:
    data_all_feature_pd[feature] = data_all_marked_position_title[feature].apply(simplify_value)
    #     print feature
    data_all_feature_numeric_pd[feature] = data_all_feature_pd[feature].map(feature_columns_dict[feature]).astype(int)

# data_all_marked_position_title.groupby('first_class').sum()

sorted_columns = [u'lower_salary', u'upper_salary', u'age', u'city', u'edu_degree', u'gender', u'work_len',
                  'school_level', 'first_class']
data_all_feature_pd = data_all_feature_pd[sorted_columns]
data_all_feature_pd.head(5)

data_all_feature_pd[data_all_feature_pd['first_class'] == u'技术'].groupby('work_len').median()

my_city = data_all_feature_pd['city'] == u'成都'
my_age = data_all_feature_pd['age'] == 28
my_gender = data_all_feature_pd['gender'] == u'男'
my_degree = data_all_feature_pd['edu_degree'] == u'硕士'
my_job_type = data_all_feature_pd['first_class'] == u'技术'
my_school_level = data_all_feature_pd['school_level'] == u'中国一流大学'
my_work_len = data_all_feature_pd['work_len'] == 2

my_data = data_all_feature_pd[
    my_city
    #                               & my_age
    & my_degree
    & my_job_type
    & my_school_level
    & my_work_len
    ]

my_data.head(5)

# data_all_marked_position_title['first_class'].unique()

print '",u"'.join(data_all_feature_pd['first_class'].unique().tolist())

my_data.describe()

data_all_feature_numeric_pd = data_all_feature_numeric_pd[sorted_columns]
data_all_feature_numeric_pd.head(3)

cols = data_all_feature_pd.columns.tolist()
print cols
sorted_columns = [u'lower_salary', u'upper_salary',
                  #                 u'age',
                  u'city',
                  u'edu_degree',
                  u'gender',
                  u'work_len',
                  #                   'school_level',
                  'first_class'
                  ]
df = data_all_feature_numeric_pd[sorted_columns]
train_data = df.values[:15000]

X = train_data[:, 3:]
y_min = train_data[:, 0]
y_max = train_data[:, 1]
y_median = (y_min + y_max) / 2

n = len(X) * 5 / 10

X_train = X[:n, :]

y_train_min = y_min[:n]
y_train_max = y_max[:n]
y_train_median = y_median[:n]

X_test = X[n:, :]

y_test_min = y_min[n:]
y_test_max = y_max[n:]
y_test_median = y_median[n:]

print len(train_data), len(X), len(y), n

model = RandomForestClassifier(n_estimators=200, max_features=0.5, max_depth=5)
# model = RandomForestRegressor(n_estimators=200,max_features=0.5, max_depth=5)

model_min = model.fit(X_train, y_train_min)
y_prediction_min = model_min.predict(X_test)

model_max = model.fit(X_train, y_train_max)
y_prediction_max = model_max.predict(X_test)

model_median = model.fit(X_train, y_train_median)
y_prediction_median = model_median.predict(X_test)

y_prediction_median_max_min = (y_prediction_min + y_prediction_max) / 2


def score(y_prediction, y_test, y_test_median, alpha=0.2):
    print len(y_prediction), len(y_test), len(y_test_median)
    # 绝对等于
    print "绝对等于:prediction accuracy:", np.sum(y_test == y_prediction) * 1. / len(y_test)
    # 在一定区间
    true_vlaues = (y_prediction * (1 - alpha) < y_test) & (y_test < y_prediction * (1 + alpha))
    print "在区间内:prediction accuracy:", np.sum(true_vlaues) * 1. / len(y_test)
    # 距离平均值
    true_median = (y_prediction * (1 - alpha) < y_test_median) & (y_test_median < y_test_median * (1 + alpha))
    print "区间内距离平均值:prediction accuracy:", np.sum(true_median) * 1. / len(y_test)

    print '\n\n'


score(y_prediction_min, y_test_min, y_test_median)

score(y_prediction_max, y_test_max, y_test_median)

score(y_prediction_median, y_test_median, y_test_median)

score(y_prediction_median_max_min, y_test_median, y_test_median)

y_result_df = pd.DataFrame()
y_result_df['y_prediction_min'] = y_prediction_min
y_result_df['y_test_min'] = y_test_min

y_result_df['y_prediction_max'] = y_prediction_max
y_result_df['y_test_max'] = y_test_max

y_result_df['y_prediction_median'] = y_prediction_median
y_result_df['y_test_median'] = y_test_median

y_result_df['y_prediction_median_max_min'] = y_prediction_median_max_min

# y_result_df['y_test_median'] = y_test_median



parameter_grid = {
    'max_features': [0.1, 0.5],
    'max_depth': [5., 10., 20., None]
}

grid_search = GridSearchCV(RandomForestClassifier(n_estimators=200), parameter_grid,
                           cv=5, verbose=3)

grid_search.fit(train_data[0:, 2:], train_data[0:, 0])
sorted(grid_search.grid_scores_, key=lambda x: x.mean_validation_score)
print(grid_search.best_score_)
print(grid_search.best_params_)
