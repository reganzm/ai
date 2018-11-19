# coding=utf-8
import json
import logging
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.web

from salary_model import SalaryModel


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger("demo")

salary_model = SalaryModel('./salary.model/')

city_dict = {'cd': 1, 'sh': 2, 'bj': 3}
edu_dict = {'other': 0, 'junior': 1, 'bachelor': 2, 'master': 3, 'doctor': 4}
job_type_dict = {'rd': 1, 'design': 2, 'bd': 3, 'pm': 4}
gender_dict = {'gg': 0, 'mm': 1}
school_dict = {'other': 0, '211': 1, '985': 2, 'oversea': 3}


class MainHandler(tornado.web.RequestHandler):

    def parse_arguments(self):
        query_info = {}
        try:
            query_info['city'] = self.get_argument("city", default=None)
            query_info['edu'] = self.get_argument("edu", default=None)
            query_info['job_type'] = self.get_argument("job_type", default=None)
            query_info['gender'] = self.get_argument("gender", default=None)
            query_info['school'] = self.get_argument("school", default=None)
            query_info['worklen'] = self.get_argument("worklen", default=None)
            query_info['is_data_valid'] = True
        except Exception, e:
            logger.error(e)
            query_info['is_data_valid'] = False
        return query_info

    def query_info_to_numeric(self, query_info):
        query_info['city'] = city_dict.get(query_info['city'], 0)
        query_info['edu'] = edu_dict.get(query_info['edu'], 0)
        query_info['job_type'] = job_type_dict.get(query_info['job_type'], 0)
        query_info['gender'] = gender_dict.get(query_info['gender'], 0)
        query_info['school'] = school_dict.get(query_info['school'], 0)
        query_info['worklen'] = int(query_info['worklen'])
        return query_info

    def get_house_price_salary_ratio(self, query_info, salary):
        if query_info['city'] == 1:
            ratio = 8877.0 / salary
            return ratio, ratio * 100 / 12
        elif query_info['city'] == 2:
            ratio = 29075.0 / salary
            return ratio, ratio * 100 / 12
        ratio = 38157.0 / salary
        return ratio, ratio * 100 / 12

    def get_salary_level(self, query_info, salary):
        city = query_info['city']
        if city == 1:  # chengdu
            if salary > 9000:
                level = 1
            elif salary > 5000:
                level = 2
            elif salary > 3000:
                level = 3
            else:
                level = 4
        elif city == 3:  # beijing
            if salary > 38000:
                level = 1
            elif salary > 19000:
                level = 2
            elif salary > 8000:
                level = 3
            else:
                level = 4
        else:
            if salary > 29000:
                level = 1
            elif salary > 15000:
                level = 2
            elif salary > 6000:
                level = 3
            else:
                level = 4
        return level

    def get_buy_house_power(self, house_salary_ratio):
        if house_salary_ratio > 1.0:
            return 1
        elif house_salary_ratio > 0.33:
            return 2
        elif house_salary_ratio > 0.1:
            return 3
        return 4

    def get(self):
        query_info = self.parse_arguments()
        result = {}
        if query_info['is_data_valid'] and query_info['edu']:
            query_info = self.query_info_to_numeric(query_info)
            lower_salary, upper_salary = salary_model.predict(query_info)
            result['lower_salary'] = lower_salary
            result['upper_salary'] = upper_salary
            result['house_salary_ratio'], result['buy_house_years'] \
            = self.get_house_price_salary_ratio(query_info, lower_salary)
            result['salary_level'] = self.get_salary_level(query_info, lower_salary)
            result['buy_house_power'] = self.get_buy_house_power(result['house_salary_ratio'])
        else:
            result['error'] = 'invalid input'
        result_str = json.dumps(result)
        self.set_header("Content-Type", 'application/json')
        self.write(result_str)
        self.finish()

application = tornado.web.Application([
    (r"/salary_predict", MainHandler),
])

if __name__ == "__main__":
    port = int(sys.argv[1])
    server = tornado.httpserver.HTTPServer(application)
    server.bind(port)
    server.start(0)
    tornado.ioloop.IOLoop.instance().start()
