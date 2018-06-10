#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import yaml
import pymysql
import datetime
import codecs

from konlpy.tag import Twitter
from konlpy.tag import Kkma
from konlpy.tag import Hannanum

twitter = Twitter()
kkma = Kkma()
hannanum = Hannanum()

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

tagger = Twitter()
corpus = codecs.open('corpus.txt', 'w', encoding='utf-8')

arr = []
setOfMorph = set()

cur.execute("SELECT * FROM analyzed order by tweet_id")
resultAnalyzed = cur.fetchall()
tmp = []
tweet_id = resultAnalyzed[0][1]
print(tweet_id)

for val in resultAnalyzed:
  # 트위터 라이브러리를 사용해 텍스트를 분석한다.
  #cur.execute("SELECT * FROM analyzed where tweet_id = " + str(row[0]))
  if tweet_id != val[1] :
    arr.append(tmp)
    tweet_id = val[1]
    tmp = []
  morph = "{}/{}".format(val[2], val[3])
  tmp.append(morph)
  if morph == "슬픔/Noun" or morph == "놀라움/Noun" or morph == "/Noun" or morph == "분노/Noun" or morph == "호기심/Noun"  :
    print(morph)
  setOfMorph.add(morph)

print("- 형태소 분석 완료")

import gensim
import multiprocessing

model = gensim.models.Word2Vec.load('model_test')

#res = model.most_similar(positive=["신지예/N"], topn=20)
#print(res)
#res = model.similarity("슬픔/NNG","슬프/VA")
#print(res)
print("- Word2Vec 모델 생성 완료")

from sklearn import preprocessing
import numpy as np

cur.execute("SELECT * FROM posts")

res = []
listOfMorph = list(setOfMorph)
similarity_array = []

for morph in listOfMorph:
  tmp = []
  val = 0
  val2 = 0
  try:
    val = model.similarity("슬픔/Noun",morph)
    val2 = model.similarity("분노/Noun",morph)
  except:
    val = 0
  finally:
    tmp.append(val)
    tmp.append(val2)
  similarity_array.append(tmp)

similarity_array = np.array(similarity_array)
min_max_scaler = preprocessing.MinMaxScaler()
scaled_similarity_array = min_max_scaler.fit_transform(similarity_array)
cnt = 0

print("- 스케일링 완료")

for row in scaled_similarity_array:
  print(listOfMorph[cnt], row)
  cnt+=1

for row in arr:
  sumOfFeeling = count = 0
  temp = []
  for morph in row:
    val = 0
    try:
      indexOfMorph = listOfMorph.index(morph)
      val = similarity_array[indexOfMorph]
    except:
      continue
    finally:
      sumOfFeeling += int(val)
      count+=1
  if count > 0:
    avrg = sumOfFeeling / float(count)
    print(avrg)
    temp.append(row)
    temp.append(avrg)
    temp.append(sumOfFeeling)
    temp.append(count)
    res.append(temp)
    print(temp)
  else:
    print(row[2] + " has no meaning")

sorted_res = sorted(res, key=lambda res : res[1])[::-1]

print("- 모든 문장의 점수화 완료")

for row in sorted_res[0:30]:
  print(row)


sentence = "나 오늘 학점 발표났는데 망함. 슬퍼ㅠㅠㅠ"
result = twitter.pos(sentence)

for word, tag in result:
  morph = "{}/{}".format(word, tag)
  val = 0
  try:
    val = model.similarity("슬픔/Noun",morph)
  except:
    continue
  finally:
    sumOfFeeling += val
    count+=1

if count > 0:
  avrg = sumOfFeeling / float(count)
  print(sumOfFeeling)
else:
  print(row[2] + " has no meaning")


print("- 문장의 점수화 완료")


print("- 상위 몇%인지 출력 완료")
