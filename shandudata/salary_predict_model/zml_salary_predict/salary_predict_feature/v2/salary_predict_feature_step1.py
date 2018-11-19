# -*- coding: utf-8 -*-
"""
@author: zhangmin
@Date: 2018-10-10
@Content:
     学校/教育/行业/学历信息： /user/bigdata/BI/resume_flatten_v1_20180813/resume_educations_with_codes.parquet
     薪资/职么力信息：/user/bigdata/BI/resume_flatten_v1_20180813/resume_works_zhimeli_locations.parquet
     学校详细信息：/data/datasets/salary_predict/university.csv
     份数据使用resume_id关联，找出训练模型需要的几个字段：学校、专业、薪资、职么力、学历、区域
@提交脚本：
"""
from argparse import ArgumentParser
from settings import *
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from settings import *
from pyspark.sql.functions import col
from pyspark.sql.types import BooleanType

def filter_degree(_985,_211,degree):
    #如果_985或者_211为1,则degree学历只能在【本科、硕士、博士】中选择
    _985 = int(_985)
    _211 = int(_211)
    if _985 or _211:
        if degree in ['本科','硕士','博士']:
            return True
        else:
            return False
    else:
        return True

def register_udf(spark):
    udf = spark.udf
    udf.register('filter_degree',filter_degree,returnType=BooleanType())   

def work(args,spark):
    #学校/专业/学历信息
    spark.read.parquet(args.input_path_0).createOrReplaceTempView('A')
    #职位地点/薪资/职么力信息
    spark.read.parquet(args.input_path_1).createOrReplaceTempView('B')
    #学校消息信息，school_code和A中的school_code做关联
    spark.read.csv(args.input_path_2,header=True).createOrReplaceTempView('C')
    
    
    s_sql = """
       select 
       A.resume_id,A.degree,A.major,A.school,
       A.degree_code,A.school_code,A.major_code,A.major_high,A.major_hot,A.degree_w,
       floor(B.lat) as lat_c,
       floor(B.long) as long_c,
       floor(C.lat) as lat_s,
       floor(C.lng) as long_s,
       C.name,C._other,C._zhuan,C._ben,C._2_first_rate,C._211,C._c9,C._top_2,C._985,
       B.province,B.province_code,B.city,B.city_w,B.area_w,
       B.salary_min_bak,B.salary_max_bak,
       B.salary_min,B.salary_max,
       B.zhimeli_min,B.zhimeli_max
       from A inner join B on A.resume_id = B.resume_id
       inner join C on A.school_code = C.sid
       where 
       salary_min >={} 
       and salary_max <={}
       and filter_degree(C._985,C._211,A.degree)
    """.format(SALARY_MIN,SALARY_MAX)
    print('sql:{}'.format(s_sql))
    spark.sql(s_sql).repartition(100).write.mode('overwrite').parquet(OUTPUT_PATH)

if __name__ == '__main__':
    parser = ArgumentParser(usage=__doc__)
    parser.description = "薪资预测算法数据处理"
    parser.add_argument('-i0', '--input_path_0', action='store', dest='input_path_0', default=INPUT_PATH_0,
                        help='学校/学历/专业信息数据路径，parquet格式')
    
    parser.add_argument('-i1', '--input_path_1', action='store', dest='input_path_1', default=INPUT_PATH_1,
                        help='薪资/职么力及工作地点信息文件保存路径，parquet格式') 
    
    parser.add_argument('-i2', '--input_path_2', action='store', dest='input_path_2', default=INPUT_PATH_2,
                        help='学校详细信息文件保存路径，csv格式')     
    
    parser.add_argument('-o', '--output_path', action='store', dest='output_path', default=OUTPUT_PATH,
                        help='数据处理完成后的保存路径， parquet格式')    
    # 运行参数
    args = parser.parse_args()
    if args.input_path_0 is None or args.input_path_1 is None:
        parser.print_help()  
    
    spark  = SparkSession.builder.master("yarn").appName("salary_predict_data_prepare").config("spark.ui.port", "44040")\
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
    register_udf(spark)
    work(args,spark)
    spark.stop()
    
    
    