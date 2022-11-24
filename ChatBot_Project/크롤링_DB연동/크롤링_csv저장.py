import cx_Oracle
dsn = cx_Oracle.makedsn("localhost",1521,"orcl")
db = cx_Oracle.connect('ora_user','human123', dsn, encoding='utf8')
cursor = db.cursor()

# csv로 저장
import pandas as pd
sql = "select * from MainNews"
sql2 = "select * from HotIssue"
sql3 = "select * from RegionNews"

cursor.execute(sql)
a = cursor.fetchall()

cursor.execute(sql2)
b = cursor.fetchall()

cursor.execute(sql3)
c = cursor.fetchall()

df = pd.DataFrame(a,columns=["day","text","img","url"])
df.to_csv("C:/Users/h/Desktop/temp221014/코딩자료(java,python 등)/ChatBot_Project/data/MainNews.csv", index=False)

df2 = pd.DataFrame(b,columns=["day","text","img","url"])
df2.to_csv("C:/Users/h/Desktop/temp221014/코딩자료(java,python 등)/ChatBot_Project/data/HotIssue.csv", index=False)

df3 = pd.DataFrame(c,columns=["regions","day","text","img","url"])
df3.to_csv("C:/Users/h/Desktop/temp221014/코딩자료(java,python 등)/ChatBot_Project/data/RegionNews.csv", index=False)

cursor.close()
db.close()