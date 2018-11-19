# coding:utf-8
from __future__ import unicode_literals

import json
from math import log1p

import datetime
import os
import pandas as pd
from bson import json_util
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from html_to_image import html2image, image_crop
from settings import IMG_PATH, MONGODB_URL, RESOURCES, SAHRE_URL_HEAD
from train_model.education import education_score
from train_model.pre_mark_job_title import mark_job_cls
from train_model.suanxinzi import salary_predict, train

PATH = os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
PATH = os.path.join(RESOURCES, "models")
model_min, model_max, model_median = train(PATH)

job_type_map = {
    u'攻城狮': u'技术',
    u'射鸡湿': u'设计',
    u'产品狗': u'产品',
    u'运营人猿': u'运营',
    u'市场商务': u'市场与销售',
    u'暖心行政': u'职能'
}

constellation_dict = {
    # 这年头，新朋友认识不问问星座都不好意思聊天，那你是？
    u'白羊座': 1,
    u'处女座': -3,
    u'金牛座': 3,
    u'巨蟹座': 1,
    u'摩羯座 ': 3,
    u'射手座': 1,
    u'狮子座': 3,
    u'双鱼座': 2,
    u'双子座': 2,
    u'水瓶座': 2,
    u'天秤座': 2,
    u'天蝎座': 3,
}

q1_dict = {
    1: -3,
    2: 0,
    3: 3
}
q2_dict = {
    1: -3,
    2: -1,
    3: 3,
    4: 3,
    5: 1,
    6: -3

}
HOUSE_PRICE = {
    u'北京': 34724,
    u'上海': 29286,
    u'广州': 18857,
    u'深圳': 26091,
    u'杭州': 16268,
    u'成都': 7917,
    u'重庆': 6991,
    u'武汉': 9054,
    u'西安': 6562

}
HOUSE_AREA = 90


def get_salary_level(salary, city):
    """
    @summary: 按地区拍脑袋
    """
    if city in [u'成都', u'西安', u'重庆', u'武汉']:
        salary += 2000
    if salary > 25000:
        level = u'土豪'
    elif salary > 15000:
        level = u'小康'
    elif salary > 9000:
        level = u'温饱'
    else:
        level = u'屌丝'

    return level


def buy_house_year(salary, city, area=HOUSE_AREA):
    """
    @summary: 买房需要的时间
    """
    total_cost = HOUSE_PRICE.get(city, 7000) * 90
    year_of_buy_house = total_cost / ((salary + 1.0) * 12)
    year = int(year_of_buy_house)

    return year + 1 if year_of_buy_house > year + 0.5 else year


def get_or_insert(collection, data, insert=True):
    from pymongo import MongoClient
    client = MongoClient((MONGODB_URL))
    suanxinzi = client.suanxinzi
    doc = suanxinzi[collection].find_one(data)
    if not doc and insert:
        data['add_time'] = datetime.datetime.now()
        _id = suanxinzi[collection].insert(data)
        doc = data
        doc['_id'] = _id

    return doc


def insert_data(collection, data):
    from pymongo import MongoClient
    client = MongoClient((MONGODB_URL))
    suanxinzi = client.suanxinzi
    data['add_time'] = datetime.datetime.now()
    _id = suanxinzi[collection].insert(data)
    return _id


# '20151124'
ALOGRITHM_VER = 1.0
# 2015-01-04 14:27 星座参数变化
ALOGRITHM_VER = 1.1
# 2015-01-04 20:41  薪资参数,2年以上添加1年经验
ALOGRITHM_VER = 1.2
# 2015-02-27 20:41  房价
ALOGRITHM_VER = 1.33


