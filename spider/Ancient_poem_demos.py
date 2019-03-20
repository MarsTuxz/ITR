#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:mars
@file: Ancient_poem_demos.py
@time: 2019/03/10
"""
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd

import random
import socket
import urllib
import http.cookiejar
import os, sys
import json
from bs4 import BeautifulSoup
from common import Logger as LOG
# 网页编码的判断
import chardet
from dataBase.Connection import mysql_operator as sql
'''
获得诗文的类别以及链接
'''

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")
logger = LOG.Logger(logger_name = 'Macro_research')


ERROR = {
    '0': 'Can not open the url,checck you net',
    '1': 'Creat download dir error',
    '2': 'The image links is empty',
    '3': 'Download faild',
    '4': 'Build soup error,the html is empty',
    '5': 'Can not save the image to your disk',
}


class BrowserBase(object):

    def __init__(self):
        socket.setdefaulttimeout(20)

    def speak(self, name, content):
        print('[%s]%s' % (name, content))


    def openurl(self, url):
        """
        打开网页
        """
        #req = urllib.request.Request(url, header)
        cj = http.cookiejar.CookieJar()
        #cookie_support = urllib.HTTPCookieProcessor(cj)
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
       # r = self.opener.open(req)
        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",

        ]

        agent = random.choice(user_agents)
        self.opener.addheaders = [("User-agent", agent), ("Accept", "*/*"), ('Referer', 'https://so.gushiwen.org/gushi/sanbai.aspx')]
        try:
            res = self.opener.open(url)
        except :

            raise Exception
        else:
            return res


class Spider(object):

    def __init__(self, BrowserBase):
        self.BrowserBase = BrowserBase


    '''
    获得类别,及对应的链接
    '''
    def get_demos(self, top_link):

        result = self.BrowserBase.openurl(top_link).read()
        # 网页的编码判断
        chardit = chardet.detect(result)
        html = result.decode(chardit['encoding'], 'ignore')
        element = BeautifulSoup(html, 'lxml')
        right_content = element.findAll('div', class_='right')[1]
        cont_content = right_content.find('div', class_='cont')
        cont_content = cont_content.findAll('a')
        print("**********************")
        with open('pemos_demos_txt', 'w+') as f:
            f.write('诗文的类别')
            f.write(',')
            f.write('链接')
            f.write('\n')

            for one in cont_content:
                demos = one.get_text()
                print(demos)
                demos_url = one['href']
                print(demos_url)
                f.write(demos)
                f.write(',')
                f.write(demos_url)
                f.write('\n')
                f.flush()



    '''
    获得每一首古诗的具体链接
    '''
    def get_link(self, url, big_demo):
        # typecont
        result = self.BrowserBase.openurl(url).read()
        # 网页的编码判断
        chardit = chardet.detect(result)
        html = result.decode(chardit['encoding'], 'ignore')
        element = BeautifulSoup(html, 'lxml')
        typecont = element.findAll('div', class_='typecont')
        bookMl = element.findAll('div', class_='bookMl')
        print(bookMl)
        insert_sql = 'INSERT INTO poem_demos (demo1, demo2, title, link) VALUES ("{}", "{}", "{}", "{}");'
        search_sql = 'select title from poem_demos;'
        poems_list = sql.select(search_sql,  'title')
        for type, book in zip(typecont, bookMl):
            book_type = book.get_text()
            # print("{greet} from {language}.".format(greet="Hello world", language="Python")
            print(book_type)
            in_part = type.findAll('a')
            for one in in_part:
                poem = one.get_text()
                if poem in poems_list:
                    print('诗文已经存在')
                    continue
                print(poem)
                demos_url = one['href']
                print(demos_url)
                new_insert_sql = insert_sql.format(big_demo, book_type, poem, demos_url)
                #print(insert_sql)
                sql.insert(new_insert_sql)





    def get_content(self, content_url):
        result = self.BrowserBase.openurl(content_url).read()
        # 网页的编码判断
        chardit = chardet.detect(result)
        html = result.decode(chardit['encoding'], 'ignore')
        element = BeautifulSoup(html, 'lxml')
        #content = element.find_next_sibling('div', class_='cont')
        content = element.findAll('div', class_='cont')[1]
        print(content)
        title = content.find('h1').string
        print(title)
        p_content = content.find('p', class_='source')
        dynasty_author = p_content.findAll('a')
        print(dynasty_author)
        dynasty = dynasty_author[0].string
        author = dynasty_author[1].string
        # 获得文本
        poem = content.find('div', class_='contson').get_text()

        print(title, dynasty, author)
        print(poem)



        for one in element.findAll("div", class_="card-header"):
            pass







if __name__ == '__main__':
    sql = sql()

    spider = Spider(BrowserBase())
    with open('pemos_demos_txt', 'r') as f:
        f.readline()
        spider.get_link('https://so.gushiwen.org/gushi/tangshi.aspx', '唐诗三百')
    sql.close()