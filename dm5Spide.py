from urllib import request
import requests
from bs4 import BeautifulSoup
import re

datapat = re.compile('\d?\d_\d\d\d\d_?\d?\d?\d?')
keypat = re.compile('\|(\w){32}\|')
fivepat = re.compile('\D(\d){5}\|')
twopat = re.compile('\|(\d){2}\|')
def AnalysisUrl(url,  cid):
    print(url)
    succeshost = ''
    #globals(datapat, keypat, fivepat, twopat,)
    sonhost = [ "manhua1025-101-69-161-98.cdndm5.com",
                "manhua1032-104-250-150-10.cdndm5.com",
                "manhua1032-101-69-161-99.cdndm5.com"]
    imgurl = []
    two_url= ''
    five_url = ''
    key_url = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    re = request.Request(url,headers = headers)
    html = request.urlopen(re)
    bsObj = BeautifulSoup(html, "html.parser")
    script = bsObj.find_all('script')
    test = script[4].get_text().split(',')[-3]
    print(test)
    five = fivepat.finditer(script[4].get_text())
    two = twopat.finditer(script[4].get_text().replace('10', ''))
    for t in two:
        two_url = t.group(0)[1:-1]
        print(t.group(0)[1:-1])
    for f in five:
        five_url = f.group(0)[1:-1]
        print(f.group(0)[1:-1])

    datalist = datapat.finditer(script[4].get_text())
    keylist = keypat.finditer(script[4].get_text())
    for key in keylist:
        key_url = key.group(0)
        print(key.group(0))
    for id in datalist:
        print(id.group(0))

        if succeshost == '':
            for host in sonhost:
                #print(host)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
                headers['Referer'] = url
                print("http://"+ host + '/' +  two_url + '/' + five_url + '/' + cid[1:].__str__() +'/' + id.group(0) + ".jpg?cid=" + cid[1:].__str__() + "&key=" +key_url[1:-1] + "&type=1")
                #print(requests.get("http://"+ host + '/' +  two_url + '/' + five_url + '/' + cid[1:].__str__() +'/' + id.group(0) + ".jpg?cid=" + cid[1:].__str__() + "&key=" +key_url[1:-1] + "&type=1", headers = headers))
                if requests.get("http://"+ host + '/' +  two_url + '/' + five_url + '/' + cid[1:].__str__() +'/' + id.group(0) + ".jpg?cid=" + cid[1:].__str__() + "&key=" +key_url[1:-1] + "&type=1", headers = headers).status_code == 200:
                    succeshost = host
                    print(host)
                    break
        imgurl.append("http://"+ succeshost + '/' + two_url + '/' + five_url + '/' + cid[1:].__str__() +'/' + id.group(0) + ".jpg?cid=" + cid[1:].__str__() + "&key=" +key_url[1:-1] + "&type=1")
    for urll in imgurl:
        print(urll)
        print(requests.get(urll).status_code)


def Chapeters(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    re = request.Request(url,headers = headers)
    html = request.urlopen(re)
    bsObj = BeautifulSoup(html, "html.parser").find('div', id = "chapterList_1")
    chapterList = bsObj.find_all('li')
    for chapter in chapterList:

        AnalysisUrl("http://m.dm5.com"+chapter.find('a')['href'], chapter.find('a')['href'][1:-1])

def cookie():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    html = requests.get("http://m.dm5.com/", headers = headers)
    print(html.cookies)

if __name__ == '__main__':
    Chapeters("http://m.dm5.com/manhua-tangyinzaiyijie1/")
    #AnalysisUrl("http://m.dm5.com/m244489/", datapat, keypat, fivepat, twopat, 244489)
