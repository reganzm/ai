#coding=utf-8
import sys
import json
from collections import Counter

def load_school_dict(filepath):
	school_dict = {}
	for line in open(filepath):
		elems = line.strip().split(',')
		if len(elems) == 2:
			elems[0] = elems[0].decode('utf-8')
			elems[1] = elems[1].decode('utf-8')
			school_dict[elems[0]] = elems[1]
	return school_dict

if __name__=="__main__":
	school_dict = load_school_dict('./dict/college.csv')
	hi_schs = []
	for line in open(sys.argv[1]):
		si = json.loads(line)
		sch = si['school']
		if sch not in school_dict and si['lower_salary'] > 15000:
			hi_schs.append(sch)
	sch_counter = dict(Counter(hi_schs))
	for k in sch_counter:
		print "%s\t%d" % (k.encode('utf-8'),sch_counter[k])
