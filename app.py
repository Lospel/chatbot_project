# -*- coding: utf-8 -*-
from flask import Flask, request
import pandas as pd 
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text 
import json

## DB 연결 Local / 1회성 (반복 실행시에는 덮어쓰기가 됨)
def db_create():
    # 로컬
	# engine = create_engine("postgresql://postgres:1234@localhost:5432/chatbot", echo = False)
		
	# Heroku  
    engine = create_engine("postgresql://xxyuyjsrqkaqyz:a360ef8c197b6886cd5f0e55fcce218e4c1bcef8ee1e63028c622cf2ce368ca8@ec2-52-1-17-228.compute-1.amazonaws.com:5432/dclcju52337jbk", echo = False)

    engine.connect()
    engine.execute("""
        CREATE TABLE IF NOT EXISTS iris(
            sepal_length FLOAT NOT NULL,
            sepal_width FLOAT NOT NULL,
            pepal_length FLOAT NOT NULL,
            pepal_width FLOAT NOT NULL,
            species VARCHAR(100) NOT NULL
        );"""
    )
    data = pd.read_csv('data/iris.csv')
    print(data)
    data.to_sql(name='iris', con=engine, schema = 'public', if_exists='replace', index=False)

## 메인 로직!! 
def cals(opt_operator, number01, number02):
    if opt_operator == "addition":
        return number01 + number02
    elif opt_operator == "subtraction": 
        return number01 - number02
    elif opt_operator == "multiplication":
        return number01 * number02
    elif opt_operator == "division":
        return number01 / number02

app = Flask(__name__)

@app.route("/")
def index():
    db_create()
    return "DB Created Done !!!!!!!!!!!!!!!"

## 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕 hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


## 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody

## 카카오톡 Calculator 계산기 응답
@app.route('/api/calCulator', methods=['POST'])
def calCulator():
    body = request.get_json()
    print(body)
    params_df = body['action']['params']
    print(type(params_df))

    print('-----')
    opt_operator = params_df['operators']
    print('operator:', opt_operator)
    print('-----')
    number01 = json.loads(params_df['sys_number01'])['amount']
    number02 = json.loads(params_df['sys_number02'])['amount']

    print(opt_operator, type(opt_operator), number01, type(number01))

    answer_text = str(cals(opt_operator, number01, number02))

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer_text
                    }
                }
            ]
        }
    }

    return responseBody

## Query 조회
@app.route('/api/querySQL', methods=['POST'])
def querySQL():
    
    body = request.get_json()
    params_df = body['action']['params']
    sepal_length_num = str(json.loads(params_df['sepal_length_num'])['amount'])

    print(sepal_length_num, type(sepal_length_num))
    query_str = f'''
        SELECT sepal_length, species FROM iris where sepal_length >= {sepal_length_num}
    '''

    engine = create_engine("postgresql://shkegbfeivphah:183a9a9bcd13ff5522b75d240cca5335d21d0f905c1a181d15eddb6f24d39915@ec2-44-209-57-4.compute-1.amazonaws.com:5432/d4oja7hb5806v7", echo = False)

    with engine.connect() as conn:
        query = conn.execute(text(query_str))

    df = pd.DataFrame(query.fetchall())
    nrow_num = str(len(df.index))
    answer_text = nrow_num

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer_text + "개 입니다."
                    }
                }
            ]
        }
    }
    return responseBody

# git push heroku main 실행시 실행. 그냥 heroku만 쓰면 실행 안됨
if __name__ == "__main__":
    db_create()
    app.run()

## 부동산

# 라이브러리 불러오기
import requests
from bs4 import BeautifulSoup

# 네이버 주요 뉴스 텍스트 가져오기
def naver_sites_text(url):
  global MainNewsText01
  global MainNewsText02
  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  titles = soup.select("ul.headline_list dt a")[:3]
  places_title = []

  for one in titles:
    if one.string != None:
      places_title.append(one.string)
  for i in places_title[:1]:
    MainNewsText01 = i
  for i in places_title[1:2]:
    MainNewsText02 = i

# 네이버 주요뉴스 URL 가져오기
def naver_sites_url(url):
  global MainNewsUrl01
  global MainNewsUrl02

  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  titles = soup.select("dt.photo a")[:2]
  places_url=[]

  for i in titles:
    places_url.append("https://land.naver.com"+i.attrs["href"])
  for i in places_url[:1]:
    MainNewsUrl01 = i
  for i in places_url[1:2]:
    MainNewsUrl02 = i

