#coding=utf-8
import sys
import json

for line in open(sys.argv[1]):
	salary_json = json.loads(line)
	for k in salary_json:
		if isinstance(salary_json[k],unicode):
			salary_json[k] = salary_json[k].encode('utf-8')
		sys.stdout.write('%s=%s\t' % (k.encode('utf-8'), salary_json[k]))
	print

