#encoding=utf8
import json
import sys,os,re
import numpy 
import pandas as pd
import numpy  as np
import gzip  
import itertools
from itertools import chain
from tokenizer import seg_sentences
pattern=re.compile(u'[^a-zA-Z\u4E00-\u9FA5]')
from jpype import *
from sklearn.feature_extraction.text import CountVectorizer  
from sklearn.feature_extraction.text import TfidfTransformer 
keep_pos="n,an,vn,nr,ns,nt,nz,nb,nba,nbc,nbp,nf,ng,nh,nhd,o,nz,nx,ntu,nts,nto,nth,ntch,ntcf,ntcb,ntc,nt,nsf,ns,nrj,nrf,nr2,nr1,nr,nnt,nnd,nn,nmc,nm,nl,nit,nis,nic,ni,nhm,nhd"
keep_pos_set=set(keep_pos.split(","))
stop_pos="q,b,f,p,qg,qt,qv,r,rg,Rg,rr,ry,rys,ryt,ryv,rz,rzs,rzt,rzv,s,v,vd,vshi,vyou,vf,vx,vl,vg,vf,vi,m,mq,uzhe,ule,uguo,ude1,ude2,ude3,usuo,udeng,uv,uzhe,uyy,udh,uls,uzhi,ulian,d,dl,u,c,cc,bl,ad,ag,al,a,r,q,p,z,pba,pbei,d,dl,o,e,xx,xu,y,yg,z,wkz,wky,wyz,wyy,wj,ww,wt,wd,wf,wm,ws,wp,wb,wh,wn,t,tg,vi,id,ip,url,tel"
stop_pos_set = set(stop_pos.split(','))
stop_ch='"是","由"'
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()        
        return json.JSONEncoder.default(self, obj)
def _replace_c(text):
    intab = ",?!"
    outtab = "，？！"    
    deltab = ")(+_-.>< "
    trantab=text.maketrans(intab, outtab,deltab)
    return text.translate(trantab)

def tokenize_raw(text):
    split_sen=(i.strip() for i in re.split('。|,|，|：|:|？|！|\t|\n',_replace_c(text)) if len(i.strip())>5)
    return [seg_sentences(sentence) for sentence in split_sen]  

def pro(text):
    fout=open("triple.txt", "w", encoding='utf-8')
    vectorize=CountVectorizer(input='content', encoding='utf-8', decode_error='strict', 
                              strip_accents=None, lowercase=True, 
                              preprocessor=None, tokenizer=tokenize, 
                   stop_words=None, 
                   token_pattern=r"[a-zA-Z\u4E00-\u9FA5]", 
                   ngram_range=(2,4), analyzer='word', max_df=0.7, 
                   min_df=2, max_features=None, vocabulary=None, 
                   binary=False, dtype=np.int64)
    freq=vectorize.fit(text)
    #out.write(json.dumps(freq.vocabulary_, ensure_ascii=False,cls=NumpyEncoder))
    #out.close()
    vectorizer1=CountVectorizer(max_df=0.7, 
                                min_df=50,tokenizer=None)

    #tt=['_'.join(i.split(" ")) for i in freq.vocabulary_.keys()]
    #ttt=('_'.join(i.split(" ")) for i in freq.vocabulary_.keys())
    freq1=vectorizer1.fit_transform(('_'.join(i.split(" ")) for i in freq.vocabulary_.keys()))   
    #nozero_element=(((i, j), freq1[i,j]) for i, j in zip(*freq1.nonzero()))

    #df = pd.SparseDataFrame([ pd.SparseSeries(freq1[i].toarray().ravel()) for i in np.arange(freq1.shape[0]) ])    
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
    word_freq=(freq1[:][i].sum() for i in range(freq1.shape[1]))
    #for a in word_freq:
        #print(a)
    #word_freq=freq1.toarray().sum(0)
    tfidf=transformer.fit_transform(freq1)#第一个fit_transform是计算tf-idf，第二个                
    #weight=tfidf.toarray()
    #w_=weight.sum(0)
    tfidf_sum=(tfidf[:][i].sum() for i in range(tfidf.shape[1]))
    #for a in w_:
        #print(a)    
    tfidf_dic=vectorizer1.get_feature_names()

    dic_filter={}

    def _add(wq,tf,i):
        dic_filter[tfidf_dic[i]]=[wq,tf]
    #[_add(word_freq[i],w_[i],i) for i in range(len(w_)) if word_freq[i]>3 and w_[i]>mean_tfidf_value]
    #[_add(word_freq[i],w_[i],i) for i in range(len(tfidf_dic)) ]
    #[_add(word_freq[i],w_[i],i) for i in range(len(tfidf_dic)) ]
    for i,(word_freq_one,w_one) in enumerate(zip(word_freq,tfidf_sum)):
        #print(word_freq_one)
        _add(word_freq_one, w_one, i)
    #dict_=dict(zip(tfidf_dic,w_))
    sort_dic=dict(sorted(dic_filter.items(),key=lambda val:val[1],reverse=False))#,reverse=False为降序排列,返回list
    #pickle.dump(sort_dic, fout)
    fout.write(json.dumps(sort_dic, ensure_ascii=False,cls=NumpyEncoder)+"\n")               
    fout.close()    


