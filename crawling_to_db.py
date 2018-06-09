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

#location = "%s,%s,%s" % ("35.95", "128.25", "1000km")                   # 검색기준(대한민국 중심) 좌표, 반지름
location = "%s,%s,%s" % ("36.62", "127.93", "250km")
keyword = " -filter:links -filter:retweets -@ -수면제 -졸피뎀 -졸피댐 -미프진 -물뽕 -요힘빈 -흥분제 -디엠 -안마 -룸싸롱 -놀이터 -포카 -팝니다 -사다리 -직거래 -토토 -오피 -대출 -하드코어 -접대 -간증 -텔레 -워커 -카톡 -오프 -op -바둑이 -카카오톡 -tel -"                        # OR 로 검색어 묶어줌, 검색어 5개(반드시 OR 대문자로)
#keyword = " -filter:retweets"
wfile = open(os.getcwd()+"/twitter2.txt", mode='w', encoding='utf8')    # 쓰기 모드

array = []
numberOfItems = 1000
loop_count = 0

# 트위터에서 크롤링
try:
  cursor = tweepy.Cursor(api.search, q=keyword, lang="ko", since='2017-01-01', geocode=location, include_entities=True)
  sql = 'INSERT INTO posts (tweet_id, text, created) VALUES (%s, %s, %s)'

  for i, tweet in enumerate(cursor.items(loop_count)):
    if loop_count >= numberOfItems:
      break;
    # 읽으면서 출력
    #print("{}: {}, {}".format(i, tweet.text, tweet.created_at))
    if 'https' in tweet.text or '@' in tweet.text:
      continue
    db.cursor().execute(sql, (tweet.id, tweet.text, tweet.created_at))
    wfile.write(tweet.text)
    wfile.write('\n')
    wfile.write('-------------------------------------------------')
    wfile.write('\n')
    loop_count += 1
    db.commit()
finally:
  db.close()

wfile.close()
