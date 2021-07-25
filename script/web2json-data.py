#!python3

from urllib import request
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9))

url = 'https://www.pref.saga.lg.jp/kiji00380273/index.html'

response = request.urlopen(url)
retrieveAt = datetime.now(JST)
retYear = retrieveAt.year
retMonth = retrieveAt.month
retDay = retrieveAt.day
ISOretrieveAt = str(retrieveAt.isoformat(timespec='seconds'))

soup = BeautifulSoup(response, features="html.parser")
response.close()

d = {}
d['見出し'] = soup.find('title').get_text(strip=True)
d['retrievedAt'] = ISOretrieveAt
tbls = soup.find_all('table', {'class': '__wys_table'})
captext = tbls[0].find_all('caption')[0].get_text(strip=True)
d[captext] = {}
trs = tbls[0].find_all('tr')
for k in range(len(trs)):
  tds = trs[k].find_all('td')
  d[captext][tds[0].get_text(strip=True)] = tds[1].get_text(strip=True)
captext = soup.find_all('h3', {'class': 'title'})[0].get_text(strip=True)
d[captext] = {}
trs = tbls[1].find_all('tr')
for k in range(len(trs)):
  tds = trs[k].find_all('td')
  d[captext][tds[0].get_text(strip=True)] = tds[1].get_text(strip=True)
          
storeDir = './data/data/{}/{}/{}'.format(retYear, retMonth, retDay)
os.makedirs(storeDir, exist_ok=True)
fn = '{}/{}'.format(storeDir, ISOretrieveAt)
fnl = './data/data/data-latest.json'
fpout  = open(fn, 'w')
json.dump(d, fpout, ensure_ascii=False, indent=4)
fpout.close()
fplout  = open(fnl, 'w')
json.dump(d, fplout, ensure_ascii=False, indent=4)
fplout.close()
