# -*- coding: utf-8 -*-

from flask import jsonify
from flask import Flask
from flask import request
from .predict_utils import *

app = Flask(__name__)  # 创建1个Flask实例

# 返回值：预测的薪资【salary】
@app.route('/get_salary', methods=['POST', 'GET'])  # 路由系统生成 视图对应url,1. decorator=app.route() 2. decorator(first_flask)
def first_flask():  # 视图函数
    parameter = request.args.get('P')
    print(parameter)
    res = get_salary(parameter)
    return jsonify(res)

# 训练数据字段顺序
# degree_code,school_code,major_code,_other,_zhuan,_ben,_2_first_rate,_211,_c9,_top_2,_985,province_code,salary_min,salary_max,zhimeli_min,zhimeli_max
# 调用模型需要使字段顺序和训练模型时的顺序一致
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port=5000)
