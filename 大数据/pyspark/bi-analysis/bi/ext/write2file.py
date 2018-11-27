# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 26/07/2018 10:10
:File    : write2file.py
"""
import csv
from os.path import join


def write2file(results, output_path, suggest=False):
    for filename, df in results.items():
        # df = df.select(filename, df.person_num.cast("string")).sort(filename)
        if suggest:
            path = join(output_path, filename + "_suggest.txt")
            rows = df.filter(df.person_num > 10).sort(df.person_num.desc()).collect()[:5000]
        else:
            path = join(output_path, filename + ".txt")
            rows = df.sort(df[filename].desc()).collect()

        print("当前写入文件：{}".format(path))
        output = open(path, 'w')

        for row in rows:
            data = row.asDict()
            output.write("{}\t{}\n".format(data[filename], data["person_num"]))
        output.close()


def write2csv(results, output_path, suggest=False):
    for filename, df in results.items():
        # df = df.select(filename, df.person_num.cast("string")).sort(filename)
        if suggest:
            path = join(output_path, filename + "_suggest.txt")
            rows = df.filter(df.person_num > 10).sort(df.person_num.desc()).collect()[:5000]
        else:
            path = join(output_path, filename + ".txt")
            rows = df.sort(df[filename].desc()).collect()

        print("当前写入文件：{}".format(path))
        output = open(path, 'w')
        writer = csv.writer(output)

        for row in rows:
            data = row.asDict()
            # output.write("{}\t{}\n".format(data[filename], data["person_num"]))
            writer.writerow([data[filename], data["person_num"]])
        output.close()
