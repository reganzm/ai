# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""

from pyspark.sql import functions as F


def group_avg(df, *cols):
    return df.groupby(*cols).agg(F.avg(df.avg_salary).alias("avg_salary"))
