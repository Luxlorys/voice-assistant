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
        self.setWindowIcon(QIcon('img/voice_icon.png'))
        self.setGeometry(300, 300, 520, 400)
        self.setStyleSheet("background-image: url(img/phone1.png);")

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
        self.help_btn.setStyleSheet("color: #fff;")
        self.help_btn.setFont(self.font)
        self.help_btn.clicked.connect(self.help_for_user)

        self.btn = QPushButton(self)
        self.btn.setGeometry(230, 300, 55, 90)
        self.btn.setIcon(QIcon('img/micro.png'))
        self.btn.setIconSize(QSize(50, 80))
        self.btn.setShortcut('F1')
        self.btn.clicked.connect(self.record_and_recognize_audio)

        self.show()

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())