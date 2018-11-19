# coding:utf-8
# from django.db import models
# Create your models here.
from datetime import datetime
from mongoengine import (StringField,
                         DateTimeField,
                         ReferenceField,
                         Document,
                         )


class SalaryPredict(Document):
    """
    @summary: 算薪资的查询
    """


class Result(Document):
    """
    @summary:
    """
    query = ReferenceField(SalaryPredict)
    query_time = DateTimeField(default=datetime.now())


class UserPredict(Document):
    email = StringField()
    salary_predict = ReferenceField(SalaryPredict)
    query_time = DateTimeField(default=datetime.now())


if __name__ == '__main__':
    from pymongo import MongoClient
    client = MongoClient(('mongodb://root:hopper201313@115.28.222.146:27017/'))
    suanxinzi = client.suanxinzi
    d = suanxinzi['salary_predict'].find_one({'data': 'hello'})
    c = suanxinzi['salary_predict']
    doc = c.insert({'data': 'hello'})
