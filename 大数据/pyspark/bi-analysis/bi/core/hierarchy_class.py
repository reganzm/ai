# coding:utf-8
"""
Created on 2016-07-05 18:26:07

@author: likaiguo
"""
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
import re
from collections import OrderedDict, defaultdict, Counter

from settings import BASE_DIR as PROJECT_ROOT


def pretty_print_dict(data={}):

    print(json.dumps(data, ensure_ascii=False, indent=4))


def list_to_dict(lst, key_affix='key_', idx=None, feature_idx=None):
    """
    将列表数据转换为字典,并且按照顺序进行赋予键值,id
    key_affix: 指定键名前缀
    idx: 添加id字段
    feature_idx: 从lst数据中选出一个数据作为特征

    >>> list_to_dict(range(3))
    OrderedDict([(u'key_1', 0), (u'key_2', 1), (u'key_3', 2)])
    """
    d = OrderedDict(zip(["%s%d" % (key_affix, i + 1) for i in xrange(len(lst))], lst))
    if idx:
        d['id'] = idx
    if feature_idx:
        d['feature'] = lst[feature_idx]

    return d


def traverse_leaf_nodes(data, id_start=1, margin=100, parent=None, key_affix='key_'):
    """
    递归获取层次标注数据: json 和 yaml类似的层级嵌套,将其转为字典编号列表
    如: d = {1: {2:[3,4]},11:{3:4}}
       key_1 key_2  key_3
    1  1
    100 1  2
    100001  1     2     3
    100002  1    2      4
    2   11
    200  11 3
    200001  11   3     4
    """

    if isinstance(data, dict):
        if not parent:
            parent = []
        results = []
        for i, (key, item) in enumerate(data.items(), id_start):
            new_parent = parent + [key]
            new_data = list_to_dict(new_parent, idx=i, feature_idx=-1)
            results.append(new_data)
            leaf_results = traverse_leaf_nodes(item, i * margin, parent=new_parent)
            results.extend(leaf_results)
        return results
    elif isinstance(data, list) or isinstance(data, tuple):
        results = []
        for i, item in enumerate(data, 1):
            new_data = traverse_leaf_nodes(item, id_start + i, parent=parent)
            results.append(new_data)
        return results
    else:
        lst = parent + [data]
        new_data = list_to_dict(lst, idx=id_start, feature_idx=-1)
        return new_data


def ishan(text):
    """
    判断是否含全部为汉字
    # for python 2.x, 3.3+
    >>> ishan(u'一')
    True
    >>> ishan(u'我&&你')
    False
    """
    return all(u'\u4e00' <= char <= u'\u9fff' for char in text)


def bag_of_words(words, ngram=[1, 2], return_tuple=False):
    """
    产生词袋
    >>> bag_of_words('I am li kai guo ')
    [u'I', u'am', u'li', u'kai', u'guo', u'Iam', u'amli', u'likai', u'kaiguo']
    """
    results = []
    if not isinstance(ngram, (tuple, list, set)):
        return results

    if isinstance(words, (str, unicode)):
        # 中英文分割
        new_words = []
        for w in words:
            new_words.append(w)
            if ishan(w):
                new_words.append(' ')
        words = "".join(new_words).strip().split()

    for n in ngram:
        if len(words) < n:
            continue
        tmp = []
        for i in xrange(n):
            tmp.append(words[i:])
        results.extend(zip(*tmp))
    if return_tuple:
        return results
    else:
        return [''.join(t) for t in results]


