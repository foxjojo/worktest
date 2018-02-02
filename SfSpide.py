from urllib import request
import bs4
import  threading
import pymysql
import time
lock = threading.Lock()
ThreadCount = 400
conn = pymysql.connect(host = '127.0.0.1',user = 'root',passwd = 'root',db = 'mysql',charset = 'utf8')
cur = conn.cursor()
cur.execute("use sf")




'''

def OpenUrl(page):
    global ThreadCount
    html = request.urlopen("http://book.sfacg.com/List/default.aspx?PageIndex=" + page.__str__())
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    ulList = bsObj.find_all("ul", {"class": "Comic_Pic_List"})
    for ul in ulList:
        name = ul.find('a').find('img')['alt']
        url = ul.find('a')['href']
        print(name)
        print(url)
        lock.acquire()
        cur.execute("insert into novel (name, url) values (\"%s\", \"%s\")", (name, url))
        cur.connection.commit()
        #ThreadCount = ThreadCount + 1
        lock.release()

'''
def OpenUrl(page, id):
    try:
        global ThreadCount
        page = page[1:]
        page = page[:-1]
        print(page)
        htmlurl = "http://book.sfacg.com" + page
        print(htmlurl)
        print(id)
        html = request.urlopen("http://book.sfacg.com" + page)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        divList = bsObj.find("div", {"class": "count-detail"}).find_all('span')
        div2List = bsObj.find("div", id = "BasicOperation").find_all('a')[2].get_text()
        author_name = bsObj.find("div", {"class": "author-name"})
        introduce = bsObj.find("p", {"class": "introduce"}).get_text()
        star = bsObj.find("div", {"class": "num"}).find("span").get_text()
        print(div2List)  # 收藏
        print(introduce)  # 介绍
        print(star)  # 评分
        print(divList[2].get_text())  # 点击
        print(divList[0].get_text())  # 类型
        print(author_name.get_text())  # 作者

        # cur.execute("insert into novel (name, url) values (\"%s\", \"%s\")", (name, url))
        # sql = "UPDATE novel SET click=" + divList[2].get_text() +", collect="+ div2List +" , author="+ author_name.get_text().format() +", introduce="+ introduce +", type="+ divList[0].get_text() +", star=" + star + " WHERE id = "+id.__str__()
        # rint(sql)
        lock.acquire()
        cur.execute("UPDATE novel SET click=%s, collect=%s , author=%s, introduce=%s, type=%s, star=%s WHERE id=%s", (
        divList[2].get_text(), div2List, author_name.get_text(), introduce, divList[0].get_text(), star, id.__str__()))
        cur.connection.commit()
        ThreadCount = ThreadCount + 1
        lock.release()
        # cur.execute(sql)
        # cur.connection.commit()
        '''
            for span in divList:
            name = ul.find('a').find('img')['alt']
            url = ul.find('a')['href']
            print(name)
            print(url)
            lock.acquire()
            cur.execute("insert into novel (name, url) values (\"%s\", \"%s\")", (name, url))
            cur.connection.commit()
            #ThreadCount = ThreadCount + 1
            lock.release()
        '''

    except Exception as e:
        lock.acquire()
        ThreadCount = ThreadCount + 1
        lock.release()






if __name__ == '__main__':
    #global ThreadCount
    '''
    #详情补充
    id = 1
    while id < 45107:
        if ThreadCount > 0:

            lock.acquire()
            cur.execute("select* from `novel` where id = " + id.__str__())
            data = cur.fetchone()
            t = threading.Thread(target=OpenUrl, args=(data[1], id))
            t.start()
            ThreadCount = ThreadCount - 1
            id = id + 1
            lock.release()
        else:
            time.sleep(1)
            
    
    
    '''
    #数据完整校验
    id = 1
    while id < 45107:
        if ThreadCount > 0:

            lock.acquire()
            cur.execute("select* from `novel` where id = " + id.__str__())
            data = cur.fetchone()
            if data[2] == None:
                t = threading.Thread(target = OpenUrl, args = (data[1], id))
                t.start()
                ThreadCount = ThreadCount - 1
                id = id + 1
                lock.release()
            else:

                id = id + 1
                lock.release()
                print("略过")
                print(id)
        else:
            time.sleep(1)


'''
#单线程版
    for id in range(103, 2256):
        cur.execute("select* from `novel` where id = " + id.__str__())
        data = cur.fetchone()
        print(data[0])
        print(data[1])
        OpenUrl(data[1], id)
'''

'''
#多线程爬取资源名  从目录中
    page = 1
    while page < 2254:
        if ThreadCount > 0:
            lock.acquire()
            print(page)
            t = threading.Thread(target=OpenUrl, args=(page, ))
            t.start()
            ThreadCount = ThreadCount - 1
            page = page + 1
            lock.release()
        else:
            time.sleep(1)

'''
