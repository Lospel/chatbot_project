# -*- coding: utf-8 -*-
from flask import Flask, request
import pandas as pd 
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text 
import json

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

@app.route("/")
def index():
    return "DB Created Done !!"

## Query 조회
@app.route('/api/querySQL', methods=['POST'])
def querySQL():
    
    body = request.get_json()
    params_df = body['action']['params']
    sepal_length_num = str(json.loads(params_df['sepal_length_num'])['amount'])

    query_str = f'''
        SELECT sepal_length, species FROM iris where sepal_length >= {sepal_length_num}
    '''

    engine = create_engine("postgresql://qxqcovcxobgrzr:136d1a4ee21d7d53fefe41723c82cadb3a41edd4203ef9b4759b8ecb1daf68a7@ec2-107-23-76-12.compute-1.amazonaws.com:5432/d7477vdhmjaq31"
    , echo = False)

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

## Query 주택시세조회 - '주소1'에 해당하는 시/구/동 변수를 통해 아파트명 조회 
@app.route('/api/querySQL2', methods=['POST'])
def querySQL2():
    
    body = request.get_json()
    
    location01 = body['action']['params']['sys_location01']
    location02 = body['action']['params']['sys_location02']
    location03 = body['action']['params']['sys_location03']

    query_str = f'''
        SELECT DISTINCT "NAME" FROM apt2 where "CITY" = '{location01}' and "GU" = '{location02}' 
        and "DONG" = '{location03}'
    '''

    engine = create_engine("postgresql://qxqcovcxobgrzr:136d1a4ee21d7d53fefe41723c82cadb3a41edd4203ef9b4759b8ecb1daf68a7@ec2-107-23-76-12.compute-1.amazonaws.com:5432/d7477vdhmjaq31"
    , echo = False)

    with engine.connect() as conn:
        query = conn.execute(text(query_str))

    df = pd.DataFrame(query.fetchall())
    results = df['NAME'].tolist()
    answer_text = '/ '.join(results)  

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": location01 + "/" + location02 + "/" + location03 + 
                        "(을)를 선택하셨습니다. \n 해당 지역의 아파트는 \n [" + answer_text + 
                        "] \n 입니다. \n 소유하신 아파트명을 입력해 주세요."
                    }
                }
            ]
        }
    }
    return responseBody


## Query 주택시세조회 - '주소2'에 해당하는 아파트명 + 컨텍스트로 앞서 조회했던 시/구/동 파라미터 연동 
## => 해당 아파트 타입 조회
@app.route('/api/querySQL3', methods=['POST'])
def querySQL3():
    
    body = request.get_json()
    
    location01 = body['action']['params']['sys_location01']
    location02 = body['action']['params']['sys_location02']
    location03 = body['action']['params']['sys_location03']
    location04 = body['action']['params']['sys_location04']

    query_str = f'''
        SELECT "TYPE" FROM apt2 where "CITY" = '{location01}' and "GU" = '{location02}' 
        and "DONG" = '{location03}' and "NAME" = '{location04}'
    '''

    engine = create_engine("postgresql://qxqcovcxobgrzr:136d1a4ee21d7d53fefe41723c82cadb3a41edd4203ef9b4759b8ecb1daf68a7@ec2-107-23-76-12.compute-1.amazonaws.com:5432/d7477vdhmjaq31"
    , echo = False)

    with engine.connect() as conn:
        query = conn.execute(text(query_str))

    df = pd.DataFrame(query.fetchall())
    results = df['TYPE'].tolist()
    answer_text = '/'.join(str(s) for s in results)

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": location04 + "(을)를 선택하셨습니다. \n 해당 아파트의 타입은 \n [" 
                        + answer_text + "] \t 입니다. \n 해당하시는 아파트의 타입을 입력해주세요."
                    }
                }
            ]
        }
    }
    return responseBody

## Query 주택시세조회 - 컨텍스트로 앞선 파라미터 모두 연동하여 해당 타입의 시세 조회
@app.route('/api/querySQL4', methods=['POST'])
def querySQL4():
    
    body = request.get_json()
    
    location01 = body['action']['params']['sys_location01']
    location02 = body['action']['params']['sys_location02']
    location03 = body['action']['params']['sys_location03']
    location04 = body['action']['params']['sys_location04']
    sys_number = str(json.loads(body['action']['params']['sys_number'])['amount'])
    # params_df = body['action']['params']
    # sys_number = str(json.loads(params_df['sys_number'])['amount'])

    query_str = f'''
        SELECT "PRICE" FROM apt2 where "CITY" = '{location01}' and "GU" = '{location02}' 
        and "DONG" = '{location03}' and "NAME" = '{location04}' AND "TYPE" = {sys_number}
    '''

    engine = create_engine("postgresql://qxqcovcxobgrzr:136d1a4ee21d7d53fefe41723c82cadb3a41edd4203ef9b4759b8ecb1daf68a7@ec2-107-23-76-12.compute-1.amazonaws.com:5432/d7477vdhmjaq31"
    , echo = False)

    with engine.connect() as conn:
        query = conn.execute(text(query_str))
    df = pd.DataFrame(query.fetchall())
    results = df['PRICE'].tolist()
    answer_text = '/'.join(str(s) for s in results)

    responseBody = {
        "contents":[
                        {
                            "type":"card.text",
                            "cards":[
                                        {
                                            "description": "해당 아파트 타입의 시세 조회 결과입니다.",
                                            "buttons":[
                                                        {
                                                            "type":"text",
                                                            "label": answer_text,
                                                            "message": "-" + answer_text + "-"
                                                            
                                                        }
                                                     ]
                                         }
                             ]
                 }
          ]
    }
    return responseBody


## Query 조회5
@app.route('/api/querySQL5', methods=['POST'])
def querySQL5():
    
    body = request.get_json()
    
    price = json.loads(body['action']['params']['sys_number02'])['amount']
    
    Error_message = "코드이상"
    if price <= 600000000:
        answer_text = "위에서 입력하신 기준으로 고객님은 안심전환대출 신청이 가능합니다. \n (유의사항) 주택의 시세는 변동될 수 있으며, 최종 대출 가능 여부는 실제 대출심사를 통해 확인할 수 있습니다."
    elif price > 600000000:
        answer_text = "주택가격이 신청일 기준 6억원을 초과할 경우 안심전환대출신청이 불가합니다."
    else:
        answer_text = Error_message

    responseBody = {
        "contents":[
                        {
                            "type":"card.text",
                            "cards":[
                                        {
                                            "description": answer_text,
                                            "buttons":[
                                                        {
                                                            "type":"text",
                                                            "label": "신청안내",
                                                            "message": "신청안내"
                                                            
                                                        },
                                                        {
                                                            "type":"text",
                                                            "label": "홈버튼",
                                                            "message": "홈버튼"
                                                            
                                                        }
                                                     ]
                                         }
                             ]
                 }
          ]
    }
    return responseBody