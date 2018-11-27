# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""
from pyspark.sql import SparkSession
import re
from argparse import ArgumentParser
from pinbot_clean.normalization import get_position_level1, normalization_company_name, normalization_industry, normalization_position_name
from pyspark.sql import SQLContext, functions as F
from pyspark.sql.types import FloatType,StringType
import threading
from bi.settings import JWORK_PATH
from pyspark import StorageLevel
OUTPUT_PATH = JWORK_PATH.replace("json", "parquet")
format_date = re.compile("[./]")
import os
def format_time(time_string):
    return format_date.sub("-", time_string)
    
def register_udf(spark):
    udf = spark.udf
    udf.register('normalization_company_name',normalization_company_name,returnType=StringType())
    udf.register('normalization_industry',normalization_industry,returnType=StringType())
    udf.register('normalization_position_name',normalization_position_name,returnType=StringType())
    udf.register('get_position_level1',get_position_level1,returnType=StringType())  
    udf.register('format_time',format_time,returnType=StringType())
    
def preprocess_works(df, output_path,spark):
    """
    简历工作经历信息预处理
    :param df: 工作经历数据，DataFrame数据类型
    :param output_path: 输出文件路径
    :return: 
    """
    register_udf(spark)
    # 预处理后输出字段
    output_columns = ["resume_id","company_name", "industry", "position_name", "position_title", "position_category","work_start_date", "work_end_date", "work_start_year", "work_end_year","work_index", "salary_min", "salary_max"]
    df = df.select('resume_id','company_name','industry_category','position_title','start_time','end_time','index','salary_min','salary_max')
    # 归一化处理公司名称，公司行业，职位名称
    schema = ['resume_id','company_name','industry_category','position_title','start_time','end_time','index','salary_min','salary_max']
    table_name = 'A'
    df.createOrReplaceTempView(table_name)
    df = spark.sql("""
    select 
           resume_id,
           lower(trim(normalization_company_name(company_name))) as company_name,
           lower(trim(normalization_industry(industry_category))) as industry,
           lower(trim(normalization_position_name(position_title))) as position_name,
           position_title,
           lower(trim(get_position_level1(normalization_position_name(position_title)))) as position_category,
           date_format(format_time(start_time),'yyyy-MM') as work_start_date,
           date_format(format_time(end_time),'yyyy-MM') as work_end_date,
           year(start_time) as work_start_year,
           year(end_time) as work_end_year,
           index as work_index,
           salary_min,
           salary_max
     from {} 
    """.format(table_name))
     # 过滤公司、行业、职位全为空的字段
    df = df.dropna(how="all", subset=["company_name", "industry", "position_category"])
    df.select(output_columns).write.mode('append').save(output_path)        
    spark.catalog.dropTempView(table_name)
    print('--------Task Finished !!! ------------')
    spark.stop()

if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历基本信息预处理"
    parser.add_argument('-i', '--input_path', action='store', dest='input_path', default=JWORK_PATH,
                        help='简历基本信息文件路径，json格式')
    parser.add_argument('-o', '--output_path', action='store', dest='output_path', default=OUTPUT_PATH,
                        help='简历基本信息处理后的文件保存路径， parquet格式')
    # 运行参数
    args = parser.parse_args()
    if args.input_path is None:
        parser.print_help()
        
    spark  = SparkSession.builder.master("yarn").appName("resume_works").config("spark.ui.port", "44040")\
        .config('spark.default.parallelism','40')\
        .config('spark.executor.memory','10G')\
        .config('spark.driver.memory','4G')\
        .config('spark.executor.cores','4')\
        .config('spark.dynamicAllocation.minExecutors','50')\
        .config('spark.dynamicAllocation.initialExecutors','50')\
        .config('spark.task.cpus','2')\
        .config('spark.default.defaultMinPartitions','1000')\
        .config('spark.executor.memoryOverhead','4G')\
        .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel('WARN')        
    # 加载数据
    profile_df = spark.read.json(args.input_path)
    preprocess_works(profile_df, args.output_path,spark)

