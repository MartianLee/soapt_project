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
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

location = "%s,%s,%s" % ("36.62", "127.93", "250km")                    # 검색기준(대한민국 중심) 좌표, 반지름
keyword = " -filter:links -filter:retweets -뎀 -멘션 -팔로 -추천인 -양도 -콘서트 -역세권 -룸 -서비스 -실장 -공지 -코인 -문의 -010 -사이트 -가입 -DM -수면제 -졸피 -미프진 -물뽕 -요힘빈 -흥분제 -디엠 -안마 -놀이터 -포카 -사다리 -거래 -토토 -오피 -대출 -하드코어 -접대 -텔레 -워커 -카톡 -op -바둑이 -카카오톡 -tel"                        # OR 로 검색어 묶어줌, 검색어 5개(반드시 OR 대문자로)

wfile = open(os.getcwd()+"/twitter2.txt", mode='w', encoding='utf8')    # 쓰기 모드

array = []
numberOfItems = 100000  # 검색횟수 입력
count = 0

cursor = tweepy.Cursor(api.search, q=keyword, lang="ko", until='2018-06-25', count=numberOfItems, geocode=location, include_entities=True)

sql = 'INSERT INTO posts (tweet_id, text, created) VALUES (%s, %s, %s)'

# 트위터에서 크롤링
try:
  for i, tweet in enumerate(cursor.items(numberOfItems)):
    count += 1
    if count % 1000 == 0:
      print(count)
    if 'https' in tweet.text or 'com' in tweet.text or '@' in tweet.text or '&' in tweet.text or 'domain' in tweet.text:
      continue
    db.cursor().execute(sql, (tweet.id, tweet.text, tweet.created_at))
    wfile.write(tweet.text)
  db.commit()
finally:
  db.close()

wfile.close()