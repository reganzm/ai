# coding:utf-8
'''
Created on 2014年12月27日

@author: likaiguo
'''

from mongoengine import DateTimeField, Document, StringField, connect
from mongoengine.fields import IntField

connect(db='recruiting')


class WorkStatis(Document):
    '''
    classdocs
    '''

    start_time = DateTimeField()
    end_time = DateTimeField()
    scale_max = IntField(db_field='companyscale_max')
    scale_min = IntField(db_field='companyscale_min')
    gender = StringField()
    age = IntField()
    c_name = StringField(db_field='company_name')
    school = StringField(db_field='education_school')
    degree = StringField(db_field='education_degree')
    major = StringField(db_field='education_major')
    city = StringField(db_field='address')

    salary_min = IntField(db_field='salary_min')
    salary_max = IntField(db_field='salary_max')

    expect_min = IntField(db_field='expect_salary_min')
    expect_max = IntField(db_field='expect_salary_max')

    position_title = StringField(db_field='position_title')
    job_desc = StringField(db_field='job_desc')
    work_len = IntField(db_field='work_experience_len')

    meta = {
        # 'db_alias':"recruiting",
        'index_background': True,
        #             "collection": "resumeData",
        "indexes": [
            "-start_time",
            "end_time",
            "-major",
            "-city",
            "degree",
            "school",
            "expect_min",
            "expect_max",
            "position_title",
        ]

    }


if __name__ == "__main__":
    from bson import json_util

    works = WorkStatis.objects.filter()  # .limit(10)
    print WorkStatis.objects.count()
    i = 0
    for work in works:
        #         print work.id, work.c_name
        print json_util.dumps(work._data, ensure_ascii=False, indent=2)

        for filed in work._fields_ordered:
            if isinstance(work[filed], unicode):
                work[filed] = work[filed].strip()
        work.save()
        i += 1
        if i % 100 == 0:
            print i
