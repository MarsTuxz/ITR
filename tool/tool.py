#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:mars
@file: tool.py
@time: 2019/04/15
"""
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
from collections import Counter


def get_count_by_counter(l):
    '''
    统计列表中的各个元素出现的次数
    :param l: 列表
    :return:
    '''
    count = Counter(l)   #类型： <class 'collections.Counter'>
    count_dict = dict(count)   #类型： <type 'dict'>
    return count_dict
