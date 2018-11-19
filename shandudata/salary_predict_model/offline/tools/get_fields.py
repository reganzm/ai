#coding=utf-8
import sys
import json

for line in open(sys.argv[1]):
	salary_info = json.loads(line)
	#print salary_info['lower_salary'].strip().encode('utf-8')
	#ls = salary_info['lower_salary']
	#us = salary_info['upper_salary']
	#print (ls+us) / 2
	#print salary_info['birthday'].encode('utf-8')
	print salary_info['position_title'].encode('utf-8')
