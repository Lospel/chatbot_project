from urllib.request import urlretrieve
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
x = datetime.now()
y = x.date()
path_folder2 = r"C:\Users\h\Pictures"
path_folder = path_folder2 +"\ " + str(y)
if not os.path.isdir(path_folder):
    os.mkdir(path_folder)

def crawling_sites_img(url):
  response = requests.request("GET", url)
  soup = BeautifulSoup(response.content,'html.parser')
  news_thumbnail = soup.select('dt.photo img')
  link_thumbnail = []
  for img in news_thumbnail:
      link_thumbnail.append(img.attrs['src'])
  i = 0
  for link in link_thumbnail:          
    i += 1
    urlretrieve(link, path_folder +f"\{y}_"+ f'{i}.jpg')

url = "https://land.naver.com/news/headline.naver"
crawling_sites_img(url)