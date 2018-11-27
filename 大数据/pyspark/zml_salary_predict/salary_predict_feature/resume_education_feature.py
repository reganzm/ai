# -*- coding: utf-8 -*-
# 教育经历数据中的学校、学历、专业编码
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType

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

    major_df_t = spark.read.csv('/data/datasets/salary_predict/major.csv', header=True).toPandas().to_dict()
    major_df_map = dict(zip(major_df_t['name'].values(), major_df_t['id'].values()))

    school_df_t = spark.read.csv('/data/datasets/salary_predict/university.csv', header=True).select('sid',
                                                                                                     'name').toPandas().to_dict()
    school_df_map = dict(zip(school_df_t['name'].values(), school_df_t['sid'].values()))

    degree_df_t = spark.read.csv('/data/datasets/salary_predict/degree.csv', header=True).toPandas().to_dict()
    degree_df_map = dict(zip(degree_df_t['name'].values(), degree_df_t['id'].values()))


    def func_school(name):
        if school_df_map.get(name):
            return int(school_df_map.get(name))
        else:
            return int(school_df_map.get('unknown'))


    def func_major(name):
        if major_df_map.get(name):
            return int(major_df_map.get(name))
        else:
            return int(major_df_map.get('unknown'))


    def func_degree(name):
        if degree_df_map.get(name):
            return int(degree_df_map.get(name))
        else:
            return int(degree_df_map.get('unknown'))


    def register_udf(spark):
        udf = spark.udf
        udf.register('func_degree', func_degree, returnType=IntegerType())
        udf.register('func_school', func_school, returnType=IntegerType())
        udf.register('func_major', func_major, returnType=IntegerType())


    def work(spark):
        df = spark.read.json(
            '/user/bigdata/BI/resume_flatten_v1_20180813/resume_educations.json').createOrReplaceTempView('A')
        s_sql = """
            select *,func_degree(degree) as degree_code,func_school(school) as school_code, func_major(major) as major_code from A
        """
        spark.sql(s_sql).repartition(100).write.mode('overwrite').parquet(
            '/user/bigdata/BI/resume_flatten_v1_20180813/resume_educations_with_codes.parquet')


    register_udf(spark)
    work(spark)
    spark.stop()