def gen_dic(in_path,save_path):
    fp=open(in_path,'r',encoding='utf-8')
    fout=open(save_path,'w',encoding='utf-8')

    copus=[list(json.loads(line).keys()) for line in fp]
    copus=[''.join(ph.split("_")) for phase in copus for ph in phase] 
    copus=remove_phase(copus)
    for i in copus:
        fout.write(i+" "+"nresume"+" "+str(10)+"\n")
    fout.close()
    #  fout.write()
def remove_n(text):
    intab = ""
    outtab = ""    
    deltab = "\n "
    trantab=text.maketrans(intab, outtab,deltab)
    return text.translate(trantab)
def list_2_ngram(sentence, n=4, m=2):
    if len(sentence) < n:
        n = len(sentence)
    temp=[tuple(sentence[i - k:i]) for k in range(m, n + 1) for i in range(k, len(sentence) + 1) ]
    return [item for item in temp if len(''.join(item).strip())>1 and len(pattern.findall(''.join(item).strip()))==0]
if __name__=="__main__":
    
    #'PlatformESB 组件 子系统 监控 NBI 接口'
    copus=[tokenize_raw(line.strip()) for line in open('text.txt','r',encoding='utf8') if len(line.strip())>0 and "RESUMEDOCSSTARTFLAG" not in line]
    #['TM_拓扑 拓扑_管理 TM_拓扑_管理']
    doc=[]
    if len(copus)>1: 
        for list_copus in copus:
            for t in list_copus:
                doc.extend([' '.join(['_'.join(i) for i in list_2_ngram(t, n=4, m=2)])])
    doc=list(filter(None,doc))
    fout=open("ngram2_41.txt", "w", encoding='utf-8')
    vectorizer1=CountVectorizer()
    
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
    freq1=vectorizer1.fit_transform(doc)  
    tfidf=transformer.fit_transform(freq1)
    word_freq=[freq1.getcol(i).sum() for i in range(freq1.shape[1])]
                 
    tfidf_sum=[tfidf.getcol(i).sum() for i in range(tfidf.shape[1])]     
    #tfidf_dic=vectorizer1.get_feature_names()
    tfidf_dic=vectorizer1.vocabulary_
    tfidf_dic=dict(zip(tfidf_dic.values(),tfidf_dic.keys()))
    dic_filter={}
    def _add(wq,tf,i):
        dic_filter[tfidf_dic[i]]=[wq,tf]
    for i,(word_freq_one,w_one) in enumerate(zip(word_freq,tfidf_sum)):
        _add(word_freq_one, w_one, i)
    sort_dic=dict(sorted(dic_filter.items(),key=lambda val:val[1],reverse=True))#,reverse=False为降序排列,返回list
    fout.write(json.dumps(sort_dic, ensure_ascii=False,cls=NumpyEncoder))               
    fout.close() 
shutdownJVM()
                        #output_file.close() 