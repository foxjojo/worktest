import requests
from bs4 import BeautifulSoup
import pymysql
import threading
import time


ThreadCount = 1
ID = 0
lock = threading.Lock()

conn = pymysql.connect(host = '127.0.0.1',user = 'root',passwd = 'root',db = 'mysql',charset = 'utf8')
cur = conn.cursor()
cur.execute("use taiyingshi")

'''
You are getting response.content. But it return response body as bytes (docs). But you should pass str to BeautifulSoup constructor (docs). So you need to use the response.text instead of getting content. 
'''

def OpenUrl(url):
    global ThreadCount, ID
    url = url.strip('\'"')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'

    }
    print(url)
    #re = requests.Request(url,headers = headers)
    try:
        html = requests.get(url,headers = headers).content
    except Exception as e:
        print(e)
        return

    bsObj = BeautifulSoup(html, "html.parser")
    div_list = bsObj.find_all("div", {"class":"pic"})
    for div in div_list:
        title = div.find("span", {"class":"title"}).get_text()
        _url = div.find("a")['href']
        print(title)
        print(_url)
        lock.acquire()

        try:
            cur.execute("insert into dm (name, url, id) values (\"%s\", \"%s\", \"%s\")", (title, _url, ID))
            cur.connection.commit()
            ID = ID + 1
        except Exception as ee:
            print(ee)
            pass

        ThreadCount = ThreadCount + 1
        lock.release()




if __name__ == '__main__':

    id = 491

    cur.execute("select *from dm order by id desc LIMIT 1")
    data = cur.fetchone()
    ID = data[0] + 1

    while 1:

        lock.acquire()
        cur.execute("select* from `dm` where id = " + id.__str__())
        data = cur.fetchone()

        lock.release()
        id = id + 1
        if ThreadCount > 0:

            t = threading.Thread(target = OpenUrl, args = ( data[2], ))
            t.start()
            #OpenUrl(data[2])
            print(data[0])
            lock.acquire()
            ThreadCount = ThreadCount - 1
            lock.release()
        else:
            time.sleep(1)



