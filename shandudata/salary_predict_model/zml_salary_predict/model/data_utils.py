# -*- coding: utf-8 -*-
import pandas as pd
from torch.utils.data import Dataset
import torch


def transform(data, quata_degree, quata_school, quata_major, quata_province, columns, train_type):
    # print(columns)
    degree_index = columns.index('degree_code')
    school_index = columns.index('school_code')
    major_index = columns.index('major_code')
    province_index = columns.index('province_code')
    zhimeli_index = columns.index('zhimeli_min')
    if train_type == 'min':
        pass_index1 = columns.index('salary_max')
        pass_index2 = columns.index('zhimeli_max')
        pass_index3 = columns.index('salary_min')
    elif train_type == 'max':
        pass_index1 = columns.index('salary_min')
        pass_index2 = columns.index('zhimeli_min')
        pass_index3 = columns.index('salary_max')
        zhimeli_index = columns.index('zhimeli_max')

    result = []
    for column in columns:
        idx = columns.index(column)
        if idx in [degree_index, school_index, major_index, province_index]:
            if idx == degree_index:
                t = [0] * quata_degree
                t[int(data[idx] - 1)] = 1
                result.extend(t)
            elif idx == school_index:
                t = [0] * quata_school
                t[int(data[idx] - 1)] = 1
                result.extend(t)
            elif idx == major_index:
                t = [0] * quata_major
                t[int(data[idx] - 1)] = 1
                result.extend(t)
            elif idx == province_index:
                t = [0] * quata_province
                t[int(data[idx] - 1)] = 1
                result.extend(t)
        elif idx in [pass_index1, pass_index2, pass_index3]:
            pass
        elif idx == zhimeli_index:
            result.append(torch.log(torch.tensor(data[idx])).numpy().tolist())
        else:
            result.append(data[idx])
    return torch.tensor(result)


# 定义一个子类叫 custom_dataset，继承与 Dataset
class custom_dataset(Dataset):
    def __init__(self, csv_path, transform=transform, train_type='min', quata_degree=12, quata_school=2596,
                 quata_major=1703, quata_province=33):
        # 学位类别数
        self.quata_degree = quata_degree
        # 学校数
        self.quata_school = quata_school
        # 专业数
        self.quata_major = quata_major
        # 省份数
        self.quata_province = quata_province
        self.transform = transform  # 传入数据预处理
        df = pd.read_csv(csv_path, encoding='utf8')
        self.columns = df.columns.tolist()
        degree_index = self.columns.index('degree_code')
        school_index = self.columns.index('school_code')
        major_index = self.columns.index('major_code')
        province_index = self.columns.index('province_code')
        self.train_type = train_type
        if train_type == 'min':
            label_index = self.columns.index('salary_min')
            self.label_list = [line[label_index] for line in df.values]  # 得到标签列数据
            self.data_list = [line.tolist() for line in df.values]  # 得到特征数据
        elif train_type == 'max':
            label_index = self.columns.index('salary_max')
            self.label_list = [line[label_index] for line in df.values]  # 得到标签列数据
            self.data_list = [line.tolist() for line in df.values]  # 得到特征数据
        else:
            print('salary_type either min nor max ,load dataset error!')

    def __getitem__(self, idx):  # 根据 idx 取出其中一个
        data = self.data_list[idx]
        label = self.label_list[idx]
        if self.transform is not None:
            data = self.transform(data, self.quata_degree, self.quata_school, self.quata_major, self.quata_province,
                                  self.columns, self.train_type)
        return data, torch.log(torch.tensor(label))
        # return data, torch.tensor(label)

    def __len__(self):  # 总数据的多少
        return len(self.label_list)
