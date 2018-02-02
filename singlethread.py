from urllib.request import urlopen
from timeit import timeit

a=0
def time(t):
	url = "http://5sing.kugou.com/yc/rq/"+str(t)
	try:
		print(urlopen(url).code)
		global a
		a=a+1
		print(a)
	except Exception as e:
		pass


def mm():
	for x in range(1,9999):
		print(x)
		time(x)	

if __name__ == '__main__':
	print(timeit('mm()', 'from __main__ import mm', number=1))