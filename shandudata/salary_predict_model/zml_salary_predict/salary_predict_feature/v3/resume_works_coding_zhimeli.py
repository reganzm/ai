# -*- coding: utf-8 -*-
# 工作地点编码及计算职么力
from .settings import *
from pyspark.sql import SparkSession
from scipy.stats import norm
from pyspark.sql.types import IntegerType, FloatType


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


def func_province(name):
    if province_df_map['id'].get(name):
        return int(province_df_map['id'].get(name))
    else:
        return int(province_df_map['id'].get('unknown'))


def func_get_center(province_name, city_name):
    # 得到是否是中心城市及权重
    if province_df_map['center'].get(province_name):
        city = province_df_map['center'].get(province_name)
        # 省会城市返回3，非省会城市返回2，没有没有对应省会城市的返回1
        if city.strip() == city_name.strip():
            return 3
        else:
            return 1
    else:
        return 1


def func_get_area(province_name):
    names = ['east', 'middle', 'west']
    for name in names:
        # 得到区域编码
        if province_df_map[name].get(province_name):
            code = int(province_df_map[name].get(province_name))
            if code > 0:
                return code
        else:
            code = int(province_df_map[name].get('unknown'))
            if code > 0:
                return code

if __name__ == '__main__':
    spark = SparkSession.builder.master("yarn") \
        .appName("resume_works_coding_and_zhimeli").config("spark.ui.port", "44040") \
        .config('spark.default.parallelism', '40') \
        .config('spark.executor.memory', '6G') \
        .config('spark.driver.memory', '6G') \
        .config('spark.executor.cores', '10') \
        .config('spark.dynamicAllocation.minExecutors', '50') \
        .config('spark.dynamicAllocation.initialExecutors', '50') \
        .config('spark.task.cpus', '2') \
        .config('spark.default.defaultMinPartitions', '1000') \
        .config('spark.executor.memoryOverhead', '4G') \
        .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel('WARN')

    def register_udf(spark):
        udf = spark.udf
        udf.register('func_province', func_province, returnType=IntegerType())
        udf.register('get_zhimeli', get_zhimeli, returnType=FloatType())
        udf.register('get_growthed_salary', get_growthed_salary, returnType=FloatType())
        udf.register('get_center', func_get_center, returnType=IntegerType())
        udf.register('get_area', func_get_area, returnType=IntegerType())


    def work(spark):
        df = spark.read.parquet('/user/hdfs/resume_first_works_filter_practice_with_location.parquet')
        df.createOrReplaceTempView('B')
        print(df.columns)
        df1 = df.groupBy('resume_id').max('index')
        df1.createOrReplaceTempView('A')

        print(df1.columns)

        s_sql_0 = """
        select 
           log(get_growthed_salary(year(B.end_time),year(current_date()),B.salary_min)) as salary_min,
           log(get_growthed_salary(year(B.end_time),year(current_date()),B.salary_max)) as salary_max
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
        """.format(SALARY_MIN, SALARY_MAX)
        print(s_sql_0)
        desc = spark.sql(s_sql_0).describe().toPandas()
        SALARY_MIN_MEAN = float(desc['salary_min'][1])
        SALARY_MIN_STD = float(desc['salary_min'][2])

        SALARY_MAX_MEAN = float(desc['salary_max'][1])
        SALARY_MAX_STD = float(desc['salary_max'][2])

        s_sql = """
        select 
           B.company_name,B.end_time,B.index,B.industry_category,B.position_title,B.resume_id,B.start_time,
           B.name,B.lat,B.long,B.province,B.city,B.region,
           func_province(B.province) as province_code,
           year(current_date())-year(B.end_time) as diff_years,
           (B.salary_min+B.salary_max)/2 as salary_old,
           (get_growthed_salary(year(B.end_time),year(current_date()),B.salary_min) + get_growthed_salary(year(B.end_time),year(current_date()),B.salary_max))/2 as salary_new,
           (get_zhimeli(log(get_growthed_salary(year(B.end_time),year(current_date()),B.salary_min)),{},{})+ 
           get_zhimeli(log(get_growthed_salary(year(B.end_time),year(current_date()),B.salary_max)),{},{}))/2 as zhimeli,
           get_center(B.province,B.city)*get_area(B.province) as location_w
        from 
           A inner join B 
           on A.resume_id=B.resume_id 
           and A.`max(index)`=B.index 
        where 
           B.salary_max > B.salary_min 
           and B.salary_min >= {} 
           and B.salary_max<={}
           and year(B.end_time)<=year(current_date())
           and year(B.end_time)>=2015
        """.format(SALARY_MIN_MEAN, SALARY_MIN_STD, SALARY_MAX_MEAN, SALARY_MAX_STD, SALARY_MIN, SALARY_MAX)
        print(s_sql)
        df_salary = spark.sql(s_sql)
        df_salary.repartition(100).write.mode('overwrite').parquet(
            'resume_works_zhimeli_locations_v3.parquet')


    province_df_t = spark.read.csv('/data/datasets/salary_predict/v3/province.csv', header=True).toPandas()
    province_df_t.index = province_df_t['name']
    province_df_map = province_df_t.to_dict()
    # province_df_map = dict(zip(province_df_t['name'].values(),province_df_t['id'].values()))
    print(province_df_map)
    register_udf(spark)

    work(spark)
    spark.stop()
