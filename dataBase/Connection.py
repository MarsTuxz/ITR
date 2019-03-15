#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:mars
@file: Connection.py
@time: 2018/11/20
"""

import pandas as pd
import pymysql.cursors

class mysql_operator(object):
    def __init__(self, host='127.0.0.1', port=3306, user='root', password='1', db='test'):
        # # 连接MySQL数据库
        # connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1', db='stock',
        #                              charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        self.connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db,
                        charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        # 通过cursor创建游标
        self.cursor = self.connection.cursor()
        print('创建连接成功')

    def close(self):
        if self.connection != None:
            self.connection.close()
        if self.cursor != None:
            self.cursor.close()

    def insert(self, sql):
        try:
            print(sql)
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()

    def select_for_args(self, sql, *args):
        '''

        :param sql:
        :param args: 需要选出来的项
        :return: 以list的形式返回查询的数据-
        '''
        result_list=[]
        self.cursor.execute(sql)
        print('数据的行署', self.cursor.rowcount)
        rs = self.cursor.fetchall();
        for one in rs:
            for params in args:
                result_list.append((one[params]))
        return result_list


    def select(self, sql):
        '''
        搜索所有的字段
        :param sql:
        :return: 以Maxies的形式返回查询的数据-
        '''
        result_list = []
        self.cursor.execute(sql)
        print('数据的行署', self.cursor.rowcount)
        rs = self.cursor.fetchall()
        for one in rs:
            result_list.append(one)
        return result_list


    def get_pd_data(self, sql, index_col='date', columns=[]):
        '''

        :param sql:
        :param index_col: ｄａｔａｆｒａｍｅ的索引项默认是ＤＡＴＥ
        :param columns: List of column names to select from SQL table (only used when reading
        a table).
        :return:DATAFRAME
        '''
        if columns == []:
            data =  pd.read_sql(sql, self.connection, index_col=index_col)
            #self.close()
            return data
        else:
            data = pd.read_sql(sql, self.connection, index_col=index_col, columns=columns)
            #self.close()
            return data


# sql = "SELECT * from global_info where category_name = '澳洲股市'"
# result = mysql_operator().get_pd_data(sql=sql, columns=['id', 'open', 'close'])
# print(result)







