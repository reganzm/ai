# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 

spark-submit 
--master yarn 
--deploy-mode client 
--num-executors 6 
--executor-cores 1 
--executor-memory 10G 
--driver-memory 10G 
--jars /home/bigdata/mysql-connector-java-5.1.35.jar 
--driver-class-path /home/bigdata/mysql-connector-java-5.1.35.jar bi/statistic/statistic_main.py  
-p hdfs://bigdata-2:8020/user/bigdata/BI/resume_flatten_v1/resume_profile.parquet 
-e hdfs://bigdata-2:8020/user/bigdata/BI/resume_flatten_v1/resume_educations.parquet 
-w hdfs://bigdata-2:8020/user/bigdata/BI/resume_flatten_v1/resume_works.parquet 
-o "jdbc:mysql://222.211.90.70:3306/BI_V1?user=root&password=shuiyun@2018&autoReconnect=true&useUnicode=false&characterEncoding=gbk&useSSL=false"
"""

import datetime
from argparse import ArgumentParser

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F
from pyspark.sql.types import *

from bi.settings import EDUCATION_PATH, JOB_PATH, MYSQL_URL, PROFILE_PATH, WORK_PATH, LATEST_YEAR
from bi.statistic import *
from bi.utils import *

CURRENT_YEAR = datetime.datetime.now().year


def statistic_main(profile_path=None, education_path=None, work_path=None, job_path=None, mysql_url=None):
    """
    简历和职位预处理
    :param profile_path: 简历基本信息文件路径， parquet格式
    :param education_path: 简历教育经历文件路径， parquet格式
    :param work_path: 简历工作经历文件路径， parquet格式
    :param job_path: 职位信息文件路径， parquet格式
    :param mysql_url: 数据库路径，parquet 格式
    :return: 
    """

    # spark 环境初始化
    conf = SparkConf().set("spark.ui.port", "44040")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # 加载简历基本信息，教育经历，工作经历
    profile_df = sqlContext.read.parquet(profile_path).repartition(200)
    education_df = sqlContext.read.parquet(education_path).repartition(200)
    work_df = sqlContext.read.parquet(work_path).repartition(200)

    # job_df = sqlContext.read.parquet(job_path)

    # 专业对口职位分析
    statistic_major_position(profile_df, education_df, work_df, mysql_url)
    # 就业分析
    # work_statistic(profile_df, education_df, work_df, mysql_url)
    # 深造分析
    # postgraduate(profile_df, education_df, work_df, mysql_url)
    # 招聘职位和简历的供需关系分析
    # job_statistic(profile_df, job_df, mysql_url)


def work_statistic(profile_df, education_df, work_df, mysql_url):
    """就业分析"""
    # 最后一份教育经历， 且是最近五年毕业
    latest_education_df = education_df.filter(education_df.edu_index == 1).filter(education_df.school_area == "中国")
    latest_education_df = latest_education_df.filter(latest_education_df.edu_end_year >= CURRENT_YEAR - LATEST_YEAR)
    resume_df = profile_df.join(latest_education_df, "resume_id").join(work_df, "resume_id")
    # 过滤掉某些字段中的含有不合法值的记录
    resume_df = filter_invalid_value(resume_df)
    # 第一份工作经历
    first_work_df = resume_df.filter(resume_df.work_index == resume_df.work_len)
    first_work_df = process_work_data(first_work_df)

    # 持久化数据
    resume_df.persist()
    first_work_df.persist()
    # 最初的重构代码前的简历分析
    history_analysis(first_work_df, mysql_url)
    # 毕业后第一份工作分析
    statistic_graduate_first_work(first_work_df, mysql_url)
    # 毕业后多份工作分析
    statistic_graduate_all_work(resume_df, mysql_url)

    # 删除持久化数据
    resume_df.unpersist()
    first_work_df.unpersist()


def job_statistic(profile_df, job_df, mysql_url):
    """招聘职位分析"""
    statistic_job(profile_df, job_df, mysql_url)


def process_work_data(resume_df):
    """
    添加工作相关的字段
    """
    # 计算单次工作的时长
    resume_df = resume_df.withColumn("work_end_date",
                                     F.when(resume_df.work_end_date.isNotNull(), resume_df.work_end_date).otherwise(
                                         resume_df.update_date))
    resume_df = resume_df.withColumn("work_duration_month",
                                     F.months_between(resume_df.work_end_date, resume_df.work_start_date))
    resume_df = resume_df.withColumn("work_duration_year",
                                     F.udf(lambda x: x / 12 if x else -1, FloatType())(resume_df.work_duration_month))
    # 计算毕业到现在的工作时长
    resume_df = resume_df.withColumn("work_month", F.months_between(resume_df.work_end_date, resume_df.edu_end_date))
    resume_df = resume_df.withColumn("work_year", F.udf(get_years, IntegerType())(resume_df.work_month))
    # 计算薪资区间
    resume_df = resume_df.withColumn("salary_range", F.udf(get_salary_range)(resume_df.avg_salary))
    # 计算年龄区间
    resume_df = resume_df.withColumn("age_range", F.udf(get_age_range)(resume_df.age))
    # 计算工作年限区间
    resume_df = resume_df.withColumn("work_year_range", F.udf(get_work_year_range)(resume_df.work_year))
    return resume_df


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历和职位数据预处理"
    parser.add_argument('-p', action='store', dest='profile_path', default=PROFILE_PATH,
                        help='简历基本信息文件路径，parquet格式')
    parser.add_argument('-e', action='store', dest='education_path', default=EDUCATION_PATH,
                        help='简历教育经历文件路径，parquet格式')
    parser.add_argument('-w', action='store', dest='work_path', default=WORK_PATH,
                        help='简历工作经历文件路径，parquet格式')
    parser.add_argument('-j', action='store', dest='job_path', default=JOB_PATH,
                        help='职位信息文件路径，parquet格式')
    parser.add_argument('-o', action='store', dest='mysql_url', default=MYSQL_URL,
                        help='预处理后的数据输出路径')

    # 运行参数
    args = vars(parser.parse_args())
    if not all(args.values()):
        parser.print_help()

    # 简历和职位预处理主函数
    statistic_main(**args)
