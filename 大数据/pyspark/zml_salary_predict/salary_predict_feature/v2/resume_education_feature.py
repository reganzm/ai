# -*- coding: utf-8 -*-
# 教育经历数据中的学校、学历、专业编码
from settings import *
from argparse import ArgumentParser
from settings import *
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from settings import *
from pyspark.sql.functions import *
from pyspark.sql.types import BooleanType,StringType,IntegerType

if __name__ == '__main__':
    spark  = SparkSession.builder.master("yarn").appName("resume_educations_data_prepare").config("spark.ui.port", "44040")\
            .config('spark.default.parallelism','40')\
            .config('spark.executor.memory','6G')\
            .config('spark.driver.memory','6G')\
            .config('spark.executor.cores','10')\
            .config('spark.dynamicAllocation.minExecutors','50')\
            .config('spark.dynamicAllocation.initialExecutors','50')\
            .config('spark.task.cpus','2')\
            .config('spark.default.defaultMinPartitions','1000')\
            .config('spark.executor.memoryOverhead','4G')\
            .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel('WARN')
    
    
    major_df_t = spark.read.csv('/data/datasets/salary_predict/v2/major.csv',header=True).toPandas()
    major_df_t.index=major_df_t['name']
    major_df_map = major_df_t.to_dict()
    
    
    school_df_t = spark.read.csv('/data/datasets/salary_predict/v2/university.csv',header=True).select('sid','name').toPandas()
    school_df_t.index = school_df_t['name']
    school_df_map = school_df_t.to_dict()

    
    degree_df_t = spark.read.csv('/data/datasets/salary_predict/v2/degree.csv',header=True).toPandas()
    degree_df_t.index = degree_df_t['name']
    degree_df_map = degree_df_t.to_dict()

    
    
    
    def func_school(name):
        if school_df_map['name'].get(name):
            return int(school_df_map['sid'].get(name))
        else:
            return int(school_df_map['sid'].get('unknown'))
        
    
    def func_major(name):
        if major_df_map['name'].get(name):
            return int(major_df_map['id'].get(name))
        else:
            return int(major_df_map['id'].get('unknown'))
    
    def func_major_hot(name):
        if major_df_map['name'].get(name):
            return int(major_df_map['hot'].get(name))
        else:
            return int(major_df_map['hot'].get('unknown'))
    
    def func_major_high(name):
        if major_df_map['name'].get(name):
            return int(major_df_map['high'].get(name))
        else:
            return int(major_df_map['high'].get('unknown'))        
    
    def func_degree(name):
        if degree_df_map['name'].get(name):
            return int(degree_df_map['id'].get(name))
        else:
            return int(degree_df_map['id'].get('unknown'))
        
    def func_degree_w(name):
        if degree_df_map['name'].get(name):
            return int(degree_df_map['w'].get(name))
        else:
            return int(degree_df_map['w'].get('unknown'))
    
    def register_udf(spark):
        udf = spark.udf
        udf.register('func_degree',func_degree,returnType=IntegerType())
        udf.register('func_school',func_school,returnType=IntegerType())
        udf.register('func_major',func_major,returnType=IntegerType())
        
        udf.register('func_major_high',func_major_high,returnType=IntegerType())
        udf.register('func_major_hot',func_major_hot,returnType=IntegerType())
        udf.register('func_degree_w',func_degree_w,returnType=IntegerType())
    
    def work(spark):
        df = spark.read.json('/user/bigdata/BI/resume_flatten_v1_20180813/resume_educations.json').createOrReplaceTempView('A')
        s_sql = """
            select *,func_degree(degree) as degree_code,func_degree_w(degree) as degree_w,func_school(school) as school_code, func_major(major) as major_code,func_major_high(major) as major_high,
            func_major_hot(major) as major_hot from A
        """
        spark.sql(s_sql).repartition(100).write.mode('overwrite').parquet('/user/bigdata/BI/resume_flatten_v1_20180813/resume_educations_with_codes_v2.parquet')    
    
    register_udf(spark)
    work(spark)
    spark.stop()