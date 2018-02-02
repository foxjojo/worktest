import sys 
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QLabel
from PyQt5.QtGui import QIcon,QPixmap,QPainter

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Icon')
        self.button = QPushButton(self)
        self.button.setText("按一下")
        self.button.clicked.connect(self.test)
        pixmap = QPixmap("G:/OneDrive/图片/琉璃神社壁纸包 2016年10月号/29.jpg")
        lb1 = QLabel(self)
        lb1.setPixmap(pixmap)
        
        self.show()

    
    def test(self):
        print("阿勒  按到了")
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
