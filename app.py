# -*- coding: utf-8 -*-

from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

# 1단계 : 코드 수정
# 2단계 : 스킬 등록 (URI)
# 3단계 : 시나리오 등록한 스킬 호출
# 4단계 : 배포

## 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    # simple text 작성 양식
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

    # 이미지형 응답 양식
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

    ## 카카오톡 Calculator 계산기 응답
@app.route('/api/calCulator', methods=['POST'])
def calCulator():
    body = request.get_json()
    print(body)
    params_df = body['action']['params']
    print(type(params_df))

    print("-"*30)
    opt_operator = params_df['operators']
    print("operators:", opt_operator)
    print("-"*30)
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