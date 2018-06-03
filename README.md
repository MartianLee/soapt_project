# soapt_project
숭실대학교 컴퓨터학부 2018년 1학기 전공종합설계1 프로젝트 팀 저장소입니다.

# 개요
머신러닝을 활용한 트위터 감정분석 프로젝트

# 개발환경
파이썬 : 3.5.2
IDE : 서브라임

# 라이브러리
```
pip install tweepy
pip install bs4
pip install pyyaml
pip install pymysql
pip install konlpy
```

konlpy 설치 방법은 [링크](http://konlpy.org/en/v0.4.4/)



# DB 생성
스키마
데이터베이스를 만듧니다.
```
mysql > create database tweet CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

테이블을 생성합니다.
```
CREATE TABLE posts ( 
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  tweet_id bigint(40) unsigned NOT NULL,
  text varchar(400) NOT NULL,
  created datetime,
  PRIMARY KEY (id)
) DEFAULT CHARSET=utf8mb4;
```

# config 파일 생성

config 파일을 생성하고 다음 정보를 입력합니다.

```
mysql:
    host: 호스트 이름
    user: 유저 이름
    passwd: 패스워드
    db: 디비명
twitter:
    consumer_key : ###
    consumer_secret : ###
    access_token : ###
    access_token_secret : ###
```


