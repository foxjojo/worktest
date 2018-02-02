from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql

conn = pymysql.connect(host = '45.32.57.50',
						user = 'root',
						passwd = 'mypass',
						db = 'mysql', 
						unix_socket = 'run/mysqld/mysqld.sock', 
						charset = 'utf8')
cur = conn.cursor()
cur.execute("use PythonSpide")

random.seed(datetime.datetime.now())

def store(title, renqi, songid):

	try:
		if (title != "中国原创音乐基地 5SING"):
			cur.execute("insert into pages (title, renqi, songid) values (\"%s\", \"%s\", \"%s\")", (title, renqi, songid))
			cur.connection.commit()
	except Exception as e:
		raise e
	else:
		pass

def getlinks(articleUrl):
	html = urlopen("http://en.wikipedia.org"+articleUrl)
	bsObj = BeautifulSoup(html)
	title = bsObj.find("h1").get_text()
	content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
	store(title, content)
	return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href = re.compile("^(/wiki/)((?!:).)*$"))

links = getlinks("/wiki/Kevin_Bacon")

try:
	while len(links) > 0:
		newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
		print(newArticle)
		links = getlinks(newArticle)
except Exception as e:
	raise e
finally:
	cur.close()
	conn.close()
