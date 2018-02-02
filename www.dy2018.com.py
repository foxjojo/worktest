# www.dy2018.com 测试脚本
from urllib.request import urlopen, HTTPError, Request
import threading
import pymysql
from bs4 import BeautifulSoup


conn1 = pymysql.connect(host='127.0.0.1',
                        user='root',
                        passwd='root',
                        db='mysql',                       charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)
cur1 = conn1.cursor()
cur1.execute("use dy2018")


def DownloadUrl(id, url):
    cur1.execute(
        "insert into url (id, url) values (\"%s\", \"%s\")", (id, url))
    conn1.commit()


def spideInformation(url):
    try:
        html = urlopen(url).read()
        html = html.decode('gbk', 'ignore').encode('utf-8')
        bsObj = BeautifulSoup(html, "html.parser")
        print("命中" + str(id))
        title = bsObj.find("div", id="Zoom").find_all("p")
        urllist = bsObj.find_all("td", {"bgcolor": "#fdfddf"})
        urlName = bsObj.find_all("div", class_="title_all")
        for t in urlName:
            if t.find("h1") == None:
                pass
            else:
                temp, urlName = t.find("h1").get_text().split('《')
                urlName, temp = urlName.split('》')
                break
        for url in urllist:
            print(urlName)
            DownloadUrl(urlName, url.find('a').get_text())

    except HTTPError as e:
        print(id)
        print(e.code)
        LOCK.acquire()
        THREADCOUNT = THREADCOUNT + 1
        LOCK.release()   


def SpideUrl(id):
    urlList = []
    html = urlopen("http://117.169.20.240:9090/4/index_" + str(id) + ".html").read()
    html = html.decode('gbk', 'ignore').encode('utf-8')
    bsObj = BeautifulSoup(html, "html.parser")
    tableList = bsObj.find_all("table", class_="tbspan")
    for url in tableList:
        print("a")
        print(url.find("a", title=True)['href'])
        urlList.append(url.find("a", title=True)['href'])

    for u in urlList:
        print(u[-10:-5])
        spideInformation("http://117.169.20.240:9090"+ u)
'''
if __name__ == '__main__':
	spideInformation("http://117.169.20.240:9090/html/gndy/jddy/52928.html")
'''
if __name__ == '__main__':
    for x in range(35, 36):
        SpideUrl(x)
        print(x)
    conn1.close()
