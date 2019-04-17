from urllib import request
from bs4 import BeautifulSoup
import requests, json
import datetime
import secrets as s

URL = s.URL
WEB_HOOK_URL = s.WEB_HOOK_URL

class Day:
    def __str__(self):
        return '{} 本館:{} ST:{}'.format(self.date, self.honkan4f, self.st)

    def __init__(self, date):
        self.date = date
        self.honkan4f = []
        self.st = []

def GetDay(num):
    #get html
    html = request.urlopen(URL)

    #set BueatifulSoup
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)

    #get headlines
    table = soup.find_all("table")[1]
    days_row = table.find_all('tr')[1:]
    days = []
    for day_row in days_row:
        d = day_row.find_all('td')
        day = Day(d[0].string)
        for yotei in d[1].find_all('font'):
            day.honkan4f.append(yotei.text)
        for yotei in d[2].find_all('font'):
            day.st.append(yotei.text)
        days.append(day)
    today = days[num - 1]
    if(len(today.honkan4f)==0 and len(today.st)==0):
        ret = '今日は会議室の予約はありません'
    else:
        ret = '本館4F\n{}\n\nSTビル\n{}'.format( '\n'.join(today.honkan4f), '\n'.join(today.st))
    return ret

def Post(text):
    requests.post(WEB_HOOK_URL, data = json.dumps({
        'text': text,  #通知内容
        'username': 'Kaigishitu-bot',  #ユーザー名
    }))

if __name__ == "__main__":
    today = datetime.date.today().day
    reserveInfo = GetDay(today)
    text = 'おはようございます。\n' + reserveInfo + '\n' + URL
    print(text)