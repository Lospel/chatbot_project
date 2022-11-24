# -*- coding: utf-8 -*-
from flask import Flask, request
import pandas as pd 
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

## DB 연결 Local
def db_create():
    # 로컬
	# engine = create_engine("postgresql://postgres:1234@localhost:5432/chatbot", echo = False)
		
	# Heroku
    engine = create_engine("postgres://bypdipoxswrvkd:1014bfc1e87c03ffb7268bdeaa83408c615f16b80781d8094ce52043bf014ce1@ec2-52-23-131-232.compute-1.amazonaws.com:5432/dfshtv0nbclup8", echo = False)

    engine.connect()
    engine.execute("""CREATE TABLE MainNews(
    day VARCHAR(10), 
    text VARCHAR(255), 
    img VARCHAR(255), 
    url VARCHAR(255)
    )""")

    data = pd.read_csv(r'C:\Users\h\Desktop\temp221014\코딩자료(java,python 등)\ChatBot_Project\data\MainNews.csv')
    print(data)
    data.to_sql(name='MainNews', con=engine, schema = 'public', if_exists='replace', index=False)

if __name__ == "__main__":
    db_create()
    app.run()

from datetime import datetime
x = datetime.now()
y = x.date()
a = str(y)

## 주요 뉴스 Query 조회
@app.route('/api/queryMainNews', methods=['POST'])
def queryMainNews():
    
    # body = request.get_json()
    # params_df = body['action']['params']
    # select_MainNews = str(json.loads(params_df['select_MainNews'])['amount'])

    query_str = f'''
        SELECT text, img, url FROM MainNews where day == {a}
    '''

    engine = create_engine("postgres://bypdipoxswrvkd:1014bfc1e87c03ffb7268bdeaa83408c615f16b80781d8094ce52043bf014ce1@ec2-52-23-131-232.compute-1.amazonaws.com:5432/dfshtv0nbclup8", echo = False)

    with engine.connect() as conn:
        query = conn.execute(text(query_str))

    df = pd.DataFrame(query.fetchall())
    MainNewsText01 = df["text"][0]
    MainNewsImg01 = df["img"][0]
    MainNewsUrl01 = df["url"][0]
    MainNewsText02 = df["text"][1]
    MainNewsImg02 = df["img"][1]
    MainNewsUrl02 = df["url"][1]

    responseMain = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "주요 뉴스"
          },
          "items": [
            {
              "title": f"{MainNewsText01}",
              "imageUrl": f"{MainNewsImg01}",
              "link": {
                "web": f"{MainNewsUrl01}"
              }
            },
            {
              "title": f"{MainNewsText02}",
              "imageUrl": f"{MainNewsImg02}",
              "link": {
                "web": f"{MainNewsUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b35e4af8d760349365f56"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": "https://land.naver.com/news/headline.naver"
            }         
          ]
        }
      }
    ]
  }
}

    return responseMain