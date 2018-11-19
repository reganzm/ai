# -*- coding: utf-8 -*-

import pandas as pd
import torch
import math
from flask import jsonify
from flask import Flask
from flask import request

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
major_dict = major_info.to_dict()['id']

degree_info = pd.read_csv('./datas/degree.csv', encoding='utf8', index_col='name')
degree_info.index = degree_info.index.map(lambda name: name.strip())
degree_dict = degree_info.to_dict()['id']

province_info = pd.read_csv('./datas/province.csv', encoding='utf8', index_col='name')
province_info.index = province_info.index.map(lambda name: name.strip())
province_dict = province_info.to_dict()['id']


@app.route('/get_salary', methods=['POST', 'GET'])  # 路由系统生成 视图对应url,1. decorator=app.route() 2. decorator(first_flask)
def first_flask():  # 视图函数
    parameter = request.args.get('P')
    print(parameter)
    return jsonify(get_salary(parameter))


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
        if degree_dict.get(degree):
            degree_id = degree_dict.get(degree)
        else:
            degree_id = degree_dict.get('unknown')

        dict_school = dict(zip(school_dict['name'].values(), school_dict['name'].keys()))
        if dict_school.get(school_name):
            school_id = dict_school.get(school_name)
        else:
            school_id = dict_school.get('unknown')

        # 专业
        if major_dict.get(major):
            major_id = major_dict.get(major)
        else:
            major_id = major_dict.get('unknown')
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

        province_id = province_dict[province_name]

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
        # 职么力用log放缩处理
        features.append(math.log(zhimeli))

        features = torch.tensor(features)
        print('features length:{},model type:{}'.format(len(features), train_type))
        model = load_model(train_type)
        out = model(features)
        print('预测毕业薪资为：{:.2f}'.format(math.e ** float(out)))
        return math.e ** float(out)
    else:
        print('arguments is error!')
        return 0


# 训练数据字段顺序
# degree_code,school_code,major_code,_other,_zhuan,_ben,_2_first_rate,_211,_c9,_top_2,_985,province_code,salary_min,salary_max,zhimeli_min,zhimeli_max
# 调用模型需要使字段顺序和训练模型时的顺序一致
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port=5000)