# 네이버 주요뉴스 이미지 가져오기
def naver_main_img_url(url):
  global MainNewsImg01
  global MainNewsImg02  
  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  news_thumbnail = soup.select('dt.photo img')[:2]
  link_thumbnail = []
  for img in news_thumbnail:
      link_thumbnail.append(img.attrs['src'])
  for i in link_thumbnail[:1]:
    MainNewsImg01 = i
  for i in link_thumbnail[1:2]:
    MainNewsImg02 = i

# 주요 뉴스 스킬
@app.route('/api/sayMainNews', methods=['POST'])
def sayMainNews():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    url = "https://land.naver.com/news/headline.naver"
    naver_sites_text(url)
    naver_sites_url(url)
    naver_main_img_url(url)

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
              "webLinkUrl": url
            }         
          ]
        }
      }
    ]
  }
}

    return responseMain

# 핫이슈 텍스트 가져오기
def naver_hotissue_text(url):
  global HotIssueText01
  global HotIssueText02
  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  titles = soup.select("div.hot_list strong")
  places_title = []

  for one in titles:
    if one.string != None:
      places_title.append(one.string)
  for i in places_title[:1]:
    HotIssueText01 = i
  for i in places_title[1:2]:
    HotIssueText02 = i


# 핫이슈 URL 가져오기
def naver_hotissue_url(url):
  global HotIssueUrl01
  global HotIssueUrl02
  
  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  titles = soup.select("dt.photo a")
  places_url=[]

  for i in titles:
    places_url.append("https://land.naver.com"+i.attrs["href"])
  for i in places_url[:1]:
    HotIssueUrl01 = i
  for i in places_url[1:2]:
    HotIssueUrl02 = i
    
# 핫이슈 이미지 가져오기
def naver_hotissue_img_url(url):
  global HotIssueImg01
  global HotIssueImg02

  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  news_thumbnail = soup.select('dt.photo img')
  link_thumbnail = []
  for img in news_thumbnail:
      link_thumbnail.append(img.attrs['src'])
  for i in link_thumbnail[:1]:
    HotIssueImg01 = i
  for i in link_thumbnail[1:2]:
    HotIssueImg02 = i

# 핫이슈 스킬
@app.route('/api/sayHotIssue', methods=['POST'])
def sayHotIssue():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    url = "https://land.naver.com/news/hotIssue.naver"
    naver_hotissue_text(url)
    naver_hotissue_url(url)
    naver_hotissue_img_url(url)

    responseHotIssue = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "핫이슈"
          },
          "items": [
            {
              "title": f"{HotIssueText01}",
              "imageUrl": f"{HotIssueImg01}",
              "link": {
                "web": f"{HotIssueUrl01}"
              }
            },
            {
              "title": f"{HotIssueText02}",
              "imageUrl": f"{HotIssueImg02}",
              "link": {
                "web": f"{HotIssueUrl02}"
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
              "webLinkUrl": url
            }         
          ]
        }
      }
    ]
  }
}

    return responseHotIssue

## 지역별 뉴스

# 지역별 뉴스 이미지 가져오기
def naver_region_img_url(url):
  global RegionImg01
  global RegionImg02
  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  news_thumbnail = soup.select('dt.photo img')
  link_thumbnail = []
  for img in news_thumbnail:
      link_thumbnail.append(img.attrs['src'])
  for i in link_thumbnail[:1]:
    RegionImg01 = i
  for i in link_thumbnail[1:2]:
    RegionImg02 = i
  
# 지역별 뉴스 텍스트 가져오기
def naver_region_text(url):
  global RegionText01
  global RegionText02
  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  titles = soup.select("div.section_headline dt a")
  places_title = []

  for one in titles:
    if one.string != None:
      places_title.append(one.string)

  for i in places_title[:1]:
    RegionText01 = i
  for i in places_title[1:2]:
    RegionText02 = i

# 지역별 뉴스 URL 가져오기
def naver_region_url(url):
  global RegionUrl01
  global RegionUrl02

  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  titles = soup.select("dt.photo a")
  places_url=[]

  for i in titles:
    places_url.append("https://land.naver.com"+i.attrs["href"])
  for i in places_url[:1]:
    RegionUrl01 = i
  for i in places_url[1:2]:
    RegionUrl02 = i

