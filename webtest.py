import requests
import bs4
url = "https://makeabooking.flyscoot.com/Book/Flight"
payload = {'revAvailabilitySelect.init': '', 'revAvailabilitySelect.MarketKeys[0]': '0~O1~~O1TRA~2000~~1~X|TR~+588~+~~SIN~01/28/2018+19:15~MLE~01/28/2018+20:50~'}
html = requests.post(url,data = payload)
f = open('test.html', 'w') # 若是'wb'就表示写二进制文件
f.write(html.text)
f.close()