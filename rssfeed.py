#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from datetime import datetime, timezone, timedelta
from time import mktime
from pyquery import PyQuery as pq
import yaml
import mysql.connector


def insert(connector,title,link,detail,updated_at):
    cursor = connector.cursor()
    sql = "insert into article (title,link,detail,updated_at) values ('" \
          + title + "','" + link + "','" + detail + "','" + updated_at + "')"
    try:
        cursor.execute(sql)
        connector.commit()
    except (mysql.connector.errors.IntegrityError):
        print("WARNING. dupulicate error")
    cursor.close()

# 定数
## RSSのURL
RSS_URL  = "http://news.yahoo.co.jp/pickup/rss.xml"
## mysqlの設定ファイル
SQL_CONF_FILE = "./mysql_conf.yml"

#RSSの取得
feed = feedparser.parse(RSS_URL)
#dbの接続
with open(SQL_CONF_FILE, "r") as file:
    sql_conf = yaml.load(file)
connector = mysql.connector.connect(**sql_conf)

#RSSをパースしてinsert
for entry in range(len(feed.entries)):
    #RSSの内容を一件づつ処理する
    title = feed.entries[entry].title
    link = feed.entries[entry].link
    news_url = pq(link)
    detail_url = pq(news_url(".newsLink").attr("href"))
    #更新日を文字列として取得
    published_string = feed.entries[entry].published

    #更新日をdatetimeとして取得
    tmp = feed.entries[entry].published_parsed
    hourdiff = 3600*9
    updated_at = datetime.fromtimestamp(mktime(tmp)+hourdiff)

    #表示
    insert(connector,title,link,detail_url(".ynDetailText").text(),str(updated_at))



