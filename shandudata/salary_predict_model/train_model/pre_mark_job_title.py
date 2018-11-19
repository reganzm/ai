# coding: utf-8

import json

import codecs
import jieba
import os
import pandas as pd

from jieba_pro import add_user_words
from settings import RESOURCES


def load_classify_data(fpath, MARGIN=100):
    """
    @summary:按照固定格式做数据分级处理,返回分级字典
    #文本格式
    >>一级标题名(first_class_index)
    二级名称(second_class_index)
    三级关键词1(second_class_index)  三级关键词2 三级关键词3
    #返回字典格式
    {关键词:idx}
    idx规则:
    first_class_index 按照自然顺序增长
    second_class_index:每个小块按照自然顺序增长,实际产生index = first_class*MARGIN
    third_class_index:顺序横行增长,实际产生index= (first_class*MARGIN + second_class_index)*MARGIN + third_class_index
    #实例:
    {
        "一级标题名":1,
        "二级名称":1*100+1,
        "三级关键词1":(1*100+1)*100+1,
        "三级关键词2":(1*100+1)*100+2,
        "三级关键词2":(1*100+1)*100+3,
    }
    #关于分级:原本程序可以设计成无限级分层,但是考虑到实际意义,
    #现有100*100*100=100万个词可以cover到了,所以,再做更多的级无意义

    #注意第一大类不能大于100,第二大类,不能大于9999
    """
    job_cate_lines = codecs.open(fpath, 'r', "utf-8").readlines()

    job_cate_tree = {}
    first_class_index = 1
    second_class_index = 1
    third_class_index = 1

    total_lines = len(job_cate_lines)
    for i, line in enumerate(job_cate_lines):
        if '###' in line:
            continue

        keywords = line.split()
        keywords_len = len(keywords)
        next_line_num = i + 1

        if '>>' in line and keywords_len == 1:
            first_class = line.replace('>>', '').strip()
            job_cate_tree[first_class] = first_class_index
        elif keywords_len == 1:
            if job_cate_tree.get(line.strip()):
                second_class = '%s_%s' % (first_class, line.strip())
            else:
                second_class = line.strip()
            job_cate_tree[second_class] = first_class_index * MARGIN + second_class_index
        elif keywords_len > 1:
            for keyword in keywords:
                real_third_index = (first_class_index * MARGIN + second_class_index) * MARGIN + third_class_index
                if not job_cate_tree.get(keyword.strip()):
                    job_cate_tree[keyword.strip()] = real_third_index
                else:
                    # print keyword, job_cate_tree.get(keyword.strip()), 'has existed so added but with prefix!'
                    job_cate_tree["%s_%s" % (second_class, keyword.strip())] = real_third_index
                third_class_index += 1
            third_class_index = 1
            second_class_index += 1
        elif next_line_num < total_lines and ">>" in job_cate_lines[next_line_num]:
            first_class_index += 1
            second_class_index = 1
            third_class_index = 1
        elif not line.strip() and next_line_num < total_lines - 1 and len(job_cate_lines[next_line_num].strip()) > 0:
            second_class_index += 1
    return job_cate_tree


# job_cate_tree = load_classify_data(fpath=CUR_PATH + '/lagou-job-class-20141215.txt')
PATH = os.path.join(RESOURCES, "job/pinbot-job-class-20150416.txt")
# job_cate_tree = load_classify_data(fpath=CUR_PATH + '/pinbot-job-class-20150416.txt')
job_cate_tree = load_classify_data(fpath=PATH)
add_user_words(job_cate_tree.keys())

job_title_tree_tuple = [(str(idx), keyword) for keyword, idx in job_cate_tree.items()]
job_cate_tree_tuple_sorted = sorted(job_cate_tree.items(), key=lambda tup: str(tup[1]))
for keyword, idx in job_cate_tree_tuple_sorted:
    print(idx, keyword)

# list(pseg.cut('运维工程师 运维开发工程师 网络工程师 系统工程师 IT支持 IDC CDN F5 系统管理员 病毒分析 WEB安全 网络安全 系统安全 运维经理 运维其它'))


job_cate_tree_index2keywords = {index: keyword for keyword, index in job_cate_tree.items()}
# print(json.dumps(job_cate_tree_index2keywords, ensure_ascii=False, indent=2, sort_keys=True))
job_cate_tree_keywords_lower = {keyword.lower(): index for keyword, index in job_cate_tree.items()}
add_user_words(words=job_cate_tree_keywords_lower.keys())


def transform_uniform(word):
    index = job_cate_tree_keywords_lower.get(word, 0)
    return job_cate_tree_index2keywords.get(index, word)


