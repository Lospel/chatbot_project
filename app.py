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
  titles = soup.select("ul.headline_list dt a")
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
  titles = soup.select("dt.photo a")
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
  news_thumbnail = soup.select('dt.photo img')
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
                "web": f"{RegionUrl02}",
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
                "web": f"{RegionUrl02}",
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "부산 조정지역 어디 해제될까…북·사하구 모든 요건 충족",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/658/2022/09/09/19720.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=658&arti_id=0000019720"
              }
            },
            {
              "title": "부산 아파트 매매가 10년 1개월 만에 최대폭 하락",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/014/2022/08/31/4891554.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=014&arti_id=0004891554"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "대구시, 주택 임대차 신고 과태료 부과 1년 더 유예",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/421/2022/05/04/6070807.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=421&arti_id=0006070807"
              }
            },
            {
              "title": "대전시, 대덕평촌지구 지원시설용지 4필지 추가 공급",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/421/2022/03/14/5967079.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=421&arti_id=0005967079"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "대구 아파트 낙찰가율 80%선 붕괴 초읽기…저가 매수 행렬 이어질까 [심은지의 경매 인사이트]",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/015/2022/09/19/4751214.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=015&arti_id=0004751214"
              }
            },
            {
              "title": "대구 달서구 주민들, 성서행정타운 터 매각 반대(종합)",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/001/2022/08/10/13366461.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=001&arti_id=0013366461"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "LH, 울산다운2지구 신혼희망타운 공급",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/018/2022/08/17/5294008.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=018&arti_id=0005294008"
              }
            },
            {
              "title": "울산시, '미이전 시유재산 찾기' 전개…첫해 1천196억 발굴",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/001/2022/04/15/13116935.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=001&arti_id=0013116935"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "세종시, 집값 곤두박질 치더니…'찬밥 신세 됐다' 무슨 일? [심은지의 경매 인사이트]",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/015/2022/10/30/4769071.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=015&arti_id=0004769071"
              }
            },
            {
              "title": "세종시 아파트값 우수수... 7% 이상 떨어져 ‘전국1위’",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/421/2022/09/15/6334736.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=421&arti_id=0006334736"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            }
          ]
        }
      }
    ]
  }
}

    return responseSejong

# 세종 스킬
@app.route('/api/sayGwangju', methods=['POST'])
def sayGwangju():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

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
              "title": "광주송정역 일대 토지거래 허가제 연장",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/016/2022/08/25/2032686.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=016&arti_id=0002032686"
              }
            },
            {
              "title": "광주∼대구 연계 8대 프로젝트 발전계획 확정",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/003/2021/11/18/10841342.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=003&arti_id=0010841342"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "춘천시, 동산면 원창1지구 지적재조사 마무리",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/001/2022/08/25/13397432.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=001&arti_id=0013397432"
              }
            },
            {
              "title": "포항~삼척 등 영남권 9개 철도사업 “올해 8060억원 투입”",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/014/2022/06/20/4854304.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=014&arti_id=0004854304"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "청주시 등 전국 곳곳 규제지역 해제 요구",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/417/2022/04/25/807097.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=417&arti_id=0000807097"
              }
            },
            {
              "title": "사라진 단양-심곡 1.7㎞ 복합관광시설로 개발… 6월 20일까지 사업자 공모",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/016/2021/12/30/1931007.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=016&arti_id=0001931007"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "보령시, 청년 주택자금 대출이자 지원…연간 최대 300만원",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/001/2022/01/10/12908692.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=001&arti_id=0012908692"
              }
            },
            {
              "title": "11년 만에 완공…내달 1일 국내 최장 바닷길 보령해저터널 개통",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/016/2021/11/26/1917368.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=016&arti_id=0001917368"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "포항~삼척 등 영남권 9개 철도사업 “올해 8060억원 투입”",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/014/2022/06/20/4854304.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=014&arti_id=0004854304"
              }
            },
            {
              "title": "국토부, 경주·의성·장수에 '고령자복지주택' 공급",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/003/2022/06/07/11232199.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=003&arti_id=0011232199"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "전북대·창원대, 캠퍼스 혁신파크 신규사업지 선정",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/119/2022/06/09/2610999.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=119&arti_id=0002610999"
              }
            },
            {
              "title": "[함양소식] '여행을 일상처럼' 함양 온데이 프로그램 운영",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/001/2022/05/10/13168107.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=001&arti_id=0013168107"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "전주시, 부동산 조정대상지역 해제 요청…'청약시장까지 위축'",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/001/2022/09/16/13442383.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=001&arti_id=0013442383"
              }
            },
            {
              "title": "장수군, 청년 월세 20만원 특별지원…22일부터 신청",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/421/2022/08/18/6284137.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=421&arti_id=0006284137"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "광양시 '도로건설 관리계획·농어촌도로 기본계획' 용역 착수",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/421/2022/09/15/6335513.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=421&arti_id=0006335513"
              }
            },
            {
              "title": "전남 신안에 마리나단지, 충남 예산에 청년외식창업거리 조성된다",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/020/2022/08/01/3443254.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=020&arti_id=0003443254"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
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
              "title": "제주도, 청·장년 근로자 주거 제공 중소기업에 월 30만원 지원",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/001/2021/08/24/12616535.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=001&arti_id=0012616535"
              }
            },
            {
              "title": "제주시, 오등봉·중부 도시공원 민간 특례사업 추진 '박차'",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/001/2021/06/11/12453413.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=001&arti_id=0012453413"
              }
            },
           ],
          "buttons": [
            {
              "label": "뒤로 가기",
              "action": "block",
              "blockId": "636b36be0abf120ff67a4ddc"
            }
          ]
        }
      }
    ]
  }
}

    return responseJeju