# tweepy 패키지 import

import tweepy
import os
import sys
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
for section in cfg:
    print(section)
print(cfg['mysql'])

# API 인증요청
consumer_key = "SGxQUNWg7MM69iwxMe9WeICQP"
consumer_secret = "I844RT34PMOenus0assWA67t0nKXwjwcNERlD8LNzCPM6rh7Yt"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# access 토큰 요청
access_token = "42856552-fr0YbHWOk6VJbeayjQJrhf3Rf6AvEChfVhtVF9HT1"
access_token_secret = "up0DNinFpWOo3GYwDig5klbB0G1F9DptDmlikWqXb24fo"
auth.set_access_token(access_token, access_token_secret)

# twitter API 생성
api = tweepy.API(auth)

location = "%s,%s,%s" % ("35.95", "128.25", "1000km")   # 검색기준(대한민국 중심) 좌표, 반지름

keyword = "감성 OR 새벽 OR 일기 -filter:retweets"           # OR 로 검색어 묶어줌, 검색어 5개(반드시 OR 대문자로)                               # api 생성

wfile = open(os.getcwd()+"/twitter2.txt", mode='w')     # 쓰기 모드

array = []

# twitter 검색 cursor 선언

cursor = tweepy.Cursor(api.search, q=keyword, since='2017-01-01',count=100, geocode=location, include_entities=True)
for i, tweet in enumerate(cursor.items(100)):
    print("{}: {}, {}".format(i, tweet.text, tweet.created_at))
    wfile.write(tweet.text)

wfile.close()
