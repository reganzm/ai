# coding=utf-8
import cPickle
import logging

import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class SalaryModel(object):
    def __init__(self, path):
        lower_model_path = '%s/lower.model' % path
        upper_model_path = '%s/upper.model' % path
        if os.path.exists(lower_model_path):
            with open(lower_model_path, 'rb') as fid:
                self.lower_pred = cPickle.load(fid)
                logging.info("load lower salary model from file.")
        if os.path.exists(upper_model_path):
            with open(upper_model_path, 'rb') as fid:
                self.upper_pred = cPickle.load(fid)
                logging.info("load upper salary model from file.")

    def predict(self, input_info):
        x = list()
        x.append(input_info['edu'])
        x.append(input_info['school'])
        x.append(input_info['worklen'])
        x.append(input_info['city'])
        x.append(input_info['gender'])
        x.append(input_info['job_type'])
        y_lower = self.lower_pred.predict(x)
        y_upper = self.upper_pred.predict(x)
        return [y_lower[0], y_upper[0]]


if __name__ == '__main__':
    m_salary = SalaryModel('./salary.model/')
    input_info = {"job_type": 1, "gender": 0, 'edu': 2, 'school': 3,
                  'age': 28, 'worklen': 5, 'company_type': 2, "city": 1}
    print(m_salary.predict(input_info))
