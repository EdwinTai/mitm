import requests
from bs4 import BeautifulSoup
import time

#計算暫停秒數，避免被誤判成DDOS攻擊
def sleeptime(hour, min, sec):
    return hour*3600 + min*60 + sec

beginyear = 2005 #起始年份
with requests.Session() as s:
    for i in range(beginyear, 2021, 1):#因為有很多年份，根據資料提供者的網頁邏輯更換下列url
        url = "https://lotto.auzonet.com/lotto_historylist_three-star_"+str(i)+".html"
        r1= s.get(url)
        r1.encoding = 'uft-8'  # 解決中文顯示
        soup = BeautifulSoup(r1.text, "lxml")
        for table in soup.findAll('table', {'class': 'history_view_table'}):
            trs = table.find_all('tr')[1:]
            for tr in trs:
                row = ""
                for td in tr.find_all('td'):
                    row += td.text.replace("\n", "")+","
                print(row)
        time.sleep(sleeptime(0, 1, 0)) #一分鐘query一次，避免被以為是DDOS
    
