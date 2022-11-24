import cx_Oracle
from datetime import datetime
x = datetime.now()
y = x.date()
a = str(y)
path_folder = "C:/Users/h/Pictures/ "+ a

dsn = cx_Oracle.makedsn("localhost",1521,"orcl")
db = cx_Oracle.connect('ora_user','human123', dsn, encoding='utf8')
cursor = db.cursor()

# 지역별 뉴스
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
# def RegionNews2():
  
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
cursor.close()
db.close()