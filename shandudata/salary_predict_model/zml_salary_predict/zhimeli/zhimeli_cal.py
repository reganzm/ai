# -*- coding: utf-8 -*-
"""
@author: zhangmin
@Date: 2018-10-08
@Content: 从resume_works中的薪资数据分布计算出职么力的分布
@提交脚本：spark-submit --master yarn --deploy-mode client --num-executors 50 --executor-cores 4 --executor-memory 10G --driver-memory 4G --conf spark.executor.memoryOverhead=2G --conf spark.task.cpus=2 ./zhimeli_cal.py  --input_path hdfs://bigdata-2:8020/user/bigdata/BI/resume_flatten_v1_20180813/resume_works.json --output_path hdfs://bigdata-2:8020/user/bigdata/BI/resume_flatten_v1_20180813/resume_works_zhimeli.parquet
"""
from scipy.stats import norm
from pyspark.sql import SparkSession
from argparse import ArgumentParser
from .settings import *
from pyspark.sql.types import FloatType


def get_zhimeli(salary, mean_, std_):
    '''
    * salary:薪资，需要先经过log放缩处理
    * mean_:该薪资对应分布中的均值
    * std:该薪资对应分布中的标准差
    * 
    '''
    salary = float(salary)
    mean_ = float(mean_)
    std_ = float(std_)
    try:
        # 求出标准分布对应的概率
        res = norm.cdf((salary - mean_) / std_)
        # 概率百分化
        res = res * 100
        # 职么力 = 阻尼系数乘以计算出的理论职么力
        print('res:{}'.format(res))
        return float(res * DAMP_COEF)
    except Exception as e:
        print(e)
        return 50 * DAMP_COEF


def get_growthed_salary(end_year, now_, salary):
    try:
        end_year = int(end_year)
        now_ = int(now_)
        if now_ >= end_year:
            diff = now_ - end_year
            return salary * ((1 + SALARY_GROWTH_RATE) ** diff)
        else:
            return salary
    except Exception as e:
        print(e)
        return salary


def register_udf(spark):
    udf = spark.udf
    udf.register('get_zhimeli', get_zhimeli, returnType=FloatType())
    udf.register('get_growthed_salary', get_growthed_salary, returnType=FloatType())


def work():
    s_sql = """
    select 
       B._id,B.company_name,B.end_time,B.index,B.industry_category,B.position_title,B.resume_id,B.start_time,
       get_growthed_salary(year(B.end_time),year(current_date()),B.salary_min) as salary_min,
       get_growthed_salary(year(B.end_time),year(current_date()),B.salary_max) as salary_max,
       get_zhimeli(log(get_growthed_salary(year(B.end_time),year(current_date()),B.salary_min)),{},{}) as zhimeli_min,
       get_zhimeli(log(get_growthed_salary(year(B.end_time),year(current_date()),B.salary_max)),{},{}) as zhimeli_max
    from 
       A inner join B 
       on A.resume_id=B.resume_id 
       and A.`max(index)`=B.index 
    where 
       B.salary_max > B.salary_min 
       and B.salary_min >= {} 
       and B.salary_max<={}
       and year(B.end_time)<=year(current_date())
       and year(B.end_time)>=2000
    """.format(SALARY_MIN_MEAN, SALARY_MIN_STD, SALARY_MAX_MEAN, SALARY_MAX_STD, SALARY_MIN, SALARY_MAX)
    print(s_sql)
    df_salary = spark.sql(s_sql)
    df_salary.repartition(100).write.mode('overwrite').parquet(OUTPUT_PATH)


if __name__ == '__main__':
    #
    # 为了计算中减少方差，对所有薪资先计算log，再计算标准分布
    #
    #
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历薪资信息预估职么力计算【数据来自resume_works】"
    parser.add_argument('-i', '--input_path', action='store', dest='input_path', default=INPUT_PATH,
                        help='resume_works信息文件路径，json格式')
    parser.add_argument('-o', '--output_path', action='store', dest='output_path', default=OUTPUT_PATH,
                        help='resume_works职么力计算后的文件保存路径， parquet格式')

    parser.add_argument('-a', '--salary_min_mean', action='store', dest='salary_min_mean', default=SALARY_MIN_MEAN,
                        help='resume_works中由salary_min计算得到的薪资均值')
    parser.add_argument('-b', '--salary_min_std', action='store', dest='salary_min_std', default=SALARY_MIN_STD,
                        help='resume_works中由salary_min计算得到的薪资标准差')

    parser.add_argument('-c', '--salary_max_mean', action='store', dest='salary_max_mean', default=SALARY_MAX_MEAN,
                        help='resume_works中由salary_max计算得到的薪资均值')
    parser.add_argument('-d', '--salary_max_std', action='store', dest='salary_max_std', default=SALARY_MAX_STD,
                        help='resume_works中由salary_max计算得到的薪资标准差')

    # 运行参数
    args = parser.parse_args()
    if args.input_path is None:
        parser.print_help()

    spark = SparkSession.builder.master("yarn").appName("zhimeli_cal").config("spark.ui.port", "44040") \
        .config('spark.default.parallelism', '40') \
        .config('spark.executor.memory', '10G') \
        .config('spark.driver.memory', '4G') \
        .config('spark.executor.cores', '4') \
        .config('spark.dynamicAllocation.minExecutors', '50') \
        .config('spark.dynamicAllocation.initialExecutors', '50') \
        .config('spark.task.cpus', '2') \
        .config('spark.default.defaultMinPartitions', '1000') \
        .config('spark.executor.memoryOverhead', '4G') \
        .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel('WARN')
    # 注册自定义函数
    register_udf(spark)
    # 加载数据
    df = spark.read.json(args.input_path)
    df1 = df.groupBy('resume_id').max('index')
    df1.createOrReplaceTempView('A')
    df.createOrReplaceTempView('B')

    work()
    spark.stop()
