import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout,QVBoxLayout,QScrollArea
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QResizeEvent
from PyQt5.Qt import QMediaPlayer, QUrl, QMediaContent
import requests
import time
import re
import copy
import threading
import bs4
from functools import partial  

lrcFilePath = "E:/5sing/lrc/" 
picFilePath = "E:/5sing/pic/"



class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #初始化目录
        if(os.path.exists(lrcFilePath) == False):
            os.makedirs(lrcFilePath)
        if(os.path.exists(picFilePath) == False):
            os.makedirs(picFilePath)


        self.setWindowTitle('5SING')
        self.resize(700,500)
        #布局管理器
        layout = QGridLayout()
        self.mainLayout = QGridLayout()

        #歌词计时器
        self.startTimer(100)

        #头像控件
        self.la = QLabel(self)
        self.la.adjustSize()
        self.la.setWordWrap(True)

        #歌词及效果显示区
        self.lrcLabel = QLabel(self)
        # self.lrcLabel.setPixmap(
        #     QPixmap("G:/10.jpg").scaled(self.height() * 0.8,
        #                                 self.height() * 0.8))
        self.lrcLabel.resize(self.width(), self.height() * 0.8)
        self.lrcLabel.setScaledContents(True)
        self.tempWebRank = self.lrcLabel

        #测试按钮
        self.button = QPushButton(self)
        self.button.setText("歌词")
        self.button.clicked.connect(self.lrcDisplay)

        #播放载体
        self.song = QMediaPlayer()

        #播放按钮
        self.buttonplay = QPushButton(self)
        self.buttonplay.setText("play")
        self.buttonplay.setStyleSheet("color: blue")
        self.buttonplay.clicked.connect(self.play)

        #测试网页按钮
        self.button1 = QPushButton(self)
        self.button1.setText("排行榜")
        self.button1.clicked.connect(self.web)

        #添加布局
        self.mainLayout.addWidget(self.lrcLabel, 0, 0)
        layout.addWidget(self.la, 1, 0)
        layout.addWidget(self.button, 1, 1)
        layout.addWidget(self.buttonplay, 1, 2)
        layout.addWidget(self.button1,1,3)

        self.mainLayout.addLayout(layout, 1, 0)
        self.setLayout(self.mainLayout)

        #self.song = AudioSegment.from_mp3("C:/Users/14514/Music/萧忆情Alex - 十二镇魂歌（Cover 星尘）.mp3")
        self.show()
    def lrcDisplay(self):
        self.tempWebRank.close()
        qLabell = QLabel(self)
        qLabell.setText("Loading")
        self.mainLayout.replaceWidget(self.tempWebRank,qLabell)
        self.tempWebRank = qLabell
        t = threading.Thread(target=self.lrcScroll, args=("songid", qLabell))
        t.start()
        t.setName("lrcThreading")
        

    def web(self):
        a = self.webRank()
        t = threading.Thread(target=self.webRank, args=())
        t.start()
        t.setName("webRank")


    def webRank(self):
        scrollWidget = QScrollArea()
        childLayout = QVBoxLayout()
        mainWidget = QWidget()

        html = requests.get("http://5sing.kugou.com/top/")#原创音乐榜
        bsObj = bs4.BeautifulSoup(html.content, "html.parser")
        rank_list = bsObj.find('div',class_="rank_list")
        list_one = rank_list.find_all('tr')
        for one in list_one[1:]:
            val = one.find('td', class_="r_td_1").find('input').get('value')#js参数
            name = one.find('td', class_="r_td_3").find_all('a')[-1]['title']#.get_text()#歌曲名
            print(val)
            print(name)
            temp = QPushButton(name)
            temp.clicked.connect(partial(self.playInfmation, val))
            '''
            temp.clicked.clicked.connect(lambda: self.playInfmation(val))  
            使用lambda表达式所有信号槽的参数都会被修改为循环最后一次所要传递的参数
            用partial才不会出错
            from functools import partial  
            '''
            childLayout.addWidget(temp)
        
        mainWidget.setLayout(childLayout)
        scrollWidget.setWidget(mainWidget)
        scrollWidget.setAutoFillBackground(True)
        scrollWidget.setWidgetResizable(True)

        self.mainLayout.replaceWidget(self.tempWebRank,scrollWidget)
        self.tempWebRank = scrollWidget
        return

    def playInfmation(self, value):
        self.test(value[:-3])
        self.LrcData(value[:-3],value[-2:])

    def resizeEvent(self, size):
        #窗口大小改变事件
        self.resize(size.size())

    def timerEvent(self, event):
        if self.song.state() == 1:
            pass
            #self.lrcScroll(self.song.position()," ")
        else:
            pass

    def play(self):
        # 暂停及播放函数
        # QMediaPlayer::StoppedState	0	The media player is not playing content, playback will begin from the start of the current track.
        # QMediaPlayer::PlayingState	1	The media player is currently playing content.
        # QMediaPlayer::PausedState	    2	The media player has paused playback, playback of the current track will resume from the position the player was paused at.

        if self.song.state() == 1:
            self.song.pause()
            self.buttonplay.setText("play")
        else:
            self.song.play()
            self.buttonplay.setText("pause")

    def test(self, songId):
        print(songId)
        for a in threading.enumerate():
            if a.getName() == "lrcThreading":
                print(a)
        #json测试函数
        html = requests.get(
            "http://service.5sing.kugou.com/song/find?songinfo=yc$"+songId)
        # html = requests.get(
        #     "http://service.5sing.kugou.com/song/find?songinfo=yc$3504548")
        print(html.json())
        print(html.json()[0]["id"])
        aa = requests.get(html.json()[0]["avatar"])
        temp = str(html.json()[0]["id"]) + '\n' + html.json()[0]["songname"] + '\n' + html.json()[0]["nickname"] + '\n'
        print(temp)
        with open(lrcFilePath + 'test.5sing', 'w') as lrcFile:
            lrcFile.writelines(temp)
        with open(picFilePath + 'test'+html.json()[0]["avatar"][-4:], 'wb') as lrcFile:
            lrcFile.write(aa.content)
        self.LrcData()

        self.la.setPixmap(
            QPixmap(picFilePath + 'test'+html.json()[0]["avatar"][-4:]).scaled(self.height() * 0.2,
                                                     self.height() * 0.2))
        self.la.setScaledContents(True)
        self.la.resize(self.height() * 0.2, self.height() * 0.2)
        

        self.song = QMediaPlayer()
        self.song.setMedia(QMediaContent(QUrl(html.json()[0]["sign"])))
        self.song.setVolume(50)
        self.song.play()


    def LrcData(self, songId="", songType=""):
        print(songType)
        print(songId)
        lrcJson = requests.get("http://5sing.kugou.com/fm/m/json/lrc?songId="+ songId +"&songType="+ songType)
        # lrcJson = requests.get(
        #     "http://5sing.kugou.com/fm/m/json/lrc?songId=3504548&songType=yc"
        # )  #测试代码
        lrcFile = open(lrcFilePath + 'test.5sing', 'a')
        if lrcJson.json()['isSuccess'] == True:  #请求成功
            if lrcJson.json()['lrc']['type'] == 1:  #支持滚动
                lrcFile.writelines("1"+ "\n")
                for l in lrcJson.json()['lrc']['data']['lrc']:
                    if l['text'] == "":
                        lrcFile.writelines(str(l['time']) + " " + "------"+ "\n")
                    else:
                        lrcFile.writelines(str(l['time']) + " " + l['text'] + "\n")
                    
                lrcFile.close()
            elif lrcJson.json()['lrc']['type'] == 0:  #不支持滚动
                lrcFile.writelines("0"+ "\n")
                lrcFile.writelines(lrcJson.json()['lrc']['data'].replace('''<br />''',"\n"))
                lrcFile.close()
        else:
            pass

    def lrcScroll(self, lrcName, qLabel):
        #lrcFile = open(lrcFilePath + lrcName + '.5sing', 'r')
        lrcList = []
        with open(lrcFilePath + 'test.5sing', 'r') as lrcFile:#测试
            lrcList = lrcFile.readlines()
        i = 0
        if self.song.state() == 1:
            while i < len(lrcList): 
                if re.match(r"\d+\s{1}\S", lrcList[i]) != None:
                    lrc = lrcList[i].split(' ',1)
                    while True:
                        if int(lrc[0]) <= self.song.position():
                            i = i + 1
                            break
                        else:
                            try:
                                a = lrcList[i-1].split(' ',1)[1]
                                if qLabel.text() != a:
                                    qLabel.setText(a)
                                    pass
                                else:
                                    pass
                            except :
                                pass

                else:
                    i = i + 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())