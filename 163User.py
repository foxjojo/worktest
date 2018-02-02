from urllib import request
import threading
import bs4
import time
import pymysql
lock = threading.Lock()
ThreadCount = 100

conn = pymysql.connect(host = '127.0.0.1',user = 'root',passwd = 'root',db = 'mysql',charset = 'utf8')
cur = conn.cursor()
cur.execute("use netease")

def OpenUrl(url, id):
    global ThreadCount
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'

    }
    re = request.Request(url,headers = headers)
    try:
        html = request.urlopen(re)
    except Exception as e:
        print(e)
        lock.acquire()
        ThreadCount = ThreadCount + 1
        lock.release()
        return

    bsObj = bs4.BeautifulSoup(html, "html.parser")
    notfound = bsObj.find("script")
    if notfound.get_text()[1] == '{':
        Name = bsObj.find("span", {"class": "tit f-ff2 s-fc0 f-thide"}).get_text()
        Lv = bsObj.find("span", {"class": "lev u-lev u-icn2 u-icn2-lev"}).get_text()
        Area = bsObj.find("div", {"class": "inf s-fc3"}).find("span").get_text()
        if bsObj.find("class", {"class": "icn u-icn u-icn-01"}) ==None:
            Sex = "女"
        else:
            Sex = "男"

        Type = bsObj.find("p", {"class": "djp f-fs1 s-fc3"})
        if Type != None:
            print(Type.get_text())
        Fan_count = bsObj.find("strong", id = "fan_count").get_text()
        print(Sex)
        print(Name)
        print(Lv)
        print(Area)
        print(Fan_count)
        print(id)

        lock.acquire()
        cur.execute("insert into user (Name, Sex, Lv, Area, Fan_count, Netease_id) values (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")", (Name, Sex, Lv, Area, Fan_count, id.__str__()))
        cur.connection.commit()
        ThreadCount = ThreadCount + 1
        lock.release()

    else:
        print("no")
        lock.acquire()
        ThreadCount = ThreadCount + 1
        lock.release()





if __name__ == '__main__':
    id = 29357
    while id<1297200375:
        if ThreadCount > 0:
            t = threading.Thread(target = OpenUrl, args = ("http://music.163.com/user/home?id=" + id.__str__(), id))
            t.start()
            lock.acquire()
            ThreadCount = ThreadCount - 1
            lock.release()
            id = id + 1
            print(id)
        else:
            time.sleep(1)