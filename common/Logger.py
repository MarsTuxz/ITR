#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:mars
@file: Logger.py
@time: 2019/03/07
"""
import logging
import platform

class Logger(object):
    def __init__(self, LOG_FILE='', logger_name=None):
        # 创建一个logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        sysStr = platform.system()
        if LOG_FILE == '':
            if sysStr == "Windows":
                LOG_FILE = 'C:\\log\\spider\\log.log'
            else:
                LOG_FILE = '/home/mars/log/log.log'

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def info(self, log):
        self.logger.info(log)

    def debug(self, log):
        self.logger.debug(log)

    def warn(self, log):
        self.logger.warn(log)

    def error(self, log):
        self.logger.error(log)