# 서울 스킬
@app.route('/api/saySeoul', methods=['POST'])
def saySeoul():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Seoul = "https://land.naver.com/news/region.naver?city_no=1100000000&dvsn_no="
    naver_region_img_url(Seoul)
    naver_region_text(Seoul)
    naver_region_url(Seoul)

    # simple text 작성 양식
    responseSeoul = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "서울특별시 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Seoul
            }
          ]
        }
      }
    ]
  }
}

    return responseSeoul

# 경기 스킬
@app.route('/api/sayGyeonggi', methods=['POST'])
def sayGyeonggi():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Gyeonggi = "https://land.naver.com/news/region.naver?city_no=4100000000&dvsn_no="
    naver_region_img_url(Gyeonggi)
    naver_region_text(Gyeonggi)
    naver_region_url(Gyeonggi)

    responseGyeonggi = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "경기도 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Gyeonggi
            }
          ]
        }
      }
    ]
  }
}

    return responseGyeonggi

# 인천 스킬
@app.route('/api/sayIncheon', methods=['POST'])
def sayIncheon():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Incheon = "https://land.naver.com/news/region.naver?city_no=2800000000&dvsn_no="
    naver_region_img_url(Incheon)
    naver_region_text(Incheon)
    naver_region_url(Incheon)

    responseIncheon = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "인천 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"    
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Incheon
            }
          ]
        }
      }
    ]
  }
}

    return responseIncheon

# 부산 스킬
@app.route('/api/sayBusan', methods=['POST'])
def sayBusan():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Busan = "https://land.naver.com/news/region.naver?city_no=2600000000&dvsn_no="
    naver_region_img_url(Busan)
    naver_region_text(Busan)
    naver_region_url(Busan)

    responseBusan = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "부산 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Busan
            }
          ]
        }
      }
    ]
  }
}

    return responseBusan

# 대전 스킬
@app.route('/api/sayDaejeon', methods=['POST'])
def sayDaejeon():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Daejeon = "https://land.naver.com/news/region.naver?city_no=3000000000&dvsn_no="
    naver_region_img_url(Daejeon)
    naver_region_text(Daejeon)
    naver_region_url(Daejeon)

    responseDaejeon = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "대전 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Daejeon
            }
          ]
        }
      }
    ]
  }
}

    return responseDaejeon

# 대구 스킬
@app.route('/api/sayDae_gu', methods=['POST'])
def sayDae_gu():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Dae_gu = "https://land.naver.com/news/region.naver?city_no=2700000000&dvsn_no="
    naver_region_img_url(Dae_gu)
    naver_region_text(Dae_gu)
    naver_region_url(Dae_gu)

    responseDae_gu = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "대구 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Dae_gu
            }
          ]
        }
      }
    ]
  }
}

    return responseDae_gu

# 울산 스킬
@app.route('/api/sayUlsan', methods=['POST'])
def sayUlsan():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Ulsan = "https://land.naver.com/news/region.naver?city_no=3100000000&dvsn_no="
    naver_region_img_url(Ulsan)
    naver_region_text(Ulsan)
    naver_region_url(Ulsan)

    responseUlsan = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "울산 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Ulsan
            }
          ]
        }
      }
    ]
  }
}

    return responseUlsan

# 세종 스킬
@app.route('/api/saySejong', methods=['POST'])
def saySejong():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Sejong = "https://land.naver.com/news/region.naver?city_no=3600000000&dvsn_no="
    naver_region_img_url(Sejong)
    naver_region_text(Sejong)
    naver_region_url(Sejong)

    responseSejong = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "세종 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Sejong
            }
          ]
        }
      }
    ]
  }
}

    return responseSejong

# 광주 스킬
@app.route('/api/sayGwangju', methods=['POST'])
def sayGwangju():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Gwangju = "https://land.naver.com/news/region.naver?city_no=2900000000&dvsn_no="
    naver_region_img_url(Gwangju)
    naver_region_text(Gwangju)
    naver_region_url(Gwangju)

    responseGwangju = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "광주 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Gwangju
            }
          ]
        }
      }
    ]
  }
}

    return responseGwangju

