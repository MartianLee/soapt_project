#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import os
import sys
import yaml
import pymysql
import datetime

# config 파일 불러옴
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# 디비 연결

db = pymysql.connect(host = cfg['mysql']['host'],       # 호스트
                     user = cfg['mysql']['user'],       # 유저이름
                     passwd = cfg['mysql']['passwd'],   # 비밀번호
                     db = cfg['mysql']['db'],           # 디비 이름
                     charset = 'utf8mb4')               # utf-8
cur = db.cursor()

# API 인증요청
consumer_key = cfg['twitter']['consumer_key']
consumer_secret = cfg['twitter']['consumer_secret']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# access 토큰 요청
access_token = cfg['twitter']['access_token']
access_token_secret = cfg['twitter']['access_token_secret']
auth.set_access_token(access_token, access_token_secret)

# twitter API 생성
api = tweepy.API(auth)

location = "%s,%s,%s" % ("33.65", "123.95", "200km")                   # 검색기준(대한민국 중심) 좌표, 반지름
#keyword = " -filter:retweets"                           # OR 로 검색어 묶어줌, 검색어 5개(반드시 OR 대문자로)
keyword = "-filter:retweets AND -https -실장 -오피 -하느님 -강남"
wfile = open(os.getcwd()+"/result.txt", mode='w', encoding='utf8')    # 쓰기 모드

array = []
numberOfItems = 1000

# 트위터에서 크롤링

try:
  # api 생성
  cursor = tweepy.Cursor(api.search, q=keyword, lang="ko", since='2017-01-01', until = '2018-01-01',count=100, geocode=location, include_entities=True)
  sql = 'INSERT INTO sobo (tweet_id, text, created) VALUES (%s, %s, %s)'
  for i, tweet in enumerate(cursor.items(numberOfItems)):
      # 읽으면서 출력
      # print("{}: {}, {}".format(i, tweet.text, tweet.created_at))
      db.cursor().execute(sql, (tweet.id, tweet.text, tweet.created_at))
      wfile.write(tweet.text) # 폴더 안에있는 text파일안에다가 써넣는 과정
  db.commit()          #트위터에서 긁어온 내용이 db에 다 긁어져 들어감. -> 그후 한번에 필터과정이 여기서 필요한듯


  sql2 = 'INSERT INTO sobo2 (tweet_id, text, created) SELECT tweet_id, text, created FROM sobo WHERE text not like %s'


  tmp = '%@%'

  db.cursor().execute(sql2, (tmp))

  db.commit()
  # 크롤링 결과 출력
  cur.execute("SELECT * FROM sobo2")
  for row in cur.fetchall():
    print(row[2])

finally:
  db.close()

wfile.close()