def mark_job_cls(position_title, print_it=False):
    """
    @summary:标记一个职位名称的类别,分三级,参考词典
    """
    if isinstance(position_title, str):
        position_title = position_title.decode('utf-8', 'ignore')

    word_dict = {
        'first_class': '',
        'first_class_1': '',
        'first_class_2': '',
        '2nd_class': '',
        '2nd_class_1': '',
        '2nd_class_2': '',
        '2nd_class_3': '',
        '3rd_class': '',
        '3rd_class_1': '',
        '3rd_class_2': '',
        '3rd_class_3': '',
        '3rd_class_4': '',
        'unknown': '',
        'full_cut': '',
        'raw_text': position_title}

    if not isinstance(position_title, float):
        position_title_cuts = [transform_uniform(word) for word in jieba.cut_for_search(position_title)]
        word_dict['full_cut'] = '|'.join(position_title_cuts)

        position_title_cuts.append(position_title)
        #     print position_title,type(position_title),isinstance(position_title,float),word_dict['full_cut']
        #         position_title_with_flag = pseg.cut(position_title_lower)

        unknown_keywords = []
        first_class, second_class, third_class = [], [], []
        unique_keyword_cate = set()
        for word in position_title_cuts:
            index = job_cate_tree.get(word, 0)
            if word in unique_keyword_cate or not word.strip():
                continue
            else:
                unique_keyword_cate.add(word)
                #         print index,word
            if index > 10000:
                third = job_cate_tree_index2keywords.get(index)
                third_class.append(third)
                second_class.append(job_cate_tree_index2keywords.get(index / 100))
                first_class.append(job_cate_tree_index2keywords.get(index / (100 * 100)))
            elif index > 100:
                second_class.append(job_cate_tree_index2keywords.get(index))
                first_class.append(job_cate_tree_index2keywords.get(index / 100))
            elif index >= 1:
                #             print job_cate_tree.get(index),index,word.word
                first_class.append(job_cate_tree_index2keywords.get(index))
            else:
                unknown_keywords.append(word)
        # print word_dict
        print(word_dict['full_cut'], index, word)
        print(first_class, second_class, third_class, unknown_keywords)
        word_dict['3rd_class'] = '|'.join(third_class)
        word_dict['2nd_class'] = '|'.join(second_class)
        word_dict['first_class'] = '|'.join(first_class)
        word_dict['unknown'] = '|'.join(unknown_keywords)

        def mark_detail(keywords, prefix):
            for i, word in enumerate(keywords[:4]):
                word_dict['%s_%d' % (prefix, i + 1)] = word

        mark_detail(third_class, '3rd_class')
        mark_detail(second_class, '2nd_class')
        mark_detail(first_class, 'first_class')
    if print_it:
        print(word_dict, json.dumps(word_dict, ensure_ascii=False, indent=2, sort_keys=True))

    return word_dict


def main():
    position_title_median_df = pd.read_csv('old_data_works.csv', encoding='utf-8')
    position_title_median_df.head(5)
    position_titles = position_title_median_df['position_title']
    marked_position_title = []
    print(position_titles[3])
    for position_title in position_titles:
        print(position_title)
        if isinstance(position_title, float):
            word_dict = {'first_class': '',
                         '2nd_class': '',
                         '3rd_class': '',
                         'unknown': '',
                         'full_cut': '',
                         'raw_text': position_title}
            marked_position_title.append(word_dict)
        else:
            word_dict = mark_job_cls(position_title)
            marked_position_title.append(word_dict)

    position_title_marked_df = pd.DataFrame(marked_position_title)
    position_title_marked_df[position_title_marked_df['first_class'] != ''].to_csv(
        "position_title_marked_df.csv", encoding='utf-8')

    len(position_title_median_df)
    z = (position_title_median_df.T.append(position_title_marked_df.T)).T
    z['age'] = z['age'].astype('float')
    z['lower_salary'] = z['lower_salary'].astype('float')
    z['upper_salary'] = z['upper_salary'].astype('float')
    z['work_len'] = z['work_len'].astype('float')
    z[10:13]
    # z.groupby('first_class').median()
    z.dtypes
    z[z['first_class'] == u'技术'].groupby('3rd_class').median().to_csv(
        'work_type_first_class_tech_3rd_class_median.csv', encoding='utf-8')


if __name__ == '__main__':
    mark_job_cls(position_title='产品/品牌主管 ')
    #     main()
    job_titles = u'运维工程师 android开发 运维开发工程师 网络工程师 系统工程师 IT支持 IDC CDN F5 系统管理员 python java java工程师'.split()
    print(len(job_titles))
    for job_title in job_titles:
        d = mark_job_cls(job_title)
        print(job_title, json.dumps(d, ensure_ascii=False, indent=2, sort_keys=True))
