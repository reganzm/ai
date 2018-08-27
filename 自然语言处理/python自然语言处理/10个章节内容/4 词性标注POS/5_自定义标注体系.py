import nltk
taggedword=nltk.tag.str2tuple('bear/NN')
print(taggedword)
print(taggedword[0])
print(taggedword[1])

taggedword=nltk.tag.str2tuple('苹果/NN')
print(taggedword)
print(taggedword[0])
print(taggedword[1])
