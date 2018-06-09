#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import yaml
import pymysql
import datetime
import codecs

from konlpy.tag import Twitter
from konlpy.tag import Kkma

twitter = Twitter()
kkma = Kkma()

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

cur.execute("SELECT * FROM posts")

tagger = Twitter()
corpus = codecs.open('corpus.txt', 'w', encoding='utf-8')

arr = []

for row in cur.fetchall():
  # 트위터 라이브러리를 사용해 텍스트를 분석한다.
  result = twitter.pos(row[2])
  tmp = []
  for word, tag in result:
    corpus.write("{}/{}".format(word, tag))
    tmp.append("{}/{}".format(word, tag))
  print(tmp)
  corpus.write('\n')
  arr.append(tmp)

sentences_vocab = arr
sentences_train = arr

import gensim

import multiprocessing

config = {
    'min_count': 3,  # 등장 횟수가 5 이하인 단어는 무시
    'size': 300,  # 300차원짜리 벡터스페이스에 embedding
    'sg': 1,  # 0이면 CBOW, 1이면 skip-gram을 사용한다
    'batch_words': 10000,  # 사전을 구축할때 한번에 읽을 단어 수
    'iter': 10,  # 보통 딥러닝에서 말하는 epoch과 비슷한, 반복 횟수
    'workers': multiprocessing.cpu_count(),
}
# 문장 배열을 config 설정으로 Word2Vec에 학습시킨다.
model = gensim.models.Word2Vec(sentences_vocab, **config)

#model.save('model')
res = model.most_similar(positive=["슬픔/NNG"], topn=20)
print(res)
res = model.similarity("슬픔/NNG","슬프/VA")
print(res)

