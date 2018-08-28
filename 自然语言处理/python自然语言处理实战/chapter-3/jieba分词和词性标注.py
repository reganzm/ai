#jieba分词示例
def get_content(path):
    
    with open(path, 'r', encoding='gbk', errors='ignore') as f:
        content = ''
        for l in f:
            l = l.strip()
            content += l
        return content


def get_TF(words, topK=10):
    
    tf_dic = {}
    for w in words:
        tf_dic[w] = tf_dic.get(w, 0) + 1
    return sorted(tf_dic.items(), key = lambda x: x[1], reverse=True)[:topK]

def stop_words(path):
    with open(path,'r',encoding='utf8') as f:
        return [l.strip() for l in f]
stop_words('./data/stop_words.utf8')

#分词
def main1():
    import glob
    import random
    import jieba
    
    files = glob.glob('./data/news/C000013/*.txt')
    corpus = [get_content(x) for x in files[:5]]
    
    
    sample_inx = random.randint(0, len(corpus))
    sample_inx = 3
    
    import jieba.posseg as psg
    
    split_words = [x for x in jieba.cut(corpus[sample_inx]) if x not in stop_words('./data/stop_words.utf8')]
    print('样本之一：'+corpus[sample_inx])
    print('样本分词效果：'+'/ '.join(split_words))
    print('样本的topK（10）词：'+str(get_TF(split_words)))
main1()


#jieba词性标注示例

def main():
    import glob
    import random
    import jieba
    import jieba.posseg as psg
    
    files = glob.glob('./data/news/C000013/*.txt')
    corpus = [get_content(x) for x in files]
    
    sample_inx = random.randint(0, len(corpus))
    sample_inx = 3
    
    split_words = [w for w, t in psg.cut(corpus[sample_inx]) 
                   if w not in stop_words('./data/stop_words.utf8')
                  and t.startswith('n')]
    print('样本之一：'+corpus[sample_inx])
    print('样本分词效果：'+'/ '.join(split_words))
    print('样本的topK（10）词：'+str(get_TF(split_words)))
main()