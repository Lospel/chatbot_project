import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

x = datetime.now()
y = x.date()
a = str(y)

path_folder = "C:/Users/h/Pictures/"+ a
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 
createFolder(path_folder)

# 주요뉴스
def naver_sites_all(url):
  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  titles = soup.select("ul.headline_list dt a")[:4]
  titles2 = soup.select("dt.photo a")[:2] 
  news_thumbnail = soup.select('dt.photo img')[:2]
  places_title = []
  places_url= []
  link_thumbnail = []

  for one in titles:
    if one.string != None:
      places_title.append(one.string)
  for i in places_title[:1]:
    MainNewsText01 = i
  for i in places_title[1:2]:
    MainNewsText02 = i

  for i in titles2:
    places_url.append("https://land.naver.com"+i.attrs["href"])
  for i in places_url[:1]:
    MainNewsUrl01 = i
  for i in places_url[1:2]:
    MainNewsUrl02 = i

  for img in news_thumbnail:
    link_thumbnail.append(img.attrs['src'])
  for i in link_thumbnail[:1]:
    MainNewsImg01 = i
  for i in link_thumbnail[1:2]:
    MainNewsImg02 = i

  f = open(path_folder+"/주요뉴스_텍스트.txt","w")
  f.write(MainNewsText01+"@@")
  f.write(MainNewsText02)
  f.close()

  f = open(path_folder+"/주요뉴스_이미지.txt","w")
  f.write(MainNewsImg01+"@@")
  f.write(MainNewsImg02)
  f.close()

  f = open(path_folder+"/주요뉴스_URL.txt","w")
  f.write(MainNewsUrl01+"@@")
  f.write(MainNewsUrl02)
  f.close()

# 핫이슈
def naver_hotissue_all(url):
  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  titles = soup.select("div.hot_list strong")[:4]
  titles2 = soup.select("dt.photo a")[:2]
  news_thumbnail = soup.select('dt.photo img')[:2]
  places_title = []
  places_url=[]
  link_thumbnail = []

  for one in titles:
    if one.string != None:
      places_title.append(one.string)
  for i in places_title[:1]:
    HotIssueText01 = i
  for i in places_title[1:2]:
    HotIssueText02 = i

  for i in titles2:
    places_url.append("https://land.naver.com"+i.attrs["href"])
  for i in places_url[:1]:
    HotIssueUrl01 = i
  for i in places_url[1:2]:
    HotIssueUrl02 = i

  for img in news_thumbnail:
    link_thumbnail.append(img.attrs['src'])
  for i in link_thumbnail[:1]:
    HotIssueImg01 = i
  for i in link_thumbnail[1:2]:
    HotIssueImg02 = i

  f = open(path_folder+"\핫이슈_텍스트.txt","w")
  f.write(HotIssueText01+"@@")
  f.write(HotIssueText02)
  f.close()

  f = open(path_folder+"\핫이슈_이미지.txt","w")
  f.write(HotIssueImg01+"@@")
  f.write(HotIssueImg02)
  f.close()

  f = open(path_folder+"\핫이슈_URL.txt","w")
  f.write(HotIssueUrl01+"@@")
  f.write(HotIssueUrl02)
  f.close()

# 지역별 뉴스 텍스트, 이미지, URL 가져오기
def naver_region_all(url):
  global RegionImg01
  global RegionImg02
  global RegionText01
  global RegionText02
  global RegionUrl01
  global RegionUrl02

  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  news_thumbnail = soup.select('dt.photo img')[:2]
  titles = soup.select("div.section_headline dt a")[:4]
  titles2 = soup.select("dt.photo a")[:2]
  places_url=[]  
  places_title = []
  link_thumbnail = []

  for img in news_thumbnail:
      link_thumbnail.append(img.attrs['src'])
  for i in link_thumbnail[:1]:
    RegionImg01 = i
  for i in link_thumbnail[1:2]:
    RegionImg02 = i

  for one in titles:
    if one.string != None:
      places_title.append(one.string)
  for i in places_title[:1]:
    RegionText01 = i
  for i in places_title[1:2]:
    RegionText02 = i

  for i in titles2:
    places_url.append("https://land.naver.com"+i.attrs["href"])
  for i in places_url[:1]:
    RegionUrl01 = i
  for i in places_url[1:2]:
    RegionUrl02 = i
def Region(region):
  f = open(path_folder+ "\\" + region + "_텍스트.txt","w")
  f.write(RegionText01+"@@")
  f.write(RegionText02)
  f.close()

  f = open(path_folder+ "\\" + region + "_이미지.txt","w")
  f.write(RegionImg01+"@@")
  f.write(RegionImg02)
  f.close()

  f = open(path_folder+ "\\" + region + "_URL.txt","w")
  f.write(RegionUrl01+"@@")
  f.write(RegionUrl02)
  f.close()
def RegionNews():
  
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

  for i in regions :
    naver_region_all(regions[i])
    Region(i)

# 함수 실행
naver_sites_all("https://land.naver.com/news/headline.naver")
naver_hotissue_all("https://land.naver.com/news/hotIssue.naver")
RegionNews()