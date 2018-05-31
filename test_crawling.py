# tweepy 패키지 import

import tweepy
import os
import sys

# API 인증요청
consumer_key = ""
consumer_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# access 토큰 요청
access_token = ""
access_token_secret = ""
auth.set_access_token(access_token, access_token_secret)

# twitter API 생성
api = tweepy.API(auth)

location = "%s,%s,%s" % ("35.95", "128.25", "1000km")   # 검색기준(대한민국 중심) 좌표, 반지름

keyword = "감성 OR 새벽 OR 일기"                           # OR 로 검색어 묶어줌, 검색어 5개(반드시 OR 대문자로)                               # api 생성

wfile = open(os.getcwd()+"/twitter2.txt", mode='w')     # 쓰기 모드


# twitter 검색 cursor 선언

cursor = tweepy.Cursor(api.search, q=keyword, since='2015-01-01',count=100, geocode=location, include_entities=True)
for i, tweet in enumerate(cursor.items()):
    print("{}: {}".format(i, tweet.text))
    wfile.write(tweet.text + '\n')
wfile.close()
