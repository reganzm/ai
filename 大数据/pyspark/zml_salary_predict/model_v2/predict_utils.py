# -*- coding: utf-8 -*-

import pandas as pd
import torch
import math
from flask import Flask

app = Flask(__name__)  # 创建1个Flask实例
quata_degree = 12
quata_school = 2596
quata_major = 1703
quata_province = 33

# train_type 可取值为min和max【min表示使用的是简历中的salary_min训练的模型，max表示使用的是简历中的salary_max训练的模型】
min_train_type = 'min'
max_train_type = 'max'

# 读取模型
min_model_path = 'model_' + min_train_type + '.ckpt'
min_model = torch.load(min_model_path)
# 转化为测试模式
min_model.eval()

# 读取模型
max_model_path = 'model_' + max_train_type + '.ckpt'
max_model = torch.load(max_model_path)
# 转化为测试模式
max_model.eval()


def load_model(train_type):
    if train_type == max_train_type:
        return max_model
    return min_model


# 传入的参数：
# 学校【school_code,_other,_zhuan,_ben,_2_first_rate,_211,_c9,_top_2,_985,province_code】
# 专业【major_code】
# 学历【degree】
# 职么力【zhimeli】

# 返回值：预测的薪资【salary】
school_info = pd.read_csv('./datas/university.csv', encoding='utf8', index_col='sid')
school_dict = school_info.to_dict()

major_info = pd.read_csv('./datas/major.csv', encoding='utf8', index_col='name')
major_info.index = major_info.index.map(lambda name: name.strip())
major_dict = major_info.to_dict()

degree_info = pd.read_csv('./datas/degree.csv', encoding='utf8', index_col='name')
degree_info.index = degree_info.index.map(lambda name: name.strip())
degree_dict = degree_info.to_dict()

province_info = pd.read_csv('./datas/province.csv', encoding='utf8', index_col='name')
province_info.index = province_info.index.map(lambda name: name.strip())
province_dict = province_info.to_dict()


def transform(pos, quata):
    # 传入向量的位置pos和向量的长度quata，返回长度为quata且pos位置为1其余位置为0的向量
    array = [0] * quata
    array[pos - 1] = 1
    return array


def get_salary(features):
    # parameter = "西华大学,软件工程,本科,60,min"
    keys = features.split(',')
    if len(keys) == 5:
        school_name = keys[0].strip()
        major = keys[1].strip()
        degree = keys[2].strip()
        zhimeli = float(keys[3])
        train_type = keys[4].strip()

        # 学历
        if degree_dict['id'].get(degree):
            degree_id = degree_dict['id'].get(degree)
        else:
            degree_id = degree_dict['id'].get('unknown')

        dict_school = dict(zip(school_dict['name'].values(), school_dict['name'].keys()))
        if dict_school.get(school_name):
            school_id = dict_school.get(school_name)
        else:
            school_id = dict_school.get('unknown')

        # 专业
        if major_dict['id'].get(major):
            major_id = major_dict['id'].get(major)
        else:
            major_id = major_dict['id'].get('unknown')
        # 学校的各个维度信息
        # _other,_zhuan,_ben,_2_first_rate,_211,_c9,_top_2,_985 顺序不要变
        _other = school_dict['_other'][school_id]
        _zhuan = school_dict['_zhuan'][school_id]
        _ben = school_dict['_ben'][school_id]
        _2_first_rate = school_dict['_2_first_rate'][school_id]
        _211 = school_dict['_211'][school_id]
        _c9 = school_dict['_c9'][school_id]
        _top_2 = school_dict['_top_2'][school_id]
        _985 = school_dict['_985'][school_id]

        # 省份
        if school_dict['province'].get(school_id):
            province_name = school_dict['province'].get(school_id)
        else:
            province_name = 'unknown'
        # 城市
        if school_dict['city'].get(school_id):
            school_city = school_dict['city'].get(school_id)
        else:
            school_city = 'unknown'

        province_id = province_dict['id'].get(province_name)

        features = []

        features.extend(transform(degree_id, quata_degree))
        features.extend(transform(school_id, quata_school))
        features.extend(transform(major_id, quata_major))
        features.append(_other)
        features.append(_zhuan)
        features.append(_ben)
        features.append(_2_first_rate)
        features.append(_211)
        features.append(_c9)
        features.append(_top_2)
        features.append(_985)
        features.extend(transform(province_id, quata_province))
        if zhimeli >= 80:
            zhimeli = 80
        if zhimeli <= 30:
            zhimeli = 30
        # 职么力用log放缩处理
        features.append(math.log(zhimeli))
        # major_high,major_hot,degree_w,city_w,area_w
        # major_high
        if major_dict['high'].get(major):
            major_high = int(major_dict['high'].get(major))
        else:
            major_high = int(major_dict['high'].get('unknown'))
            # major_hot
        if major_dict['hot'].get(major):
            major_hot = int(major_dict['hot'].get(major))
        else:
            major_hot = int(major_dict['hot'].get('unknown'))
        # degree_w
        if degree_dict['w'].get(degree):
            degree_w = int(degree_dict['w'].get(degree))
        else:
            degree_w = int(degree_dict['w'].get('unknown'))

            # city_w 3,1,1
        if province_dict['center'].get(province_name):
            center_city = province_dict['center'].get(province_name)
            if center_city == school_city:
                city_w = 3
            else:
                city_w = 1
        else:
            city_w = 1
            # area_w 3,2,1
        area_w = 1
        for area in ['east', 'middle', 'west']:
            if province_dict[area].get(province_name):
                tmp = province_dict[area].get(province_name)
                if tmp > 0:
                    area_w = tmp
                    break
        features.append(major_high)
        features.append(major_hot)
        features.append(degree_w)
        features.append(city_w)
        features.append(area_w)

        features = torch.tensor(features)
        print('features length:{},model type:{}'.format(len(features), train_type))
        model = load_model(train_type)
        out = model(features)
        print('预测毕业薪资为：{:.2f}'.format(math.e ** float(out)))
        res = math.e ** float(out)
        # 过大过小的数据，进行截断处理
        if res > 35000.:
            res = 35000
        if res < 2000:
            res = 3500
        return res
    else:
        print('arguments is error!')
        raise RuntimeError('参数错误')
