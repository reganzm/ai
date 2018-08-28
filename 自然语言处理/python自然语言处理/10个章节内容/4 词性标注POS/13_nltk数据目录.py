import nltk
import os,os.path
create = os.path.expanduser('~/nltkdoc')
print(create)
if not os.path.exists(create):
    os.mkdir(create)
print(os.path.exists(create))
import nltk.data
print(nltk.data.path)
print(create in nltk.data.path)

