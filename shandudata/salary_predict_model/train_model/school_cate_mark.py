# coding:utf-8
'''
Created on 2014年12月14日

@author: likaiguo
'''
from __future__ import unicode_literals

import jieba
import jieba.posseg as pseg
import pandas as pd
from os.path import join

from settings import RESOURCES

school_dict_path = join(RESOURCES, "user_dict/user_dict_school.txt")
jieba.load_userdict(school_dict_path)

school_rank_path = join(RESOURCES, "user_dict/2014中国大学排行榜600强排行榜.csv")
school_rank_df = pd.read_csv(school_rank_path, encoding='utf-8')
universities, school_level = school_rank_df[u'学校名称'], school_rank_df[u'办学层次']
school_level_dict = dict(zip(universities, school_level))

school_feature_words_dict = {
    u"university": "国外",
    u"institute": "国外",
    u"college": "国外",
    u"英国": "国外",
    u"爱尔兰": "国外",
    u"爱顶堡": "国外",
    u"谢菲": "国外",
    u"牛津": "国外",
    u"芬兰": "国外",

    u"美国": "国外",
    u"悉尼": "国外",
    u"纽约": "国外",
    u"约克": "国外",

    u"州立": "国外",
    u"德国": "国外",
    u"germeny": "国外",
    u"日本": "国外",
    u"东京": "国外",
    u"京都": "国外",

    u"荷兰": "国外",
    u"法国": "国外",
    u"加拿大": "国外",
    u"多伦多": "国外",

    u"新西兰": "国外",
    u"澳大利亚": "国外",
    u"悉尼": "国外",
    u"堪培拉": "国外",

    u"韩国": "国外",
    u"澳大利亚": "国外",
    u"新加坡": "国外",
    u"印度": "国外",

    u"香港": "港澳台",
    u"台湾": "港澳台",
    u"澳门": "港澳台",

    u"大学": "大学",
    u"师大": "大学",
    u"211": "大学",
    u"985": "大学",
    u"研究": "大学",
    u"科学": "大学",

    u"部队": "军队院校",
    u"解放军": "军队院校",
    u"军": "军队院校",
    u"空军": "军队院校",
    u"炮": "军队院校",
    u"兵": "军队院校",

    u"学院": "学院",
    u"师范学院": "学院",
    u"师院": "学院",
    u"美院": "学院",

    u"干部管理": "党政",
    u"党": "党政",

    u"职业技术": "职业技术",
    u"广播": "职业技术",
    u"电视": "职业技术",
    u"广电": "职业技术",
    u"电大": "职业技术",
    u"职业": "职业技术",
    u"职工": "职业技术",
    u"学校": "职业技术",
    u"职": "职业技术",
    u"教育": "职业技术",
    u"外包": "职业技术",
    u"高等专科": "职业技术",
    u"技工": "职业技术",
    u"师专": "职业技术",
    u"工专": "职业技术",
    u"专科": "职业技术",
    u"青鸟": "职业技术",
    u"五月花": "职业技术",
    u"高专": "职业技术",

    u"驾校": "特殊技能",

    u"进修": "进修",
    u"继续教育": "进修",
    u"研修": "进修",
    u"自修": "进修",
    u"专修": "进修",
    u"培训": "进修",
    u"自学": "进修",
    u"自考": "进修",
    u"函授": "进修",
    u"成人": "进修",
    u"网络教育": "进修",
    u"网教": "进修",
    u"远程": "进修",
    u"网校": "进修",

    u"中学": "中学以下",
    u"高中": "中学以下",
    u"高级中学": "中学以下",
    u"职业高中": "中学以下",

    u"中专": "中学以下",
    u"中等专业": "中学以下",
    u"初中": "中学以下",
    u"初级中学": "中学以下",

    u"小学": "中学以下",

}

school_cate_map_dict = {
    "国外": 'oversea',
    "大学": "university",
    "港澳台": 'gangaotai',
    "党政": "party",
    "军队院校": "army",
    "学院": "college",
    "进修": "up",
    "职业技术": "prof_tech",
    "中学以下": "high_school",

}

school_feature_words_keys = school_feature_words_dict.keys()
# print '\n'.join(school_feature_words_keys)
shcool_cates = school_cate_map_dict.values()


def mark_school_cls(school):
    """
    @summary:判断是否为一个学校或者组织
    """
    school_dict = {}

    if not school:
        return school_dict
    is_school = False
    school_lower = school.lower()

    for school_keyword in school_feature_words_keys:
        cate_value = school_feature_words_dict.get(school_keyword)
        cate_cls = school_cate_map_dict.get(cate_value)

        if len(school_keyword) and school_keyword in school_lower:
            school_dict[cate_cls] = cate_value.decode('utf-8')
        # is_a_org = True
        elif school_dict.get(cate_cls):
            continue
        else:
            school_dict[cate_cls] = ''

    seg_words = list(pseg.cut(school))
    marked_school = []
    others = []
    flags = [word.flag for word in seg_words]
    #     words = [ word.word for word in seg_words]

    seg_school = ''

    for word in seg_words:
        if word.flag == 'school' or word.flag == 'nt':
            marked_school.append(word.word)
            seg_school = word.word
        else:
            others.append(word.word)
            #         print word.word

    if marked_school:
        school_dict['marked_school'] = ','.join(marked_school)
        school_dict['unmarked_school'] = ''
    else:
        school_dict['unmarked_school'] = school.strip()

    if 'x' not in flags and is_school:
        school_dict['is_org'] = school

    school_dict['school'] = school.strip()
    school_dict['others'] = '=='.join(others)
    level = school_level_dict.get(seg_school)
    if level and len(level) > 2 and not school_dict['college'] and not school_dict['up']:
        school_dict['school_level'] = level
    elif school_dict['gangaotai'] or u'中科院' in school or u'中国科学院' in school:
        school_dict['school_level'] = u'中国一流大学'
    elif school_dict['oversea']:
        school_dict['school_level'] = u'国外大学'
    elif school_dict['army'] or school_dict['party']:
        school_dict['school_level'] = u'党政军大学'
    elif (level and len(level) > 0 and school_dict['university']) or (u"理工" in school and not school_dict['up']):
        school_dict['school_level'] = u'普通大学'
    elif (school_dict['college'] and not school_dict['prof_tech']) or school_dict['university']:
        school_dict['school_level'] = u'普通二本学院'
    elif u'中' in school and not (school_dict['college'] or school_dict['university']):
        school_dict['school_level'] = u'中学以下'
    else:
        school_level_line = u"%s%s%s%s%s" % (school_dict['up'], school_dict['university'], school_dict['college'],
                                             school_dict['prof_tech'], school_dict['high_school'])
        #         print type(school_level_line),school_level_line
        school_dict['school_level'] = school_level_line

    return school_dict


if __name__ == '__main__':
    schools = [
        u'韩国公州大学',
        u"北京大学",
        u"法国图尔大学工程师学院",
        u'上海国际经济技术进修学院'

    ]
    import json

    for school in schools:
        school_dict = mark_school_cls(school)
        print json.dumps(school_dict, ensure_ascii=False, indent=4)
