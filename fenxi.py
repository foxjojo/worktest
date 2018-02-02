from urllib.request import urlopen
import json
js = urlopen("http://service.5sing.kugou.com/analysis/songGraph?jsoncallback=type=1&SongID=38&SongType=yc")
print(js.rq)