def salary_predict_pro(request):
    para = json.loads(request.GET.get('p'))
    data = para['data']
    request_doc = get_or_insert('request_data', data)
    result = get_or_insert('result', {'request_id': str(request_doc['_id']), 'alog_ver': ALOGRITHM_VER}, insert=False)
    if not result:

        work_len = data.get('workLength', 3)
        if work_len != 3:
            work_len = (int(work_len.split('-')[0]) + int(work_len.split('-')[1])) / 2
            if work_len < 1:
                work_len = 1
            elif work_len > 15:
                work_len = 10
            else:
                work_len += 1
        scale = int(data.get('scale', '0-50').split('-')[0])
        first_class = job_type_map.get(data.get('jobType'), u'技术')
        second_class = data.get('secondClass', [])
        gender = data.get('gender', u'男')
        parameters = {
            'lower_salary': 1000,
            'upper_salary': 2000,
            'age': data.get('age', 27),
            'city': data.get('city', u'成都'),
            'degree': data.get('degree', u'本科'),
            'gender': gender,
            'work_len': work_len,
            'first_class': first_class,  # tmp['data[jobType]'],
            'first_class_1': first_class,
            'school_level': u"中国一流大学",
            "scale": scale
        }
        if second_class:
            job_cls = mark_job_cls(' '.join(second_class))
        else:
            job_cls = mark_job_cls('')
        parameters['first_class_2'] = job_cls.get('first_class_2')
        parameters['2nd_class_1'] = job_cls.get('2nd_class_1')
        parameters['3rd_class_1'] = job_cls.get('3rd_class_1')
        parameters['2nd_class_2'] = job_cls.get('2nd_class_2')
        parameters['3rd_class_2'] = job_cls.get('3rd_class_2')
        parameters['3rd_class_3'] = job_cls.get('3rd_class_3')
        # print json.dumps(parameters, ensure_ascii=False, indent=2).encode('ascii', 'ignore')
        predict_df = pd.DataFrame([parameters])

        y_min, y_max, y_median = salary_predict(model_min, model_max, model_median, predict_df)

        constellation = data.get('constellation')
        city = data.get('city', u'成都')
        ext = para['ext']
        q1 = ext.get('q1', {2: 1})
        q2 = ext.get('q2', {3: 1})

        edu_score = education_score(data.get("school", None), data.get("major", None))
        college_len = len(data.get("college", ""))
        college_score = college_len * 10 if 4 <= college_len <= 10 else 0

        adjust = constellation_dict.get(
            constellation, 0) + q1_dict.get(int(q1.keys()[0]), 0) + q2_dict.get(int(q2.keys()[0]), 0)
        scale_index = log1p(scale + 1)

        current = int(y_median * (adjust + scale_index + 100 + edu_score) / 100) + college_score
        future = int(y_max * (adjust + scale_index + 100 + edu_score) / 100) + college_score
        increase = int((y_max / y_median - 1) * 100)
        summary = get_salary_level(current, city)
        year_of_buy_house = buy_house_year(future, city)
        src = u"?src=%s&gender=%s&summary=%s&increase=%d&city=%s&year=%s" % (
            data.get('src', u'img/rw/woman/yy/1_3/yy_1_3_jx.png'),
            'man' if gender == u'男' else 'woman', summary, increase, city, year_of_buy_house)
        result = {'current': current,
                  'future': future,
                  'increase': increase,
                  'summary': summary,
                  'min': y_min,
                  'max': y_max,
                  'median': y_median,
                  'adjust': adjust,
                  'src': src,
                  'para': para,
                  'parameters': parameters,
                  'scale_index': scale_index,
                  'alog_ver': ALOGRITHM_VER,
                  'city': city,
                  'buy_house_year': year_of_buy_house
                  }
        parameters['request_id'] = request_doc['_id']
        parameters['alog_ver'] = ALOGRITHM_VER
        parameters['min'] = y_min
        parameters['max'] = y_max
        parameters['median'] = y_median

        get_or_insert('parameters', parameters)

        result['request_id'] = str(request_doc['_id'])

        get_or_insert('result', result)
    result['id'] = str(request_doc['_id'])
    result_str = json_util.dumps(result)

    client_data = {
        'ip': request.META['REMOTE_ADDR'],
        'cookie': request.COOKIES,
        #             'referer':request.META['HTTP_REFERER'],
        'user_agent': request.META['HTTP_USER_AGENT'],
        'request_id': request_doc['_id']
    }
    insert_data('client_data', client_data)

    return HttpResponse(result_str, 'application/json')


