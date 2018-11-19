# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""


def write_mysql(mysql_url, result_tables, write_mode="append"):
    """
    将统计分析的结果数据存入到mysql数据库
    :param mysql_url: mysql数据库的连接信息
    :param result_tables: 数据库表名和表对应的数据
    :param write_mode: 存储的模式，默认是在已有数据上追加
    :return: 
    """
    print("开始向数据库写入数据！！！！！")
    for table_name, result_table in result_tables.items():
        print("向数据库写入表： {}".format(table_name))
        result_table.write.jdbc(mysql_url, table_name, mode=write_mode)
    print("数据库写入完成！！！")
