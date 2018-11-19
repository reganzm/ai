# coding=utf-8
import json
import re
import sys


def get_recent_work_expr(resume_json, count=1):
    work_expr = resume_json.get('workExperience', [])
    return work_expr[:count]


def get_recent_salary(resume_json):
    digit_regex = re.compile("\d{1,10}")
    salary = [0, 0]
    origin_current_salary = resume_json.get('latestSalary', None)
    if origin_current_salary:
        salary_nums = digit_regex.findall(origin_current_salary)
        if u'以下' in origin_current_salary:
            salary = int(salary_nums[0]) * 10000 / 12
            salary = [salary / 2, salary]
        elif u'以上' in origin_current_salary:
            salary = int(salary_nums[0]) * 10000 / 12
            salary = [salary, salary * 2]
        elif len(salary_nums) == 2:
            if origin_current_salary.find(u'元/月') > 0:
                salary = int(salary_nums[0]) * int(salary_nums[1]) / 12
                salary = [salary, salary]
            else:
                salary = [int(i) * 10000 / 12 for i in salary_nums]
        else:
            salary = [0, 0]
    else:
        for work_expr in get_recent_work_expr(resume_json):
            origin_salary = work_expr.get('salary', None)
            if origin_salary:
                salary = digit_regex.findall(origin_salary)
                if len(salary) == 2:
                    salary = [int(i) for i in salary]
                elif len(salary) == 1:
                    salary = int(salary[0])
                    if u'下' in origin_salary:
                        salary = [salary / 2, salary]
                    elif u'上' in origin_salary:
                        salary = [salary, salary * 2]
                    else:
                        salary = [0, 0]
                else:
                    salary = [0, 0]
    return salary


def get_edu(resume_json):
    edu_expr_list = resume_json.get('educationExperience', [])
    for edu_expr in edu_expr_list:
        return edu_expr['degree'], edu_expr['school']
    return None, None


def get_recent_position_title(resume_json):
    work_expr_list = resume_json.get('workExperience', [])
    for work_expr in work_expr_list:
        return work_expr['positionTitle'], work_expr['companyCatagory'], work_expr['industryCatagory']
    return None, None, None

key_list = ['city', 'work_len', 'age', 'edu_degree', 'school', 'position_title',
    'company_cate', 'industry_cate', 'birthday', 'gender', 'lower_salary', 'upper_salary']


def extract_data(resume_json):
    imp_info = {}
    addr = resume_json.get('address', None)
    if addr:
        city = addr.split(' ')[0]
    else:
        city = None
    imp_info['city'] = city
    imp_info['work_len'] = resume_json['workExperienceLength']
    imp_info['age'] = resume_json['age']
    imp_info['edu_degree'], imp_info['school'] = get_edu(resume_json)
    imp_info['position_title'], imp_info['company_cate'], imp_info[
        'industry_cate'] = get_recent_position_title(resume_json)
    imp_info['birthday'] = resume_json.get('birthday', None)
    imp_info['gender'] = resume_json.get('gender', None)
    salary_scope = get_recent_salary(resume_json)
    # print salary_scope
    if salary_scope[0] > 0 and salary_scope[1] > 0:
        imp_info['lower_salary'] = salary_scope[0]
        imp_info['upper_salary'] = salary_scope[1]
    for k in key_list:
        if k not in imp_info or imp_info[k] == None:
            return None
    return imp_info

if __name__ == '__main__':
    for line in open(sys.argv[1]):
        resume_json = json.loads(line)
        talent_info = extract_data(resume_json)
        if talent_info:
            print json.dumps(talent_info)
