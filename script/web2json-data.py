#!python3

from urllib import request
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9))

#url = 'https://www.pref.saga.lg.jp/kiji00373220/index.html'
url = 'https://www.pref.saga.lg.jp/kiji00380157/index.html'

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
rows = tbls[0].find_all('tr')
t = []
t.append([k.get_text(strip=True) for k in rows[0].find_all('th')])
for e in rows[1:]:
  t.append([k.get_text(strip=True) for k in e.find_all('td')])
d['患者発生状況'] = t
rows = tbls[1].find_all('tr')
t = []
t.append([k.get_text(strip=True) for k in rows[0].find_all('th')])
for e in rows[1:]:
  t.append([k.get_text(strip=True) for k in e.find_all('td')])
d['検査実施状況'] = t
rows = tbls[2].find_all('tr')
t = []
t.append([k.get_text(strip=True) for k in rows[0].find_all('th')])
for e in rows[1:]:
  t.append([k.get_text(strip=True) for k in e.find_all('td')])
d['PCR等検査陽性者一覧'] = t
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
