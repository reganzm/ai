#-*- coding=utf8 -*-
import jieba
import re
from tokenizer import cut_hanlp
#jieba.load_userdict("dict.txt")

#jieba.add_word(row[0].strip(),tag=row[1].strip())
#jieba.suggest_freq(segment)
#fp=open("dict.txt",'r',encoding='utf8')
#for line in fp:
    #line=line.strip()
    #jieba.suggest_freq(line, tune=True)
#[jieba.suggest_freq(line.strip(), tune=True) for line in open("dict.txt",'r',encoding='utf8')]
if __name__=="__main__":
    string="台中正确应该不会被切开。"
    
    words=cut_hanlp(string)
    #words  = jieba.cut(string)
    print([i for i in words])
    
  
