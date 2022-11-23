# ## DB 연결 Local / 1회성 (반복 실행시에는 덮어쓰기가 됨)
# def db_create():
#     # 로컬
# 	# engine = create_engine("postgresql://postgres:1234@localhost:5432/chatbot", echo = False)
		
# 	# Heroku  
#     engine = create_engine("postgresql://xxyuyjsrqkaqyz:a360ef8c197b6886cd5f0e55fcce218e4c1bcef8ee1e63028c622cf2ce368ca8@ec2-52-1-17-228.compute-1.amazonaws.com:5432/dclcju52337jbk", echo = False)

#     engine.connect()
#     engine.execute("""
#         CREATE TABLE IF NOT EXISTS iris(
#             sepal_length FLOAT NOT NULL,
#             sepal_width FLOAT NOT NULL,
#             pepal_length FLOAT NOT NULL,
#             pepal_width FLOAT NOT NULL,
#             species VARCHAR(100) NOT NULL
#         );"""
#     )
#     data = pd.read_csv('data/iris.csv')
#     print(data)
#     data.to_sql(name='iris', con=engine, schema = 'public', if_exists='replace', index=False)

# ## 메인 로직!! 
# def cals(opt_operator, number01, number02):
#     if opt_operator == "addition":
#         return number01 + number02
#     elif opt_operator == "subtraction": 
#         return number01 - number02
#     elif opt_operator == "multiplication":
#         return number01 * number02
#     elif opt_operator == "division":
#         return number01 / number02

# app = Flask(__name__)

# @app.route("/")
# def index():
#     # db_create()
#     return "DB Created Done !!!"

# ## 카카오톡 텍스트형 응답
# @app.route('/api/sayHello', methods=['POST'])
# def sayHello():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": "안녕 hello I'm Ryan"
#                     }
#                 }
#             ]
#         }
#     }

#     return responseBody


# ## 카카오톡 이미지형 응답
# @app.route('/api/showHello', methods=['POST'])
# def showHello():
#     body = request.get_json()
#     print(body)
#     print(body['userRequest']['utterance'])

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleImage": {
#                         "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
#                         "altText": "hello I'm Ryan"
#                     }
#                 }
#             ]
#         }
#     }

#     return responseBody

# ## 카카오톡 Calculator 계산기 응답
# @app.route('/api/calCulator', methods=['POST'])
# def calCulator():
#     body = request.get_json()
#     print(body)
#     params_df = body['action']['params']
#     print(type(params_df))

#     print('-----')
#     opt_operator = params_df['operators']
#     print('operator:', opt_operator)
#     print('-----')
#     number01 = json.loads(params_df['sys_number01'])['amount']
#     number02 = json.loads(params_df['sys_number02'])['amount']

#     print(opt_operator, type(opt_operator), number01, type(number01))

#     answer_text = str(cals(opt_operator, number01, number02))

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": answer_text
#                     }
#                 }
#             ]
#         }
#     }

#     return responseBody

# ## Query 조회
# @app.route('/api/querySQL', methods=['POST'])
# def querySQL():
    
#     body = request.get_json()
#     params_df = body['action']['params']
#     sepal_length_num = str(json.loads(params_df['sepal_length_num'])['amount'])

#     print(sepal_length_num, type(sepal_length_num))
#     query_str = f'''
#         SELECT sepal_length, species FROM iris where sepal_length >= {sepal_length_num}
#     '''

#     engine = create_engine("postgresql://shkegbfeivphah:183a9a9bcd13ff5522b75d240cca5335d21d0f905c1a181d15eddb6f24d39915@ec2-44-209-57-4.compute-1.amazonaws.com:5432/d4oja7hb5806v7", echo = False)

#     with engine.connect() as conn:
#         query = conn.execute(text(query_str))

#     df = pd.DataFrame(query.fetchall())
#     nrow_num = str(len(df.index))
#     answer_text = nrow_num

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": answer_text + "개 입니다."
#                     }
#                 }
#             ]
#         }
#     }
#     return responseBody

# git push heroku main 실행시 실행. 그냥 heroku만 쓰면 실행 안됨
# if __name__ == "__main__":
#     # db_create()
#     app.run()