# -*- coding: utf-8 -*-
from flask import Flask, request
import pandas as pd 
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text 
import json

## DB 연결 Local
def db_create():
    # 로컬
	# engine = create_engine("postgresql://postgres:1234@localhost:5432/chatbot", echo = False)
		
	# Heroku
    engine = create_engine("postgresql://shkegbfeivphah:183a9a9bcd13ff5522b75d240cca5335d21d0f905c1a181d15eddb6f24d39915@ec2-44-209-57-4.compute-1.amazonaws.com:5432/d4oja7hb5806v7", echo = False)

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


if __name__ == "__main__":
    db_create()
    app.run()

## 부동산

# 주요 뉴스 스킬
@app.route('/api/sayMainNews', methods=['POST'])
def sayMainNews():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

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
              "title": "서울 해제여부, 주변지역 효과 지켜본 후 판단",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/008/2022/11/11/4816714.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=headline&bss_ymd=&prsco_id=008&arti_id=0004816714"
              }
            },
            {
              "title": "연봉 1억 직장인, 16억 집살때 내달부터 7억 대출 가능",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/020/2022/11/11/3461618.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=headline&bss_ymd=&prsco_id=020&arti_id=0003461618"
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

# 핫이슈 스킬
@app.route('/api/sayHotIssue', methods=['POST'])
def sayHotIssue():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    # simple text 작성 양식
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
              "title": "규제 풀린 지방, 11월 4만 가구 분...",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/277/2022/11/11/5175821.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=issueView&isu_no=102392&prsco_id=277&arti_id=0005175821"
              }
            },
            {
              "title": "[2022 국감] '스카이72' 수상한 지...",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/119/2022/10/19/2649398.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=issueView&isu_no=102372&prsco_id=119&arti_id=0002649398"
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

# 서울 스킬
@app.route('/api/saySeoul', methods=['POST'])
def saySeoul():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

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
              "title": "경매도 전세도 급급매도 '싸늘'…'26억' 목동 아파트도 16억으로 10억 '뚝'",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/421/2022/11/09/6446031.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=421&arti_id=0006446031"
              }
            },
            {
              "title": "준공 30년 넘은 노후 아파트 비중 영등포 1위…도봉·송파 순",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/003/2022/11/09/11526383.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=003&arti_id=0011526383"
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
              "title": "광명3구역, 공공재개발 후보지 선정…LH, 2126가구 건설",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/022/2022/11/09/3752280.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=022&arti_id=0003752280"
              }
            },
            {
              "title": "두 달 만에 3억 뚝…과천 전세도 무너졌다",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/014/2022/11/09/4925252.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=014&arti_id=0004925252"
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
              "title": "송도 84㎡ 1년새 5억 뚝 … 은마는 20억선 무너져",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/009/2022/11/03/5039861.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=009&arti_id=0005039861"
              }
            },
            {
              "title": "더 떨어지기 전 팔자… 인천 \'단타 거래\' 전국 1위",
              "imageUrl": "https://s.pstatic.net/imgnews/image/thumb100/011/2022/10/20/4112568.jpg",
              "link": {
                "web": "https://land.naver.com/news/newsRead.naver?type=region&prsco_id=011&arti_id=0004112568"
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