from urllib import request
import requests
from bs4 import BeautifulSoup
import re
import string


def AnalysisUrl(url,  cid):
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    res = request.Request(url,headers = headers)
    html = request.urlopen(res)
    bsObj = BeautifulSoup(html, "html.parser")
    script = bsObj.find_all('script')
    temp = script[4].get_text().split(',')[-3]
    temp_array = temp.split('|')

    old = re.findall(r'\\\'.*\\\'',script[4].get_text())
    old = old[0].replace('\\\'',"")
    old_list = old.split(',')
    print(old_list)
    print(temp_array)
    for o in old_list:
        u = UrlAnalysis(temp_array,o)
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
        headers['Referer'] = url
        ir = requests.get(u, headers = headers)
        name = u.split('?')[0].split('/')[-1]
        if ir.status_code == 200:
            open("G:/"+name, 'wb').write(ir.content)
            print("yes")



def UrlAnalysis(temp_array, old):
    try:
        temp_array[0] = temp_array[0].replace('\'',"")
    except:
        pass
    print(temp_array)
    print(old)
    capital_dict = dict.fromkeys(string.ascii_uppercase, 0)
    capital_list = [chr(i) for i in range(65,91)]
    i = 36
    for temp in capital_list:
        capital_dict[temp] = i
        i = i + 1

    lowercase_letters_dict = dict.fromkeys(string.ascii_lowercase, 0)
    lowercase_letters_list = [chr(i) for i in range(97,123)]
    i = 10
    for temp in lowercase_letters_list:
        lowercase_letters_dict[temp] = i
        i = i + 1

    num_list = [str(i) for i in range(10,91)]
    num_dict = dict.fromkeys(num_list, 0)
    i = 62
    for temp in num_list:
        num_dict[temp] = i
        i = i + 1

    for ce in lowercase_letters_list:
        try:
            old = re.sub(r'(?<=\W)%s(?=\W)'%(ce),temp_array[lowercase_letters_dict[ce]],old)#位置匹配
        except :
            break
    for ce in capital_list:
        try:
            old = re.sub(r'(?<=\W)%s(?=\W)'%(ce),temp_array[capital_dict[ce]],old)#位置匹配
        except:
            break
    for ce in num_list:
        try:
            old = re.sub(r'(?<=\W)%s(?=\W)'%(ce),temp_array[num_dict[ce]],old)
        except:
            break
    for num in range(0,10):
        try:
            old = re.sub(r'(?<=\W)%s(?=\W)'%(num),temp_array[num],old)
        except:
            break
    old = "http" + old[1:]
    print(old)
    return old


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


'''
eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('11 w=[\'8://7-6-9-c-3.2.5/4/f/0/x.h?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/y.h?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/t.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/u.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/v.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/C.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/D.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/E.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/z.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/A.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/B.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/l.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/j.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/m.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/k.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/i.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/n.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/r.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/s.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/q.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/p.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/o.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/F.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/V.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/W.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/U.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/S.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/T.h?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/X.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/N.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/12.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/10.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/Y.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/Z.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/R.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/J.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/K.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/I.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/G.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/H.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/L.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/P.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/Q.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/O.g?e=0&b=a&d=1\',\'8://7-6-9-c-3.2.5/4/f/0/M.g?e=0&b=a&d=1\'];',62,65,'565598||cdndm5|98|40|com|101|manhua1032|http|69|32f0e8371cda88218d6784d723ada4eb|key|161|type|cid|39948|png|jpg|16_2974|13_5230|15_1310|12_1045|14_1108|17_6663|22_6925|21_7725|20_4023|18_1924|19_1395|3_5691|4_8115|5_9961|newImgs|1_2570|2_2038|9_3918|10_2330|11_1351|6_2201|7_2626|8_3098|23_3063|39_8140|40_5433|38_6370|36_4345|37_1897|41_2644|45_8007|30_4913|44_9775|42_2712|43_8882|35_7467|27_8007|28_4477|26_9840|24_8761|25_4377|29_2102|33_7794|34_3493|32_9759|var|31_2662'.split('|'),0,{}))

'''