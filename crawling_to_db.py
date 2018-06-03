# -*- coding: utf-8 -*-
#!/usr/bin/python

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

#location = "%s,%s,%s" % ("35.95", "128.25", "1000km")                   # 검색기준(대한민국 중심) 좌표, 반지름
location = "%s,%s,%s" % ("36.62", "127.93", "250km")
#keyword = "감성 OR 새벽 OR 일기-filter:retweets"                        # OR 로 검색어 묶어줌, 검색어 5개(반드시 OR 대문자로)
keyword = " -filter:retweets"
wfile = open(os.getcwd()+"/twitter2.txt", mode='w', encoding='utf8')    # 쓰기 모드

array = []
numberOfItems = 100

# 트위터에서 크롤링

try:
  # api 생성
  cursor = tweepy.Cursor(api.search, q=keyword, lang="ko", since='2017-01-01', count=100, geocode=location, include_entities=True)
  sql = 'INSERT INTO posts (tweet_id, text, created) VALUES (%s, %s, %s)'

  for i, tweet in enumerate(cursor.items(numberOfItems)):
      # 읽으면서 출력
      # print("{}: {}, {}".format(i, tweet.text, tweet.created_at))
      db.cursor().execute(sql, (tweet.id, tweet.text, tweet.created_at))
      wfile.write(tweet.text)
  db.commit()

  # 크롤링 결과 출력
  cur.execute("SELECT * FROM posts")
  for row in cur.fetchall():
    print(row[2])

finally:
  db.close()

wfile.close()
