# coding=utf-8
import datetime
import logging

import tornado.ioloop
import tornado.web

from salary_model import SalaryModel


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger("demo")

salary_model = SalaryModel('./salary.model/')

with open("suan_alpha.htm") as html_file:
    html_src = html_file.read()
    html_src = html_src.decode('utf-8')


class MainHandler(tornado.web.RequestHandler):

    def parse_arguments(self):
        query_info = {}
        try:
            query_info['city'] = int(self.get_argument("city", default=-1))
            query_info['edu'] = int(self.get_argument("edu", default=-1))
            query_info['school'] = int(self.get_argument("school", default=-1))
            query_info['gender'] = int(self.get_argument("gender", default=-1))
            query_info['job_type'] = int(self.get_argument("job_type", default=-1))
            query_info['worklen'] = int(self.get_argument("worklen", default=-1))
        except Exception, e:
            logger.error(e)
            query_info['edu'] = -1
        return query_info

    def get_buy_house_years(self, city, salary):
        if city == 1:
            ratio = 8877.0 * 100 / (salary * 12)
        elif city == 2:
            ratio = 29075.0 * 100 / (salary * 12)
        else:
            ratio = 38157.0 * 100 / (salary * 12)
        return int(ratio)

    def get(self):
        query_info = self.parse_arguments()
        if query_info['edu'] != -1:
            salary_scope = salary_model.predict(query_info)
            buy_house_year = self.get_buy_house_years(query_info['city'], salary_scope[0])
            result_range_str = u"月薪范围：%d元 - %d元" % (int(salary_scope[0]), int(salary_scope[1]))
            result_buy_house_years_str = u"不吃不喝在当地买一百平的房子需要<em>%s</em>年" % (buy_house_year)
            html_src_result = html_src.replace('{{range_result}}', result_range_str)
            html_src_result = html_src_result.replace('{{buy_house_year_result}}', result_buy_house_years_str)
            html_src_result = html_src_result.replace('{{display_style}}', '')
        else:
            html_src_result = html_src.replace('{{range_result}}', '')
            html_src_result = html_src_result.replace('{{buy_house_year_result}}', '')
            html_src_result = html_src_result.replace('{{display_style}}', 'display:none')
        self.write(html_src_result)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
