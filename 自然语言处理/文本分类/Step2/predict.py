# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr
import numpy as np
from cnn_model_v2 import TCNNConfig, TextCNN
from datas.cnews_loader import read_category, read_vocab

try:
    bool(type(unicode))
except NameError:
    unicode = str

#base_dir = 'data/cnews'
#vocab_dir = os.path.join(base_dir, 'cnews.vocab.txt')

save_dir = 'checkpoints/textcnn_v2'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class CnnModel:
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words = np.load('./datas/total_token.npy')
        self.word_to_id = np.load('./datas/word_to_id.npy').tolist()
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)
        
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型
        

    def predict(self, data):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        #content = unicode(message)
        #data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]


if __name__ == '__main__':
    cnn_model = CnnModel()
    #test_demo = ['三星ST550以全新的拍摄方式超越了以往任何一款数码相机',
    #             '热火vs骑士前瞻：皇帝回乡二番战 东部次席唾手可得新浪体育讯北京时间3月30日7:00']
    test_sets = np.load('./datas/test_tokens.npy')
    import pandas as pd
    list1 = []
    list2 = []
    for i in range(len(test_sets)):
        list1.append(i)
        list2.append(cnn_model.predict(test_sets[i]))
    ser1 = pd.Series(list1)
    ser2 = pd.Series(list2)
    df = pd.concat([ser1,ser2],axis=1)
    df.columns = ['id','class']
    df.to_csv('result.csv',encoding='utf8')
    
         