#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import pymysql
import datetime

#from konlpy.tag import Kkma
#from konlpy.utils import pprint
from konlpy.tag import Twitter
from konlpy.tag import Hannanum

#kkma = Kkma()
twitter = Twitter()
hannanum = Hannanum()

#konlpy 사용방법
#pprint(kkma.sentences(u'네, 안녕하세요. 반갑습니다.'))
#pprint(kkma.nouns(u'질문이나 건의사항은 깃헙 이슈 트래커에 남겨주세요.'))
#pprint(kkma.pos(u'오류보고는 실행환경, 에러메세지와함께 설명을 최대한상세히!^^'))
#result = twitter.pos(u'오류보고는 실행환경, 에러메세지와함께 설명을 최대한상세히!^^')

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

# 이전에 DB가 있으면 제거한다.
sqlDrop = "DROP TABLE IF EXISTS analyzed;"
cur.execute(sqlDrop)

# 분석용 DB를 생성한다.
sqlCreate = "CREATE TABLE analyzed ( id bigint(20) unsigned NOT NULL AUTO_INCREMENT, tweet_id bigint(40) unsigned NOT NULL, morph VARCHAR(300), class VARCHAR(20), PRIMARY KEY (id) )  DEFAULT CHARSET=utf8mb4;"
cur.execute(sqlCreate)

cur.execute("SELECT * FROM posts")

sqlInsert = 'INSERT INTO analyzed (tweet_id, morph, class) VALUES (%s, %s, %s)'

for row in cur.fetchall():
  # 트위터 라이브러리를 사용해 텍스트를 분석한다.
  result = twitter.pos(row[2])
  for morph in result:
    print(morph)
    db.cursor().execute(sqlInsert, (row[1], morph[0], morph[1]))

db.commit();
