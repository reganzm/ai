# coding:utf-8
'''
Created on 2014年12月16日

@author: likaiguo
'''

from jieba import add_word, require_initialized


@require_initialized
def load_userdict(f):
    ''' Load personalized dict to improve detect rate.
    Parameter:
        - f : A plain text file contains words and their ocurrences.
    Structure of dict file:
    word1 freq1 word_type1
    word2 freq2 word_type2
    ...
    Word type may be ignored
    '''
    if isinstance(f, (str, unicode)):
        f = open(f, 'rb')
    content = f.read().decode('utf-8')
    line_no = 0
    for line in content.split("\n"):
        line_no += 1
#         print line_no, line
        if not line.rstrip():
            continue
        tup = line.split()
#         print len(tup),tup[0],tup[1],tup[2]
        word, freq = tup[0], tup[1]
        if freq.isdigit() is False:
            continue
        if line_no == 1:
            word = word.replace(u'\ufeff', u"")  # remove bom flag if it exists

        add_word(*tup)


def add_user_words(words, freq=10, tag='job_title'):
    """
    @summary: 批量加入自定义词,词频,标注
    """

    for word in words:
        tup = word.strip(), freq, tag
        add_word(*tup)


if __name__ == '__main__':
    pass
