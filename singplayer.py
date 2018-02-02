import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QResizeEvent
from PyQt5.Qt import QMediaPlayer, QUrl, QMediaContent
import requests
from pydub import AudioSegment

lrcFilePath = "D:/5sing/lrc/" 
picFilePath = "D:/5sing/pic/"


class web(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1000, 500)
        self.setWindowTitle('5SING')


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('5SING')

        #布局管理器
        layout = QGridLayout()
        mainLayout = QGridLayout()

        #歌词计时器
        self.startTimer(100)

        #头像控件
        self.la = QLabel(self)
        self.la.adjustSize()
        self.la.setWordWrap(True)

        #歌词及效果显示区
        self.lrcLabel = QLabel(self)
        self.lrcLabel.setPixmap(
            QPixmap("G:/10.jpg").scaled(self.height() * 0.8,
                                        self.height() * 0.8))
        self.lrcLabel.resize(self.width(), self.height() * 0.8)
        self.lrcLabel.setScaledContents(True)

        #测试按钮
        self.button = QPushButton(self)
        self.button.setText("按一下")
        self.button.clicked.connect(self.test)

        #播放按钮
        self.buttonplay = QPushButton(self)
        self.buttonplay.setText("play")
        self.buttonplay.clicked.connect(self.play)

        #添加布局
        mainLayout.addWidget(self.lrcLabel, 0, 0)
        layout.addWidget(self.la, 1, 0)
        layout.addWidget(self.button, 1, 1)
        layout.addWidget(self.buttonplay, 1, 2)

        mainLayout.addLayout(layout, 1, 0)
        self.setLayout(mainLayout)

        #self.song = AudioSegment.from_mp3("C:/Users/14514/Music/萧忆情Alex - 十二镇魂歌（Cover 星尘）.mp3")
        self.show()

    def resizeEvent(self, size):
        #窗口大小改变事件
        self.resize(size.size())

    def timerEvent(self, event):
        print("a")

    def play(self):
        #暂停及播放函数
        # QMediaPlayer::StoppedState	0	The media player is not playing content, playback will begin from the start of the current track.
        # QMediaPlayer::PlayingState	1	The media player is currently playing content.
        # QMediaPlayer::PausedState	    2	The media player has paused playback, playback of the current track will resume from the position the player was paused at.

        if self.song.state() == 1:
            self.song.pause()
            self.buttonplay.setText("play")
        else:
            self.song.play()
            self.buttonplay.setText("pause")

    def test(self):
        #json测试函数
        html = requests.get(
            "http://service.5sing.kugou.com/song/find?songinfo=yc$3504548")
        print(html.json())
        aa = requests.get(html.json()[0]["avatar"])

        with open(lrcFilePath + 'test.5sing', 'wb') as lrcFile:
            lrcFile.writelines(
                str(html.json()[0]["id"]) + "\n" + html.json()[0]["songname"] +
                "\n" + html.json()[0]["nickname"] + "\n")
        with open(picFilePath + 'test.jpg', 'wb') as lrcFile:
            lrcFile.write(aa.content)
        self.LrcData()

        self.la.setPixmap(
            QPixmap(picFilePath + "test.jpg").scaled(self.height() * 0.2,
                                                     self.height() * 0.2))
        self.la.setScaledContents(True)
        self.la.resize(self.height() * 0.2, self.height() * 0.2)

        self.song.setMedia(QMediaContent(QUrl(html.json()[0]["sign"])))
        self.song.setVolume(50)
        self.song.play()

    def LrcData(self, nowTime="", songId="", songType=""):
        #lrcJson = requests.get("http://5sing.kugou.com/fm/m/json/lrc?songId="+ songId +"&songType="+ songType)
        lrcJson = requests.get(
            "http://5sing.kugou.com/fm/m/json/lrc?songId=3504548&songType=yc"
        )  #测试代码
        print(lrcJson.json())
        lrcFile = open(lrcFilePath + 'test.5sing', 'a')
        if lrcJson.json()['isSuccess'] == 'true':  #请求成功
            if lrcJson.json()['lrc']['type'] == 1:  #支持滚动
                for l in lrcJson.json()['lrc']['data']['lrc']:
                    print(l['time'])
                    lrcFile.writelines(str(l['time']) + " " + l['text'] + "\n")
                lrcFile.close()
            elif lrcJson.json()['lrc']['type'] == 0:  #不支持滚动
                pass
        else:
            pass

        return lrcJson.json()

    def lrcScroll(self, nowTime, lrcJson):
        #readline()
        pass


class Lrc(QLabel):
    def funcname(self, parameter_list):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())