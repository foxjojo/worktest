# http://www.beiwo.tv 测试脚本
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
cur1.execute("use animation")


def DownloadUrl(name, url):
    print(name)
    cur1.execute(
        "insert into list (name, url) values (\"%s\", \"%s\")", (name, url))
    conn1.commit()


def spideInformation(url):
    try:
        html = urlopen(url).read()
        bsObj = BeautifulSoup(html, "html.parser")
        print("命中" + str(id))
        title = bsObj.find("ul", class_="img-list clearfix").find_all("li")
        urllist = bsObj.find_all("h5")
        for url in urllist:
            DownloadUrl(url.find('a').get_text(),"http://www.beiwo.tv"+url.find('a')['href'])

    except HTTPError as e:
        print(id)
        print(e.code)

if __name__ == '__main__':
    # for x in range(2, 166):
    #     spideInformation("http://www.beiwo.tv/list/3/index-" + str(x) + ".html")
    #     print(x)
    spideInformation(" http://www.beiwo.tv/list/3/index.html")
       
    conn1.close()