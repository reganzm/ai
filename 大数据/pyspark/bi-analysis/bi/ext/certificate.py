# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

import copy
from argparse import ArgumentParser

from pinbot_clean.normalization import normalization_certificate
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F

from bi.ext.write2file import write2file, write2csv
from bi.settings import JCERTIFICATE_PATH, OUTPUT_PATH


def flat_map_certificate(row):
    results = []
    data = row.asDict()
    certificates = data.pop("certificate")
    if certificates:
        for certificate in certificates.split(","):
            result = copy.deepcopy(data)
            result["certificate"] = certificate
            results.append(result)
    else:
        results.append(row)
    return results


def statistic_certificate(df, results):
    """统计各个搜索字段的值与权重"""
    df = df.withColumn("certificate", df.certificateTitle)
    # df = df.withColumn("certificate", F.udf(normalization_certificate)(df.certificateTitle))
    df = df.filter(df.certificate.isNotNull()).select("certificate")
    df = df.rdd.flatMap(flat_map_certificate).toDF()
    results["certificate"] = df.groupby("certificate").agg(F.count("*").alias("person_num"))


def statistic_main(certificate_path, output_path=None, suggest=False):
    """
    简历和职位预处理
    :param certificate_path: 简历证书信息文件路径， json格式
    :param output_path: 数据库路径，parquet 格式
    :param suggest: 是否输出成联想词
    :return: 
    """

    # spark 环境初始化
    conf = SparkConf().set("spark.ui.port", "44040")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    # 加载简历基本信息，教育经历，工作经历
    results = dict()
    statistic_certificate(sqlContext.read.json(certificate_path), results)
    # write2file(results, output_path, suggest)
    write2csv(results, output_path, suggest)


if __name__ == "__main__":
    parser = ArgumentParser(usage=__doc__)
    parser.description = "简历和职位数据预处理"
    parser.add_argument('-c', action='store', dest='certificate_path', default=JCERTIFICATE_PATH,
                        help='简历基本信息文件路径，parquet格式')
    parser.add_argument('-s', action='store', dest='suggest', default=False, type=bool,
                        help='是否输出成联想词结果')
    parser.add_argument('-o', action='store', dest='output_path', default=OUTPUT_PATH,
                        help='预处理后的数据输出路径')

    # 运行参数
    args = vars(parser.parse_args())
    if not all(args.values()):
        parser.print_help()

    # 简历和职位预处理主函数
    statistic_main(**args)
