#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:mars
@file: Ancient_poem_spider.py
@time: 2019/03/07
"""
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
#from Analyze import analyze
from dataBase.Connection import mysql_operator as sql
import time
'''
获得诗文的详细信息
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


    def openurl(self, url, Referer=None):
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
        self.opener.addheaders = [("User-agent", agent), ("Accept", "*/*"), ('Referer', Referer)]
        try:
            res = self.opener.open(url)
        except :

            raise Exception
        else:
            return res


class Spider(object):

    def __init__(self, BrowserBase):
        self.BrowserBase = BrowserBase



    def get_link(self, page=1):
        pass

    def expands(self, element, referer):
        # 展开阅读
        part = element.find('展开阅读')
        href = part.find('a')
        href = href['href']
        start_index = href.index('(')
        end_index = href.index(')')
        id = href[start_index+1: end_index]
        # https://so.gushiwen.org/shiwen2017/ajaxshangxi.aspx?id=812
        expands_url = 'https://so.gushiwen.org/shiwen2017/ajaxshangxi.aspx?id='+id+''
        result = self.BrowserBase.openurl(href, Referer=referer).read()
        # 网页的编码判断
        chardit = chardet.detect(result)
        html = result.decode(chardit['encoding'], 'ignore')
        element = BeautifulSoup(html, 'lxml')
        # content = element.find_next_sibling('div', class_='cont')
        content_string = element.find('div', class_='contyishang')
        content_p = content_string.findAll('p')
        content = ''
        for one in content_p:
            content += one.get_text()
        return content




    def get_content(self, content_url):
        result = self.BrowserBase.openurl(content_url, Referer='https://www.gushiwen.org').read()
        # 网页的编码判断
        chardit = chardet.detect(result)
        html = result.decode(chardit['encoding'], 'utf-8')
        element = BeautifulSoup(html, 'lxml')
        #content = element.find_next_sibling('div', class_='cont')
        content = element.findAll('div', class_='cont')[1]
        title = content.find('h1').string
        p_content = content.find('p', class_='source')
        dynasty_author = p_content.findAll('a')
        print(dynasty_author)
        dynasty = dynasty_author[0].string
        author = dynasty_author[1].string
        # 获得文本
        poem_body = content.find('div', class_='contson').get_text()
        print('基本信息')
        print(title, dynasty, author)
        print(poem_body)
        print("译文及注释")
        try:
            try:
                contyishang_content = element.findAll('div', class_='contyishang')
            except Exception:
                contyishang_content = []
            #print(contyishang_content)
            yiwen = ''
            shangxi = ''
            background = ''
            self_intro = ''
            sentence = ''
            for one in contyishang_content:
                try:
                    sentence = one.get_text().strip()
                    content_p = one.findAll('p')
                    content = ''
                    for one in content_p:
                        content += one.get_text().strip().replace('\\x99\\', '').replace('\n', '')
                except Exception:
                    pass

                if '译文' in sentence:
                    yiwen = content

                elif '赏析' in sentence:
                    shangxi = content
                elif '创作背景' in sentence:
                    background = sentence.strip().replace('\n', '')
                else:
                    pass

            # 获得诗人的 背景
            # sonspic
            try:
                self_intro_string = element.find('div', class_='sonspic')
                self_intro_string = self_intro_string.find('div', class_='cont')
                self_intro = self_intro_string.findAll('p')[1]
                self_intro = self_intro.get_text()
            except Exception:
                pass
        except Exception:
            pass
        insert_sql = "INSERT INTO poems (title, author, poem_body, dynasty, tac, appreciation, background, self_intro) " \
                     "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"

        insert_sql = insert_sql.format(title, author, poem_body, dynasty, yiwen, shangxi, background, self_intro)
        search_sql = 'select title from poems;'
        poems_list = sql.select(search_sql, 'title')

        if title in poems_list:
            print('诗文已入库')
            return
        sql.insert(insert_sql)
        print('插入一首诗')







if __name__ == '__main__':
    sql = sql()

    spider = Spider(BrowserBase())
    # 从数据库获得诗文的链接
    select_sql = 'select link, title from poem_demos'
    href_list = sql.select(select_sql, 'link','title')
    for link_title in href_list:
        link = link_title[0]
        title = link_title[1]
        search_sql = 'select title from poems;'
        poems_list = sql.select(search_sql, 'title')
        if title in poems_list:
            print('诗文已存在')
            continue
        time.sleep(1.3)
        #/shiwenv_c90ff9ea5a71.aspx
        link = 'https://so.gushiwen.org'+link
        try:
            spider.get_content(link)
        except Exception:
            pass
    sql.close()