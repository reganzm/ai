# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-24
@Content: 简历信息和职位信息预处理
"""

from argparse import ArgumentParser
from os.path import join

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

from bi.preprocess.job_profile import preprocess_job_profile
from bi.preprocess.resume_educations import preprocess_educations
from bi.preprocess.resume_profile import preprocess_resume_profile
from bi.preprocess.resume_works import preprocess_works
from bi.settings import JEDUCATION_PATH, JJOB_PATH, JPROFILE_PATH, JWORK_PATH, OUTPUT_PATH


def preprocess_main(profile_path=None, education_path=None, work_path=None, job_path=None, output_path=None):
    """
    简历和职位预处理
    :param profile_path: 简历基本信息文件路径， json格式
    :param education_path: 简历教育经历文件路径， json格式
    :param work_path: 简历工作经历文件路径， json格式
    :param job_path: 职位信息文件路径， json格式
    :param output_path: 输出文件路径，parquet 格式
    :return: 
    """

    # spark 环境初始化
    conf = SparkConf().set("spark.ui.port", "44040")
    sc = SparkContext(conf=conf)
    sql_context = SQLContext(sc)

    # 所有加载文件格式
    input_format = "json"

    # 所有预处理后的文件输出格式
    output_format = "parquet"

    # 文件名后缀替换
    op = lambda input_path: join(output_path, input_path.replace(input_format, output_format))

    # 简历基本信息预处理
    if profile_path:
        profile_df = sql_context.read.json(profile_path)
        preprocess_resume_profile(profile_df, op(profile_path))

    # 教育经历信息预处理
    if education_path:
        education_df = sql_context.read.json(education_path)
        preprocess_educations(education_df, op(education_path))

    # 工作经历信息预处理
    if work_path:
        work_df = sql_context.read.json(work_path)
        preprocess_works(work_df, op(work_path))

    # 职位信息预处理
    if job_path:
        job_df = sql_context.read.json(job_path)
        preprocess_job_profile(job_df, op(job_path))

    print(all(args.values()))


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历和职位数据预处理"
    parser.add_argument('-p', action='store', dest='profile_path', default=JPROFILE_PATH,
                        help='简历基本信息文件路径，json格式')
    parser.add_argument('-e', action='store', dest='education_path', default=JEDUCATION_PATH,
                        help='简历教育经历文件路径，json格式')
    parser.add_argument('-w', action='store', dest='work_path', default=JWORK_PATH,
                        help='简历工作经历文件路径，json格式')
    parser.add_argument('-j', action='store', dest='job_path', default=JJOB_PATH,
                        help='职位信息文件路径，json格式')
    parser.add_argument('-o', action='store', dest='output_path', default=OUTPUT_PATH,
                        help='预处理后的数据输出路径')

    # 运行参数
    args = vars(parser.parse_args())
    if not any(args.values()):
        parser.print_help()

    # 简历和职位预处理主函数
    preprocess_main(**args)
