# -*- coding: utf-8 -*-

import pandas as pd
import torch
import math
from .settings import *

quata_degree = Quota_degree_code
quata_school = Quota_school_code
quata_major = Quota_major_code
quata_province = Quota_province_code

# 读取模型
model_path = 'model.ckpt'
model = torch.load(model_path)
# 转化为测试模式
model.eval()


def get_model():
    return model


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
    # parameter = "西华大学,软件工程,本科,60"
    keys = features.split(',')
    if len(keys) == 4:
        school_name = keys[0].strip()
        major = keys[1].strip()
        degree = keys[2].strip()
        zhimeli = float(keys[3])

        # 学历
        if degree_dict['id'].get(degree):
            degree_id = degree_dict['id'].get(degree)
        else:
            degree_id = degree_dict['id'].get('unknown')

        dict_school = dict(zip(school_dict['name'].values(), school_dict['name'].keys()))
        # 学校
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

        # degree_code, school_code, major_code, major_high, major_hot,
        # degree_w, _other, _zhuan, _ben, _2_first_rate, _211, _c9, _top_2, _985,
        # province_code, location_w, salary_new, zhimeli, lat, long

        features.extend(transform(degree_id, quata_degree))
        features.extend(transform(school_id, quata_school))
        features.extend(transform(major_id, quata_major))

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

        major_high = (major_high - 0) / (3 - 0)
        features.append(major_high)

        major_hot = (major_hot - 0) / (2 - 0)
        features.append(major_hot)

        # degree_w
        if degree_dict['w'].get(degree):
            degree_w = int(degree_dict['w'].get(degree))
        else:
            degree_w = int(degree_dict['w'].get('unknown'))
        degree_w = (degree_w - 1) / (5 - 1)
        features.append(degree_w)

        features.append(_other)
        features.append(_zhuan)
        features.append(_ben)
        features.append(_2_first_rate)
        features.append(_211)
        features.append(_c9)
        features.append(_top_2)
        features.append(_985)
        features.extend(transform(province_id, quata_province))

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
        location_w = city_w * area_w
        location_w = (location_w - 1) / (9 - 1)
        features.append(location_w)

        # 职么力标准化处理
        zhimeli = (zhimeli - 30.) / 75. * 2.
        zhimeli = zhimeli * 2
        zhimeli = (math.e ** zhimeli - math.e ** (-zhimeli)) / (math.e ** zhimeli + math.e ** (-zhimeli))
        features.append(zhimeli)

        # lat lng经度纬度
        if school_dict['lat'].get(school_id):
            lat = float(school_dict['lat'].get(school_id))
        if school_dict['lng'].get(school_id):
            lng = float(school_dict['lng'].get(school_id))
        # 归一化
        features.append(lat / 90.)
        features.append((lng / 180.))

        features = torch.tensor(features)
        print('features length:{}'.format(len(features)))
        model = get_model()
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
