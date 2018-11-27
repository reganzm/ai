# coding:utf-8
"""
@author: weijinlong
@Date: 2018-05-02
@Content: 
日志模块

包含三个日志生成器：
1. flogger:日志输出到文件
2. clogger:日志输出到控制台
3. fclogger:日志同时输出到文件和控制台

官方logging默认的日志级别设置为WARNING
（日志级别等级CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET）
只有日志等级大于或等于设置的日志级别的日志才会被输出
"""
import logging.handlers
import sys

DEFAULT_LOGGING_LEVEL = logging.INFO


class Logger(object):
    """
    日志封装类
    """

    def __init__(self, loggername,
                 loglevel2console=DEFAULT_LOGGING_LEVEL,
                 loglevel2file=DEFAULT_LOGGING_LEVEL,
                 error_file=False,
                 log2console=True, log2file=False, logfile=None):
        """Logger初始化方法
        根据参数初始化不同的日志生成器：文件logger、控制台logger、文件和控制台logger

        :param loggername: logger名称,传入相同的名称则获取到同一个logger实例
        :param loglevel2console: 控制台日志级别,默认为logging.DEBUG,低于DEBUG的级别
                (如：NOTSET)将会忽略
        :param loglevel2file: 文件输出日志级别,默认为logging.INFO,低于INFO的级别
                (如：DEBUG,NOTSET)将会忽略
        :param log2console: 日志是否输出到控制台,sys.stderr
        :param log2file: 日志是否输出到文件
        :param logfile: 日志文件名

        :return: logger
        """

        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)

        # set formater
        formatstr = '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d :%(funcName)s(%(threadName)s): %(message)s'
        formatter = logging.Formatter(formatstr, "%Y-%m-%d %H:%M:%S")

        if log2console:
            # 创建一个handler，用于输出到控制台
            ch = logging.StreamHandler(sys.stderr)
            ch.setLevel(loglevel2console)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        if log2file:
            # 创建一个handler，用于写入日志文件
            # fh = logging.FileHandler(logfile)
            # 创建一个1天换一次log文件的handler,最多15个,滚动删除
            fh = logging.handlers.TimedRotatingFileHandler(logfile, 'D', 5, 15)
            fh.setLevel(loglevel2file)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        if error_file:
            # 创建日志 将错误信息单独输出到一个错误日志文件
            error = logging.handlers.TimedRotatingFileHandler(logfile + '.error', 'D', 5, 15)
            error.setLevel(logging.ERROR)
            error.setFormatter(formatter)
            self.logger.addHandler(error)

    def get_logger(self):
        return self.logger
