# coding=utf-8
import json
import re
import sys


def edu_degree_to_int(edu_degree):
    degree_to_int_dict = {u'高中': 0, u'大专': 1, u'本科': 2, u'硕士': 3, u'博士': 3, u'mba': 3, u'mba/emba': 3}
    edu_degree = edu_degree.lower()
    if edu_degree in degree_to_int_dict:
        return degree_to_int_dict[edu_degree]
    return 0


def company_cate_to_int(company_cate):
    company_cate_dict = {
        u'其他': 0,
        u'代表处': 0,
        u'国家机关': 1,
        u'政府机关': 1,
        u'事业单位': 1,
        u'国企': 2,
        u'国有企业': 2,
        u'合资': 3,
        u'中外合营': 3,
        u'上市公司': 3,
        u'股份制企业': 3,
        u'民营': 4,
        u'外商独资': 5,
        u'外企': 5
    }
    for k in company_cate_dict:
        if company_cate.find(k) >= 0:
            return company_cate_dict[k]
    return 0

school_dict = None


def school_to_int(school):
    school = school.strip()
    sint = 0
    if school in school_dict:
        stype = school_dict[school]
        if stype == u'211':
            sint = 1
        elif stype == u'985':
            sint = 2
        else:
            sint = 0
    return sint\



def city_to_int(city):
    city_dict = {u'成都': 1, u'上海': 2, u'北京': 3}
    for t in city_dict:
        if city.find(t) >= 0:
            return city_dict[t]
    return 0


def get_birthmonth(birthday):
    m = re.search(u'([0-9]+)月', birthday)
    month = int(m.groups()[0])
    return month


def gender_to_int(gender):
    if gender.strip() == u'女':
        return 1
    return 0


def normalize_worklen(worklen):
    if worklen <= 2:
        return 1
    elif worklen < 5:
        return 2
    elif worklen < 8:
        return 3
    return 4

rd_title_keys = ['数据挖掘', '架构', '服务器', '服务端', '程序', '主程', '工程',
'架构', 'java', 'php', 'android', '算法', '前端', '移动端', '后台', 'linux',
'ruby', 'web', '开发', '工程师', '研发', '软件', '架构', '客户端', 'flash', 'c++']

rd_negative_keys = ['测试', '主管', '技术支持', '运维', '售前', '售后', '数据库',
'计量', '销售', '供应商', '维修', '维护', '驻场', '经理', '需求', '管理', '运营', 'pm',
'建筑', '土建', '射频', '采购']

design_title_keys = ['原画', '设计', '美术', '绘画', '美工', '平面', '视觉', '艺术', '动画', '主美']
design_negative_keys = ['产品设计']

bd_title_keys = ['活动策划', '销售', '运营', '推广', 'bd', '市场', '营销']
bd_negative_keys = []

pm_title_keys = ['产品']
pm_negative_keys = ['测试']


def hit_negative_words(title, negative_keys):
    title = title.lower()
    for k in rd_negative_keys:
        if title.find(k) >= 0:
            return True
    return False


def is_target_position(title, title_keys, negative_keys):
    title = title.encode('utf-8').lower()
    for key in title_keys:
        if title.find(key) >= 0 and not hit_negative_words(title, negative_keys):
            return True
    return False


def position_to_int(title):
    if is_target_position(title, rd_title_keys, rd_negative_keys):
        return 1
    elif is_target_position(title, design_title_keys, design_negative_keys):
        return 2
    elif is_target_position(title, bd_title_keys, bd_negative_keys):
        return 3
    elif is_target_position(title, pm_title_keys, pm_negative_keys):
        return 4
    return 0


def to_vector(salary_info):
    salary_info['edu_degree'] = edu_degree_to_int(salary_info['edu_degree'])
    salary_info['school'] = school_to_int(salary_info['school'])
    salary_info['company_cate'] = company_cate_to_int(salary_info['company_cate'])
    salary_info['city'] = city_to_int(salary_info['city'])
    salary_info['month'] = get_birthmonth(salary_info['birthday'])
    salary_info['gender'] = gender_to_int(salary_info['gender'])
    salary_info['work_len'] = normalize_worklen(salary_info['work_len'])
    salary_info['pt'] = position_to_int(salary_info['position_title'])
    return salary_info


def load_school_dict(filepath):
    school_dict = {}
    for line in open(filepath):
        elems = line.strip().split(',')
        if len(elems) == 2:
            elems[0] = elems[0].decode('utf-8')
            elems[1] = elems[1].decode('utf-8')
            school_dict[elems[0]] = elems[1]
    return school_dict


def get_salary_scope(lower_salary, upper_salary):
    mid_salary = (lower_salary + upper_salary) / 2
    return mid_salary

if __name__ == '__main__':
    school_dict = load_school_dict('./dict/college.csv')
    for line in open(sys.argv[1]):
        salary_info = json.loads(line)
        salary_info = to_vector(salary_info)
        salary_info['salary_scope'] = get_salary_scope(salary_info['lower_salary'], salary_info['upper_salary'])
        if salary_info['city'] > 0 \
        and salary_info['pt'] > 0:
            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
            (salary_info['salary_scope'], salary_info['upper_salary'],
            salary_info['edu_degree'], salary_info['school'],
            salary_info['work_len'], salary_info['city'],
            salary_info['gender'], salary_info['pt'],
            salary_info['company_cate'], salary_info['position_title'].encode('utf-8'))