# 강원도 스킬
@app.route('/api/sayGangwon', methods=['POST'])
def sayGangwon():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Gangwon = "https://land.naver.com/news/region.naver?city_no=4200000000&dvsn_no="
    naver_region_img_url(Gangwon)
    naver_region_text(Gangwon)
    naver_region_url(Gangwon)

    responseGangwon = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "강원도 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Gangwon
            }
          ]
        }
      }
    ]
  }
}

    return responseGangwon

# 충북 스킬
@app.route('/api/sayChungbuk', methods=['POST'])
def sayChungbuk():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Chungbuk = "https://land.naver.com/news/region.naver?city_no=4300000000&dvsn_no="
    naver_region_img_url(Chungbuk)
    naver_region_text(Chungbuk)
    naver_region_url(Chungbuk)

    responseChungbuk = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "충청북도 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Chungbuk
            }
          ]
        }
      }
    ]
  }
}

    return responseChungbuk

# 충남 스킬
@app.route('/api/sayChungnam', methods=['POST'])
def sayChungnam():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Chungnam = "https://land.naver.com/news/region.naver?city_no=4400000000&dvsn_no="
    naver_region_img_url(Chungnam)
    naver_region_text(Chungnam)
    naver_region_url(Chungnam)

    responseChungnam = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "충청남도 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Chungnam
            }
          ]
        }
      }
    ]
  }
}

    return responseChungnam

# 경북 스킬
@app.route('/api/sayGyeongbuk', methods=['POST'])
def sayGyeongbuk():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Gyeongbuk = "https://land.naver.com/news/region.naver?city_no=4700000000&dvsn_no="
    naver_region_img_url(Gyeongbuk)
    naver_region_text(Gyeongbuk)
    naver_region_url(Gyeongbuk)

    responseGyeongbuk = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "경상북도 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Gyeongbuk
            }
          ]
        }
      }
    ]
  }
}

    return responseGyeongbuk

# 경남 스킬
@app.route('/api/sayGyeongnam', methods=['POST'])
def sayGyeongnam():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Gyeongnam = "https://land.naver.com/news/region.naver?city_no=4800000000&dvsn_no="
    naver_region_img_url(Gyeongnam)
    naver_region_text(Gyeongnam)
    naver_region_url(Gyeongnam)

    responseGyeongnam = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "경상남도 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Gyeongnam
            }
          ]
        }
      }
    ]
  }
}

    return responseGyeongnam

# 전북 스킬
@app.route('/api/sayJeonbuk', methods=['POST'])
def sayJeonbuk():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Jeonbuk = "https://land.naver.com/news/region.naver?city_no=4500000000&dvsn_no="
    naver_region_img_url(Jeonbuk)
    naver_region_text(Jeonbuk)
    naver_region_url(Jeonbuk)

    responseJeonbuk = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "전라북도 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Jeonbuk
            }
          ]
        }
      }
    ]
  }
}

    return responseJeonbuk

# 전남 스킬
@app.route('/api/sayJeonnam', methods=['POST'])
def sayJeonnam():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Jeonnam = "https://land.naver.com/news/region.naver?city_no=4600000000&dvsn_no="
    naver_region_img_url(Jeonnam)
    naver_region_text(Jeonnam)
    naver_region_url(Jeonnam)

    responseJeonnam = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "전라남도 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Jeonnam
            }
          ]
        }
      }
    ]
  }
}

    return responseJeonnam

# 제주 스킬
@app.route('/api/sayJeju', methods=['POST'])
def sayJeju():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    Jeju = "https://land.naver.com/news/region.naver?city_no=5000000000&dvsn_no="
    naver_region_img_url(Jeju)
    naver_region_text(Jeju)
    naver_region_url(Jeju)

    responseJeju = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "제주도 뉴스"
          },
          "items": [
            {
              "title": f"{RegionText01}",
              "imageUrl": f"{RegionImg01}",
              "link": {
                "web": f"{RegionUrl01}"
              }
            },
            {
              "title": f"{RegionText02}",
              "imageUrl": f"{RegionImg02}",
              "link": {
                "web": f"{RegionUrl02}"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            },
            {
              "label": "더보기",
              "action": "webLink",
              "webLinkUrl": Jeju
            }
          ]
        }
      }
    ]
  }
}

    return responseJeju