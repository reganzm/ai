# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr
import numpy as np
from BILSTMConfig import BILSTMConfig
from BILSTMModel import BILSTMModel
from datas.cnews_loader import read_category, read_vocab,fold_padding
from collections import Counter
try:
    bool(type(unicode))
except NameError:
    unicode = str

#base_dir = 'data/cnews'
#vocab_dir = os.path.join(base_dir, 'cnews.vocab.txt')

save_dir = 'checkpoints/bilstm'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class BILSTM:
    def __init__(self):
        self.config = BILSTMConfig()
        self.categories, self.cat_to_id = read_category()
        self.words = np.load('./datas/dict.npy')
        self.word_to_id = np.load('./datas/dict.npy').tolist()
        self.config.vocab_size = len(self.word_to_id.keys())
        self.model = BILSTMModel(self.config)
        
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型
        

    def predict(self, datas):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        #content = unicode(message)
        #data = [self.word_to_id[x] for x in content if x in self.word_to_id]
        #datas = [word for word in data if word is not None]
        data_ids = [[i for i in data if i is not None] for data in datas]
        data_0_seq_length = []
        data_big_than_seq_length = []
        for i in data_ids:
            if len(i) > self.config.seq_length:
                data_big_than_seq_length.append(fold_padding(i,self.config.seq_length))
            else:
                data_0_seq_length.append(i)
        
        feed_dict_0_seq_length = {
            self.model.x: kr.preprocessing.sequence.pad_sequences(data_0_seq_length, self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls_0 = self.session.run(self.model.pred_label, feed_dict=feed_dict_0_seq_length)
        res = [self.categories[i] for i in y_pred_cls_0]
        
        #预测length>config.seq_length的文章
        for doc in data_big_than_seq_length:
            feed_dic = {
                self.model.x: kr.preprocessing.sequence.pad_sequences(doc[0], self.config.seq_length),
                self.model.keep_prob: 1.0                
            }
            y_pred_cls_doc = self.session.run(self.model.pred_label, feed_dict=feed_dic)
            res_doc = [self.categories[i] for i in y_pred_cls_doc]  
            tmp = Counter(res_doc).most_common(1)[0][0]
            res.append(tmp)
        
        return res


if __name__ == '__main__':
    model = BILSTM()
    test_sets = np.load('./datas/test_docs.npy')
    import pandas as pd
    list1 = []
    list2 = []
    batch = 1000
    datas = []
    
    datas_0_seq_length = {}
    datas_gt_seq_length = {}
    
    for i in range(len(test_sets)):
        if len(test_sets[i]) > model.config.seq_length:
            datas_0_seq_length[i] = test_sets[i]
        else:
            datas_gt_seq_length[i] = test_sets[i]
    
    datas_0_seq_length_keys = list(datas_0_seq_length.keys())
    
    for i in range(len(datas_0_seq_length_keys)):
        list1.append(datas_0_seq_length_keys[i])
        if (len(datas)+1) % batch == 0:
            res = model.predict(datas)
            print(res)
            list2.extend(res)
            datas.clear()
        datas.append(datas_0_seq_length[datas_0_seq_length_keys[i]])
    
    if len(datas) > 0:
        res = model.predict(datas)
        print(res)
        list2.extend(res)
        datas.clear()    
    
    datas_gt_seq_length_keys = list(datas_gt_seq_length.keys())
    for i in range(len(datas_gt_seq_length_keys)):
        list1.append(datas_gt_seq_length_keys[i])
        if (len(datas)+1) % batch == 0:
            res = model.predict(datas)
            print(res)
            list2.extend(res)
            datas.clear()
        datas.append(datas_gt_seq_length[datas_gt_seq_length_keys[i]])
    
    if len(datas) > 0:
        res = model.predict(datas)
        print(res)
        list2.extend(res)
        datas.clear()       
    
    
    #for i in range(len(test_sets)):
        #list1.append(i)
        #if (len(datas)+1) % batch == 0:
            #res = model.predict(datas)
            #print(res)
            #list2.extend(res)
            #datas.clear()
        #datas.append(test_sets[i])
        
        
    #if len(datas) > 0:
        #res = model.predict(datas)
        #print(res)
        #list2.extend(res)
        #datas.clear()
    
    ser1 = pd.Series(list1)
    ser2 = pd.Series(list2)
    df = pd.concat([ser1,ser2],axis=1)
    df = df.sort_values(by=0)
    df.columns = ['id','class']
    df.to_csv('result.csv',encoding='utf8')
    
         