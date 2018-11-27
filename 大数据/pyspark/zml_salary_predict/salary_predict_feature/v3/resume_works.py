# -*- coding: utf-8 -*-
# 薪资预测第三个版本：处理简历信息，处理最后时间，‘至今’更改为系统时间。拿到最早的工作经历 并且end_time>=2015 并且不会实习经历
# 若毕业时间
from settings import *
from pyspark.sql.types import StringType, BooleanType
from pyspark.sql import SparkSession
import time
from pyspark.sql import functions as F


def filter_shixi(name):
    if name:
        if '实习' in name:
            return False
        else:
            return True
    else:
        return False


def get_year_month(i):
    if i:
        if i == '至今':
            return time.strftime('%Y.%m', time.localtime(time.time()))
        else:
            return i
    else:
        return time.strftime('%Y.%m', time.localtime(time.time()))


def register_udf(spark):
    udf = spark.udf
    udf.register('get_year_month', get_year_month, returnType=StringType())
    udf.register('filter_shixi', filter_shixi, returnType=BooleanType())


def work(spark):
    register_udf(spark)
    df = spark.read.parquet('/data/datasets/company/resume_works_with_location.parquet')
    df.groupBy('resume_id').max('index').select(F.col('resume_id'),
                                                F.col('max(index)').alias('index')).createOrReplaceTempView('A')
    df.createOrReplaceTempView('B')
    # 最早工作经历
    df1 = spark.sql('select B.* from A inner join B on A.resume_id=B.resume_id and A.index = B.index')
    df1.createOrReplaceTempView('C')
    # ‘至今’更改为当前系统时间
    df2 = spark.sql(
        "select company_name,get_year_month(end_time) as end_time,index,industry_category,position_title,"
        "resume_id,salary_max,salary_min,start_time,`name`,lat,long,province,city,region from C where `name`<>''")
    # 过滤2015年及之后的简历
    df3 = df2.where(F.year('end_time') >= '2015')
    df3.createOrReplaceTempView('D')
    # 加载最后一份学习经历
    spark.read.parquet('/user/hdfs/resume_last_educations.parquet').createOrReplaceTempView('E')
    # 由毕业时间小于第一份工作结束时间过滤‘实习经历’
    df4 = spark.sql(
        """
        select D.* from D inner join E 
        on D.resume_id = E.resume_id 
        and (year(E.end_time) < year(D.end_time) or (year(E.end_time) = year(D.end_time) and month(E.end_time) < month(D.end_time))) 
        and D.salary_min>=2000 
        and D.salary_max<=30000 
        and filter_shixi(position_title)
        """)
    df4.write.mode('overwrite').parquet('resume_first_works_filter_practice_with_location.parquet')


if __name__ == '__main__':
    spark = SparkSession.builder.master("yarn").appName("resume_works_data_prepare").config("spark.ui.port",
                                                                                            "44040") \
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
    work(spark)
    spark.stop()
