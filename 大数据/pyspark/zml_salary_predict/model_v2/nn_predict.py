# -*- coding: utf-8 -*-
from .predict_utils import get_salary
if __name__ == '__main__':
    #五个参数，以都好分隔
    #第一个参数为就读的学校
    #第二个参数为就读的专业
    #第三个参数为学历
    #第四个参数为职么力
    #第五个参数为模型的类型，有min和max可选
    features = '北京大学,软件工程,本科,79,min,'
    print(get_salary(features))
    