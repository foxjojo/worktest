import threading
from time import ctime, sleep
from urllib.request import urlopen
from timeit import timeit

lock = threading.Lock()
a = 0
def time(t):
	url = "http://5sing.kugou.com/yc/rq/"+str(t)
	try:

		if(urlopen(url).code == 200):
			lock.acquire()
			global a
			a = a + 1
			print(a)
			lock.release()
	except Exception as e:
		pass


def mm():

	threads = []
	print(ctime())
	for x in range(1,9999):
		t = threading.Thread(target = time, args = (x,))
		threads.append(t)
		t.start()	

	for z in threads:
		z.join()

if __name__ == '__main__':
	mm()
	#print(timeit('mm()', 'from __main__ import mm', number=1))

