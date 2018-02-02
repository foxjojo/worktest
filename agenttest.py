from urllib.request import urlopen, ProxyHandler, build_opener

def check_agent(ip, port):
	d = {'http': ''}
	d['http'] = 'http://' + str(ip) + ':' + str(port) + '/'
	print(d)
	proxy_support = ProxyHandler(d)
	opener = build_opener(proxy_support)
	print(opener.open("http://5sing.kugou.com/yc/1.html").code)
	try:
		if(opener.open("http://5sing.kugou.com/yc/1.html").code == 404):
			return True
		else:
			return False
	except Exception as e:
		return False

if __name__ == '__main__':
	try:
		urlopen("http://5sing.kugou.com/yc/1.html")
	except Exception as e:
		if e.code == 404:
			print("asdasdadasd")
	#print(.code == 404)
	urlopen("http://5sing.kugou.com/yc/1.html")
	print(check_agent("103.231.218.126","53281"))