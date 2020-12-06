#!python3

from urllib import request
from bs4 import BeautifulSoup
import sys
import re
import json
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9))

url = 'https://www.pref.saga.lg.jp/list04342.html'
response = request.urlopen(url)
retrieveAt = str(datetime.now(JST).isoformat(timespec='seconds'))
soup = BeautifulSoup(response, features="html.parser")
response.close()
divs = soup.find_all('div', attrs={'class': 'mainblock'})
data = {}
out = []
ymdpat = re.compile('([0-9][0-9][0-9][0-9])年([0-9][0-9]*)月([0-9][0-9]*)日')
for k in divs:
    update = k.span.contents[0]
    href = k.a.get('href')
    text = k.a.get_text(strip=True)
    res = ymdpat.match(update)
    yy = res.groups()[0].zfill(4)
    mm = res.groups()[1].zfill(2)
    dd = res.groups()[2].zfill(2)
    d = '{}@@{}@@{}'.format(yy, mm, dd)
    res = href.split('/')
    u = '{}@@{}'.format(res[0], res[1])
    item = {}
    item['date'] = d
    item['url'] = 'https:@@@@www.pref.saga.lg.jp@@{}'.format(u)
    item['text'] = text
    out.append(item)
data['retrieveAt'] = retrieveAt
data['newsItems'] = out
fn = './data/news/{}'.format(retrieveAt)
fnl = './data/news/news-latest.json'
fpout  = open(fn, 'w')
fpout.write(json.dumps(data, indent=4, ensure_ascii=False).replace('@@', r'\/'))
fpout.close()
fplout  = open(fnl, 'w')
fplout.write(json.dumps(data, indent=4, ensure_ascii=False).replace('@@', r'\/'))
fplout.close()
