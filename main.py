from commands import Commands
from help import Help
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

class App(Commands, QMainWindow, Help):
    """
    GUI for assistant
    """

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.setWindowTitle('Голосовий асистент CVA')
        self.setWindowIcon(QIcon('img/voice-assistant.png'))
        self.setIconSize(QSize(20, 20))
        self.setFixedSize(520, 400)
        self.setGeometry(300, 300, 574, 421)
        self.setStyleSheet("background-image: url(img/back.jpg);")

        self.font = QFont()
        self.font.setFamily("Bahnschrift SemiBold")
        self.font.setPointSize(10)
        self.font.setBold(True)
        self.font.setWeight(75)

        self.help_btn = QPushButton(self)
        self.help_btn.setGeometry(5, 5, 90, 30)
        self.help_btn.setIcon(QIcon('img/help2.png'))
        self.help_btn.setText('Допомога')
        self.help_btn.setIconSize(QSize(17, 17))
        self.help_btn.setShortcut('F2')
        self.help_btn.setStyleSheet("color: #02386E; border-radius: 10px")
        self.help_btn.setCursor(QCursor(Qt.WhatsThisCursor))
        self.help_btn.setFont(self.font)
        self.help_btn.setToolTip('Натисніть клавішу F1, щоб дізнатися про можливості асистента')
        self.help_btn.clicked.connect(self.help_for_user)

        self.btn = QPushButton(self)
        self.btn.setGeometry(230, 300, 55, 90)
        self.btn.setIcon(QIcon('img/microphone.png'))
        self.btn.setIconSize(QSize(70, 100))
        self.btn.setShortcut('F1')
        self.btn.setStyleSheet("color: black; border-radius: 20px")
        self.btn.setToolTip('Натисніть клавішу F2, щоб дати команду асистенту')
        self.btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn.clicked.connect(self.record_and_recognize_audio)

        self.show()

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())