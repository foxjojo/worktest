from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
def getTitle(url):
	try:
		html = urlopen(url)
	except (HTTPError, URLError) as e:
		raise None
	try:
		bs = BeautifulSoup(html.read())
		title = bs.findAll("span", {"class":"green"})
	except AttributeError as e:
		return None
	return title
title = getTitle("http://www.pythonscraping.com/pages/warandpeace.html")
if title == None:
	print("not be found")
else:
	for x in title:
		print(x.get_text())