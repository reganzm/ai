import jieba

sent = '中文分词是文本处理不可或缺的一步！'

seg_list = jieba.cut(sent, cut_all=True)

print('全模式：', '/ ' .join(seg_list)) 

seg_list = jieba.cut(sent, cut_all=False)
print('精确模式：', '/ '.join(seg_list)) 

seg_list = jieba.cut(sent)  
print('默认精确模式：', '/ '.join(seg_list))

seg_list = jieba.cut_for_search(sent)  
print('搜索引擎模式', '/ '.join(seg_list))


import jieba.posseg as psg

sent = '中文分词是文本处理不可或缺的一步！'

seg_list = psg.cut(sent)

print(' '.join(['{0}/{1}'.format(w, t) for w, t in seg_list]))

import jieba 
#加载系统词典
jieba.set_dictionary('./data/dict.txt.big')

print('自定义词典内容：')
with open('./data/user_dict.utf8', 'r') as f:
    for l in f:
        print(l)

print('------华丽的分割线-------')
sent = 'jieba分词非常好用，可以自定义金融词典！'
seg_list = jieba.cut(sent)
print('加载词典前:', '/ '.join(seg_list))

jieba.load_userdict('./data/user_dict.utf8')
seg_list = jieba.cut(sent)
print('加载词典后:', '/ '.join(seg_list))

import jieba
sent = '好丑的证件照片'
print('/ '.join(jieba.cut(sent, HMM=False)))

jieba.suggest_freq(('证件照片'), True)
print('/ '.join(jieba.cut(sent, HMM=False)))

import jieba.analyse as aly

content = '''
自然语言处理（NLP）是计算机科学，人工智能，语言学关注计算机和人类（自然）语言之间的相互作用的领域。
因此，自然语言处理是与人机交互的领域有关的。在自然语言处理面临很多挑战，包括自然语言理解，因此，自然语言处理涉及人机交互的面积。
在NLP诸多挑战涉及自然语言理解，即计算机源于人为或自然语言输入的意思，和其他涉及到自然语言生成。
'''

#加载自定义idf词典
aly.set_idf_path('./data/idf.txt.big')
#加载停用词典
aly.set_stop_words('./data/stop_words.utf8')

# 第一个参数：待提取关键词的文本
# 第二个参数：返回关键词的数量，重要性从高到低排序
# 第三个参数：是否同时返回每个关键词的权重
# 第四个参数：词性过滤，为空表示不过滤，若提供则仅返回符合词性要求的关键词
keywords = aly.extract_tags(content, topK=10, withWeight=True, allowPOS=())

for item in keywords:
    # 分别为关键词和相应的权重
    print(item[0], item[1])
    
import jieba.analyse as aly

content = '''
自然语言处理（NLP）是计算机科学，人工智能，语言学关注计算机和人类（自然）语言之间的相互作用的领域。
因此，自然语言处理是与人机交互的领域有关的。在自然语言处理面临很多挑战，包括自然语言理解，因此，自然语言处理涉及人机交互的面积。
在NLP诸多挑战涉及自然语言理解，即计算机源于人为或自然语言输入的意思，和其他涉及到自然语言生成。
'''
# 第一个参数：待提取关键词的文本
# 第二个参数：返回关键词的数量，重要性从高到低排序
# 第三个参数：是否同时返回每个关键词的权重
# 第四个参数：词性过滤，为空表示过滤所有，与TF—IDF不一样！
keywords = jieba.analyse.textrank(content, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
for item in keywords:
    # 分别为关键词和相应的权重
    print(item[0], item[1])