class HierarchyMarker(object):
    """
    层级标注器
    """

    def __init__(self,
                 data=traverse_leaf_nodes(
                     json.loads(open(os.path.join(PROJECT_ROOT, 'bi', 'areas.json'), 'r').read())),
                 ngram=None,
                 feature_relace_regex='省|市|区|县|乡| ',
                 clean_regex='\.|\-|\,|\\|\/'
                 ):
        """
        ngram 表示特征值切分方法,默认不做多余特征. 词袋可选: ngram=[1,],[1,2]等
        """
        self.data = data
        self.ngram = ngram or None
        self.cate_idx_dict = OrderedDict()
        self.cate_feature_dict = defaultdict(list)

        if feature_relace_regex:
            self.feature_relace_regex = re.compile(feature_relace_regex)
        if clean_regex:
            self.clean_regex = re.compile(clean_regex)

        self.convert_for_search()

    def convert_for_search(self):
        """
        有问题,不同层级的关键词会有冲突
        """

        for d in self.data:
            idx = d['id']
            feature = d['feature']
            if idx not in self.cate_idx_dict:
                self.cate_idx_dict[idx] = d
            else:
                msg = '%d has exists: %s ' % (idx, self.cate_idx_dict[idx])
                print(msg)
                pretty_print_dict(data=d)
                raise

            if feature in '其他 其它':
                continue

            self.cate_feature_dict[feature].append(idx)
            if self.feature_relace_regex:
                new_feature = self.feature_relace_regex.sub('', feature)
                self.cate_feature_dict[new_feature].append(idx)

            if self.ngram:
                bag_words = bag_of_words(words=feature, ngram=self.ngram)
                for w in bag_words:
                    self.cate_feature_dict[w].append(idx)

    def find_by_id(self, idx):
        """
        根据传入idx查询对应的数据,
        idx可以是单个键, 返回单个值
        也可以是迭代器 迭代器返回列表
        """
        if isinstance(idx, (list, set)):
            return [self.cate_idx_dict.get(i) for i in idx if self.cate_idx_dict.get(i)]

        return self.cate_idx_dict.get(idx)

    def find(self, feature, smart=False, ngram=(2,), merge=True, return_one=True,
             set_keys=None
             ):
        """
        merge: 自动合并多级. 如果同时存在父级和子级,合并父级
        set_keys: 重命名 键名. keys可以设置为 字符串, 如: area --> keys_1 --> area_1;
                    或列表: 如: [province,city,district] 省市区 替换原有 key1,key2,key3
        """
        if self.clean_regex:
            feature = self.clean_regex.sub(' ', feature)

        all_idx = []
        temp_feature_set = set()

        words = []
        if smart and ngram:
            bow = bag_of_words(words=feature, ngram=ngram or self.ngram)
            words.extend(bow)

        words.extend(feature.split())

        for w in words:
            if w in temp_feature_set:
                continue
            else:
                temp_feature_set.add(w)
            lst = self.cate_feature_dict.get(w)
            if lst:
                all_idx.extend(lst)

        if feature not in temp_feature_set:
            d = self.cate_feature_dict.get(feature)
            if d:
                all_idx.extend(d)

        results = []
        if all_idx:
            if self.feature_relace_regex:
                # 清洗掉一部分不重要的字/词
                feature = self.feature_relace_regex.sub('', feature)
            counter = Counter(all_idx)
            # 重新影响排序

            for idx, _ in counter.most_common():
                if merge:
                    has_sub = False
                    for may_sub_idx in set(all_idx):
                        may_sub_idx_str, idx_str = str(may_sub_idx), str(idx)
                        if may_sub_idx > 100 and (may_sub_idx > idx) and may_sub_idx_str.startswith(idx_str):
                            has_sub = True
                            break
                    if has_sub:
                        continue

                res = self.find_by_id(idx=idx)
                if res:
                    values = "".join([v for k, v in res.items() if isinstance(v, (unicode, str)) and k != 'feature'])
                    count_feature = 0
                    for f in feature:
                        if f in values:
                            count_feature += 1
                    if count_feature == len(feature):
                        results.append(res)

        if set_keys and results:
            new_results = []
            for res in results:
                new_res = OrderedDict()
                for k, v in res.items():
                    new_key = k
                    if k.startswith('key_'):
                        k, idx = k.split('_')
                        if isinstance(set_keys, (str, unicode)):
                            new_key = '%s_%s' % (set_keys, idx)
                        elif isinstance(set_keys, list):
                            if int(idx) <= len(set_keys):
                                new_key = set_keys[int(idx) - 1]
                    new_res[new_key] = v
                new_results.append(new_res)

            results = new_results

        if results and (len(results) == 1 or return_one):
            return results[0]

        return results

if __name__ == '__main__':

    import doctest
    doctest.testmod()
    data = json.loads(open('areas.json', 'r').read())
    results = traverse_leaf_nodes(data)

    import pandas as pd
    df2 = pd.DataFrame(results)
    print(df2.head(10))
    df2.to_csv('areas.csv', encoding='utf-8')
    import yaml
    print(yaml.dump(data))
