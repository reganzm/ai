import nltk
from nltk.corpus import treebank
for sent in treebank.parsed_sents('wsj_0007.mrg'):
    print(sent)