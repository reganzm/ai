#coding=utf8
import jieba
import re
print('---'*20)
fp = open('text.txt',encoding='utf8')
#print([line for line in fp.readlines()])
from grammer.rules import grammer_parse

fout = open('out.txt','w',encoding='utf8')
#for line in fp.readlines():
#    print('-----',line)
print('grammer_parse........')
[grammer_parse(line.strip(),fout) for line in fp.readlines() if len(line.strip()) >0]
print('grammer_parse_1........')
fout.close()
