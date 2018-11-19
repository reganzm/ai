#coding=utf-8
import sys
import json

if __name__=='__main__':
	salary_cnt_dict = {}
	salary_cnt_dict['2000'] = 0
	salary_cnt_dict['4000'] = 0
	salary_cnt_dict['6000'] = 0
	salary_cnt_dict['8000'] = 0
	salary_cnt_dict['10000'] = 0
	salary_cnt_dict['15000'] = 0
	salary_cnt_dict['other'] = 0
	cnt = 0
	for line in open(sys.argv[1]):
		salary_info = json.loads(line)
		cnt += 1
		if salary_info['lower_salary'] <= 2000:
			salary_cnt_dict['2000'] += 1
		elif salary_info['lower_salary'] <= 4000:
			salary_cnt_dict['4000'] += 1
		elif salary_info['lower_salary'] <= 6000:
			salary_cnt_dict['6000'] += 1
		elif salary_info['lower_salary'] <= 8000:
			salary_cnt_dict['8000'] += 1
		elif salary_info['lower_salary'] <= 10000:
			salary_cnt_dict['10000'] += 1
		elif salary_info['lower_salary'] <= 15000:
			salary_cnt_dict['15000'] += 1
		else:
			salary_cnt_dict['other'] += 1
	for k in salary_cnt_dict:
		print k, salary_cnt_dict[k] * 1.0 / cnt
