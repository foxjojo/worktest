from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import xlwt #创建workbook和sheet对象

workbook = xlwt.Workbook() #注意Workbook的开头W要大写 
sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True) 
sheet1.write(0,0,'序号') 
sheet1.write(0,1,'通用名' ) 
sheet1.write(0,2,'剂型') 
sheet1.write(0,3,'规格') 
sheet1.write(0,4,'生产企业') 
sheet1.write(0,5,'进口企业') 
sheet1.write(0,6,'企业报价') 

def store(ids, commonname, types, sizes, outputs, inputs, prices)
    global sheet1
    sheet1.write(ids,0,ids) 
    sheet1.write(ids,1,commonname) 
    sheet1.write(ids,2,types) 
    sheet1.write(ids,3,sizes) 
    sheet1.write(ids,4,outputs)
    sheet1.write(ids,5,inputs) 
    sheet1.write(ids,6,price)
    
def handle_html(url):	
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    title = bsObj.find("tbody").find_all("tr")
    for tr in title:
        td = tr.find_all("td")
        print(td[0].get_text()+" "+td[1].get_text()+" "+td[2].get_text()+" "+td[3].get_text()+" "+td[4].get_text()+" "+td[5].get_text()+" "+td[6].get_text())

if __name__ == '__main__':
    global workbook
    handle_html("http://www.jxyycg.cn/yzxt/publicity/view?id=eb1a21f2ab6a40119544e9048417bc1f")
    workbook.save('D:\\'+time.strftime("%Y-%m-%d", time.localtime())+'.xls') 
    print ('创建excel文件完成！')

