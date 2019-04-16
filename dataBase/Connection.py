#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:mars
@file: Connection.py
@time: 2018/11/20
"""

import pandas as pd
import pymysql.cursors
from tool import tool

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



    def select_body_like(self, words):
        '''
        查询对应的诗文的所有的内容
        :param words: 模糊查询的文字
        :return:
        '''
        # select * from poems where poem_body like '%夜%'
        sql = 'select * from poems where poem_body like "%'+words+'%"'
        result_list = []
        self.cursor.execute(sql)
        print('数据的行署', self.cursor.rowcount)
        rs = self.cursor.fetchall()
        for one in rs:
            result_list.append(one)
        return result_list

    '''
    add by 4/15 author mars
    '''
    def select_title_like_reg(self, words):
        '''
        查询对应的诗文的所有的内容
        :param words: 模糊查询的文字
        :return:
        '''
        # select * from poems where poem_body like '%夜%'
        sql = 'select * from poems where poem_body REGEXP "['+words+']"'
        result_list = []
        self.cursor.execute(sql)
        print('数据的行署', self.cursor.rowcount)
        rs = self.cursor.fetchall()
        for one in rs:
            result_list.append(one['title'])
        return result_list

    '''
        add by 4/15 author mars
        '''
    def select_title_like(self, words):
        '''
        查询对应的诗文的题目
        :param words: 模糊查询的文字
        :return:
        '''
        # select * from poems where poem_body like '%夜%'
        sql = 'select title from poems where poem_body like "%'+words+'%"'
        result_list = []
        self.cursor.execute(sql)
        print('数据的行署', self.cursor.rowcount)
        rs = self.cursor.fetchall()
        for one in rs:
            result_list.append(one['title'])
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

    '''
        add by 4/15 author mars
        '''
    def select_word_like(self, word):
        '''
        模糊查询的策略如下：
        先将接受文字的前两个字，前一半字，后一半字，后两个字分别作为四组子查询
        将所有的子查询的结果进行组合，获得出现次数的最多的诗名。
        :param word:
        :return:
        '''
        #将中文的逗号转为英文的逗号,并将逗号切下，只取前一句话
        word = word.replace("，",",")
        if word.count(','):
            word = word.split(',')[0]
        title = self.select_title_like(word)
        if title:
            if isinstance(title, (list,)):
                return title[0]
            return title
        else:
            #
            length = len(word)
            if length > 4:
                b_half = word[:length//2]
                b_two = word[:2]
                a_half = word[length//2:]
                a_two = word[-2:]
                result1 = self.select_title_like(b_half)
                result2 = self.select_title_like(b_two)
                result3 = self.select_title_like(a_half)
                result4 = self.select_title_like(a_two)
                title_list = result1+result2+result3+result4
                count_dict = tool.get_count_by_counter(title_list)
                # 获得值最大时对应的key值
                title = max(count_dict, key=count_dict.get)

            elif length >= 3:
                b_two = word[:2]
                a_two = word[-2:]
                result1 = self.select_title_like(a_two)
                result2 = self.select_title_like(b_two)
                title_list = result1 + result2
                count_dict = tool.get_count_by_counter(title_list)
                title = max(count_dict, key=count_dict.get)
            else:
                title_list = self.select_title_like_reg(word)
                count_dict = tool.get_count_by_counter(title_list)
                title = max(count_dict, key=count_dict.get)
        if isinstance(title, (list, )):
            return title[0]
        return title

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

if __name__ == '__main__':
    mysql = mysql_operator()
    title = mysql.select_word_like('春是眠是不觉晓,是')
    print(type(title))
    print(title)







