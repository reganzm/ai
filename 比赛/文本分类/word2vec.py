# -*- coding: utf-8 -*- 
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
sentences = LineSentence('./all_token')
# size����������ά��
# window�������Ļ����Ĵ��ڴ�С
# min_count�����Գ��ִ�������min_count�Ĵ�
model = Word2Vec(sentences, size=128, window=5, min_count=1, workers=10,compute_loss=True,iter=200,sg=0)

# ����ģ��
model.save('./word_embedding_128')