# -*- coding: utf-8 -*- 
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
sentences = LineSentence('./all_token')
# size：词向量的维度
# window：上下文环境的窗口大小
# min_count：忽略出现次数低于min_count的词
model = Word2Vec(sentences, size=128, window=5, min_count=1, workers=10,compute_loss=True,iter=200,sg=0)

# 保存模型
model.save('./word_embedding_128')