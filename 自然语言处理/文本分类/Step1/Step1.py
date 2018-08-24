from nltk import *

with open('../datas/train_set.csv','r',encoding='utf8') as f:
    lines = f.readlines()

labels = [int(label[3]) for line in lines for label in line.split(',')]
#获取所有的字
#words = [word for line in lines for word in line.split(',')[1].split(' ')]
#print('total words:{},distinct words:{}'.format(len(words),len(set(words))))
#total words:120390274,distinct words:13517
#所有不重读的字个数为13517，由此推断很可能是由汉字组成。因此要进行embedding词嵌入
#统计高频词和低频词
#fdist = FreqDist(words)
#fdist.plot(50)
#去掉低频词和高频词
#hapaxes = fdist.hapaxes()
#print('低频词个数：{}'.format(len(hapaxes)))
#most_common = fdist.most_common()
#res = [most_common[i] for i in range(10)]
#res_key = [i[0] for i in res]
#res_values = [i[1] for i in res]
#print('高频词：{}，出现次数：{}'.format(res_key,sum(res_values)))
#total words:120390274,distinct words:13517
#低频词个数：2322
#高频词：['1044285', '7368', '856005', '72195', '195449', '359838', '239755', '427848', '316564', '1077049']，出现次数：20926458

#所有词信息
#words = [word for line in lines for word in line.split(',')[1].split(' ')]
#print('total words:{},distinct words:{}'.format(len(words),len(set(words))))
#total words:73327967,distinct words:875130
#统计高频词和低频词
#fdist = FreqDist(words)
#fdist.plot(50)
#去掉低频词和高频词
#hapaxes = fdist.hapaxes()
#print('低频词个数：{}'.format(len(hapaxes)))
#most_common = fdist.most_common()
#res = [most_common[i] for i in range(10)]
#res_key = [i[0] for i in res]
#res_values = [i[1] for i in res]
#print('高频词：{}，出现次数：{}'.format(res_key,sum(res_values)))
#total words:73327967,distinct words:875130
#低频词个数：408165
#高频词：['520477', '816903', '1033823', '995362', '920327', '834740', '460600', '54111', '1226448', '1025743']，出现次数：18759821  

#查看平均文章长度
#articles = len(lines)
#mean_article_len = len(words) / float(articles)
#print('mean_article_len:{}'.format(mean_article_len))
#mean_article_len:1177.088660317957

