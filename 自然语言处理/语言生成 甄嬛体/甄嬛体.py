import sys
import os
import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import sys
import math
import tflearn
import chardet
import numpy as np
import struct


#with open('zhenhuanzhuan.txt','r',encoding='utf8') as f:
    #lines = [line.strip() for line in f.readlines() if line.strip()]
##print(lines[:10])
#res = jieba.cut(" ".join(lines))
#cut_res = " ".join([i for i in res])
#with open('zhenhuanzhuan_seg','w',encoding='utf8') as f:
    #f.write(cut_res)

#训练模型
sentences = LineSentence('zhenhuanzhuan_seg')
#size：词向量的维度
#window：上下文环境的窗口大小
#min_count：忽略出现次数低于min_count的词
model = Word2Vec(sentences, size=200, window=5, min_count=5, workers=10,compute_loss=True,iter=5,sg=0,hs=0)
model.save('zhenhuanzhuan_w2v.model')
model.wv.save_word2vec_format('zhenhuanzhuan_w2v.txt')

seq = []

max_w = 50
float_size = 4
word_vector_dict = {}

def load_vectors(input_file):
    """
    从vectors.bin加载词向量，返回一个word_vector_dict的词典，key是词，value是200维的向量
    """
    print ("begin load vectors")

    with open(input_file,'r',encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            tt = line.split(' ')
            if(len(tt)==201):
                word_vector_dict[tt[0].strip()] = [float(tt[i]) for i in range(1,201)]
            

def init_seq():
    """
    读取切好词的文本文件，加载全部词序列
    """
    file_object = open('zhenhuanzhuan_seg', 'r',encoding='utf8')
    vocab_dict = {}
    while True:
        line = file_object.readline()
        if line:
            for word in line.split(' '):
                if word_vector_dict.get(word):
                    seq.append(word_vector_dict[word])
        else:
            break
    file_object.close()

def vector_sqrtlen(vector):
    len = 0
    for item in vector:
        len += item * item
    len = math.sqrt(len)
    return len

def vector_cosine(v1, v2):
    if len(v1) != len(v2):
        sys.exit(1)
    sqrtlen1 = vector_sqrtlen(v1)
    sqrtlen2 = vector_sqrtlen(v2)
    value = 0
    for item1, item2 in zip(v1, v2):
        value += item1 * item2
    return value / (sqrtlen1*sqrtlen2)


def vector2word(vector):
    max_cos = -10000
    match_word = ''
    for word in word_vector_dict:
        v = word_vector_dict[word]
        cosine = vector_cosine(vector, v)
        if cosine > max_cos:
            max_cos = cosine
            match_word = word
    return (match_word, max_cos)

def main():
    load_vectors("./zhenhuanzhuan_w2v.txt")
    init_seq()
    xlist = []
    ylist = []
    test_X = None
    #for i in range(len(seq)-100):
    for i in range(100):
        sequence = seq[i:i+20]
        xlist.append(sequence)
        ylist.append(seq[i+20])
        if test_X is None:
            test_X = np.array(sequence)
            (match_word, max_cos) = vector2word(seq[i+20])
            print(seq[i+20])
            print ("right answer=", match_word, max_cos)

    X = np.array(xlist)
    Y = np.array(ylist)
    net = tflearn.input_data([None, 20, 200])
    net = tflearn.lstm(net, 200)
    net = tflearn.fully_connected(net, 200, activation='linear')
    net = tflearn.regression(net, optimizer='sgd', learning_rate=0.1,
                                     loss='mean_square')
    model = tflearn.DNN(net)
    model.fit(X, Y, n_epoch=500, batch_size=100,snapshot_epoch=True,show_metric=True)
    model.save("model")
    predict = model.predict([test_X])
    (match_word, max_cos) = vector2word(predict[0])
    print( "predict=", match_word, max_cos)
    test_X = test_X.tolist()
    start_word = [test_X]
    for i in range(10):
        predict = model.predict(start_word)
        print('predict.shape:',predict.shape,type(predict))
        (match_word, max_cos) = vector2word(predict[0])
        print( "predict=", match_word, max_cos)
        test_X = test_X[1:]+predict.tolist()
        start_word = [test_X]
main()