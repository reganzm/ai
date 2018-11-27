# -*- coding: utf-8 -*-
# 薪资预测第三个版本：处理学习经历信息，处理最后时间，‘至今’更改为系统时间
from settings import *
from pyspark.sql.types import StringType
from pyspark.sql import SparkSession
import time
from pyspark.sql import functions as F


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


def work(spark):
    register_udf(spark)
    df = spark.read.parquet('/user/hdfs/resume_last_educations.parquet')
    df.groupBy('resume_id').min('index').select(F.col('resume_id'),
                                                F.col('min(index)').alias('index')).createOrReplaceTempView('A')
    df.createOrReplaceTempView('B')
    df1 = spark.sql('select B.* from A inner join B on A.resume_id=B.resume_id and A.index = B.index')
    df1.createOrReplaceTempView('C')
    df2 = spark.sql('select degree,get_year_month(end_time) as end_time,index,major,resume_id,school,start_time from C')
    df2.write.mode('overwrite').parquet('resume_last_educations.parquet')


if __name__ == '__main__':
    spark = SparkSession.builder.master("yarn").appName("resume_educations_data_prepare").config("spark.ui.port",
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
