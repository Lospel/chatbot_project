import cx_Oracle
from datetime import datetime
x = datetime.now()
y = x.date()
a = str(y)
path_folder = "C:/Users/h/Pictures/"+ a

dsn = cx_Oracle.makedsn("localhost",1521,"orcl")
db = cx_Oracle.connect('ora_user','human123', dsn, encoding='utf8')
cursor = db.cursor()

# SQL 테이블 생성
def CreateTable() :
    sql = "CREATE TABLE MainNews (day VARCHAR(10), text VARCHAR(255), img VARCHAR(255), url VARCHAR(255))"
    cursor.execute(sql)
    sql2 = "CREATE TABLE HotIssue (day VARCHAR(10), text VARCHAR(255), img VARCHAR(255), url VARCHAR(255))"
    cursor.execute(sql2)
    sql3 = "CREATE TABLE RegionNews (regions VARCHAR(10), day VARCHAR(10), text VARCHAR(255), img VARCHAR(255), url VARCHAR(255))"
    cursor.execute(sql3)

# 주요 뉴스
def MainNews():
    Main_text = open(path_folder+"/주요뉴스_텍스트.txt","r")
    Main_img = open(path_folder+"/주요뉴스_이미지.txt","r")
    Main_url = open(path_folder+"/주요뉴스_URL.txt","r")
    Maindata_text = Main_text.readlines()
    Maindata_img = Main_img.readlines()
    Maindata_url = Main_url.readlines()

    for i in Maindata_text :
        MainNews_Text = i.split('@@')
    for i in Maindata_img :
        MainNews_Img = i.split('@@')
    for i in Maindata_url :
        MainNews_Url = i.split('@@')

    num = 0
    a = str(y)

    while num < 2 :
        sql = "INSERT INTO MainNews(day,text,img,url) VALUES(:1,:2,:3,:4)"
        val = (f"{a}", f"{MainNews_Text[num]}", f"{MainNews_Img[num]}",f"{MainNews_Url[num]}")
        cursor.execute(sql,val)
        db.commit()
        num += 1

    sql_rowid = "delete from MainNews a where rowid > ANY (select rowid from MainNews b where a.text = b.text)"
    cursor.execute(sql_rowid)
    db.commit()

    # cursor.close()
    # db.close()

    Main_text.close()
    Main_img.close()
    Main_url.close()

# 핫이슈
def HotIssue():
    HotIssue_text = open(path_folder+"\핫이슈_텍스트.txt","r")
    HotIssue_img = open(path_folder+"\핫이슈_이미지.txt","r")
    HotIssue_url = open(path_folder+"\핫이슈_URL.txt","r")
    Hotdata_text = HotIssue_text.readlines()
    Hotdata_img = HotIssue_img.readlines()
    Hotdata_url = HotIssue_url.readlines()

    for i in Hotdata_text :
        Hot_Text = i.split('@@')
    for i in Hotdata_img :
        Hot_Img = i.split('@@')
    for i in Hotdata_url :
        Hot_Url = i.split('@@')

    num = 0
    a = str(y)

    while num < 2 :
        sql = "INSERT INTO HotIssue (day,text,img,url) VALUES(:1,:2,:3,:4)"
        val = (f"{a}", f"{Hot_Text[num]}", f"{Hot_Img[num]}",f"{Hot_Url[num]}")
        cursor.execute(sql,val)
        db.commit()
        num += 1

    sql_rowid = "delete from HotIssue a where rowid > ANY (select rowid from HotIssue b where a.text = b.text)"
    cursor.execute(sql_rowid)
    db.commit()

    # cursor.close()
    # db.close()

    HotIssue_text.close()
    HotIssue_img.close()
    HotIssue_url.close()

# 지역별 뉴스 (RegionNews2 로 불러옴)
def RegionNews(region):
    Region_text = open(path_folder+ "/" + region + "_텍스트.txt","r")
    Region_img = open(path_folder+ "/" + region +"_이미지.txt","r")
    Region_url = open(path_folder+"/" + region +"_URL.txt","r")
    Regiondata_text = Region_text.readlines()
    Regiondata_img = Region_img.readlines()
    Regiondata_url = Region_url.readlines()

    for i in Regiondata_text :
        R_Text = i.split('@@')
    for i in Regiondata_img :
        R_Img = i.split('@@')
    for i in Regiondata_url :
        R_Url = i.split('@@')

    num = 0
    a = str(y)

    while num < 2 :
        sql = "INSERT INTO RegionNews(regions,day,text,img,url) VALUES(:1,:2,:3,:4,:5)"
        val = (f"{region}", f"{a}", f"{R_Text[num]}", f"{R_Img[num]}",f"{R_Url[num]}")
        cursor.execute(sql,val)
        db.commit()
        num += 1

    sql_rowid = "delete from RegionNews a where rowid > ANY (select rowid from RegionNews b where a.text = b.text)"
    cursor.execute(sql_rowid)
    db.commit()

    # cursor.close()
    # db.close()

    Region_text.close()
    Region_img.close()
    Region_url.close()

# 지역별 뉴스2
def RegionNews2():
    regions = {'서울':'https://land.naver.com/news/region.naver?city_no=1100000000&dvsn_no=',
    '경기':"https://land.naver.com/news/region.naver?city_no=4100000000&dvsn_no=",
    "인천":"https://land.naver.com/news/region.naver?city_no=2800000000&dvsn_no=",
    "부산":"https://land.naver.com/news/region.naver?city_no=2600000000&dvsn_no=",
    "대전":"https://land.naver.com/news/region.naver?city_no=3000000000&dvsn_no=",
    "대구":"https://land.naver.com/news/region.naver?city_no=2700000000&dvsn_no=",
    "울산":"https://land.naver.com/news/region.naver?city_no=3100000000&dvsn_no=",
    "세종":"https://land.naver.com/news/region.naver?city_no=3600000000&dvsn_no=",
    "광주":"https://land.naver.com/news/region.naver?city_no=2900000000&dvsn_no=",
    "강원":"https://land.naver.com/news/region.naver?city_no=4200000000&dvsn_no=",
    "충북":"https://land.naver.com/news/region.naver?city_no=4300000000&dvsn_no=",
    "충남":"https://land.naver.com/news/region.naver?city_no=4400000000&dvsn_no=",
    "경북":"https://land.naver.com/news/region.naver?city_no=4700000000&dvsn_no=",
    "경남":"https://land.naver.com/news/region.naver?city_no=4800000000&dvsn_no=",
    "전북":"https://land.naver.com/news/region.naver?city_no=4500000000&dvsn_no=",
    "전남":"https://land.naver.com/news/region.naver?city_no=4600000000&dvsn_no=",
    "제주":"https://land.naver.com/news/region.naver?city_no=5000000000&dvsn_no="}
    for i in regions:
        RegionNews(i)

# 함수 불러오기
# CreateTable()
MainNews()
HotIssue()
RegionNews2()

# DB 종료
cursor.close()
db.close()