@csrf_exempt
def save_email(request):
    msg = ''
    try:
        data = json.loads(request.GET.get('data'))
        get_or_insert('user_email_query', data)
        status = 'ok'
    except Exception as e:
        msg = str(e)
        status = 'error'
    return HttpResponse(json_util.dumps({'status': status, 'msg': msg}), 'application/json')


@csrf_exempt
def share_statis(request):
    """
    @summary:
    """
    msg = ''
    try:
        data = json.loads(request.GET.get('data'))
        data['cookie'] = request.COOKIES,
        insert_data('share_statis', data)
        data['ip'] = request.META['REMOTE_ADDR']
        status = 'ok'
    except Exception as e:
        msg = str(e)
        status = 'error'
    return HttpResponse(json_util.dumps({'status': status, 'msg': msg}), 'application/json')


def produce_html_image(request):
    """
    @summary: 传入url生成html图片,存在本地服务器,返回url
    """
    msg = ''
    #     try:
    data = request.GET.get('data')
    if data:
        data = json.loads(data)
    else:
        data = {}
        data['url'] = request.GET.get('url')
        #             url = 'http://pro.suanxinzi.com/sxz/more.html?src=img/rw/man/xz/3_5/xz_3_5_tx.png&gender=man&summary=%E6%B8%A9%E9%A5%B1&increase=21&id=54a947261229826b3bad8654'
        #             data['url'] = url
        data['height'] = request.GET.get('height')
        data['width'] = request.GET.get('width')
    new_data = get_or_insert('produce_images', data, insert=False)

    if new_data and os.path.exists(IMG_PATH + new_data.get('fname', 'abasex.png')):
        data = new_data
    else:
        url = data.get('url')
        height = data.get('height')
        width = data.get('width')
        box = data.get('box')
        name = data.get('name', 'share')

        image_path = html2image(url, name, save_dir=IMG_PATH)
        save_path = image_crop(image_path, height, width, box)

        _, fname = os.path.split(save_path)
        data['img_url'] = 'http://' + request.META['HTTP_HOST'] + SAHRE_URL_HEAD + fname
        data['fname'] = fname
        insert_data('produce_images', data)
    status = 'ok'
    #     except Exception as e:
    #         data = {}
    #         msg = str(e)
    #         status = 'error'
    return HttpResponse(json_util.dumps({'status': status, 'msg': msg, 'data': data}), 'application/json')


def more(request):
    host = request.META['HTTP_HOST']
    referer = request.META.get('HTTP_REFERER', '')

    if host in referer:
        display = True
    else:
        display = False
    return render_to_response("sxz/more.html", {'display': display})


def log_click_info(request, collection, key):
    try:
        data = request.GET.copy()
        record_data = {
            'ip': request.META['REMOTE_ADDR'],
            'cookie': request.COOKIES,
            #             'referer':request.META['HTTP_REFERER'],
            'request_id': data.get('id', ''),
            key: data.get(key, 0)  # -1 , 0 ,1
        }
        status = 'ok'
        rcd_id = insert_data(collection, record_data)
        msg = str(rcd_id)
    except Exception as e:
        status = 'error'
        msg = str(e)

    return HttpResponse(json_util.dumps({'status': status, 'msg': msg}), 'application/json')


def predict_feedback(request):
    """
    @summary: 计算准确性
    """
    return log_click_info(request, collection='feed_back_data', key='accuracy')


def share_plantform(request):
    """
    @summary: 点击分享平台按钮
    """
    return log_click_info(request, collection='share_plantform', key='plantform')
