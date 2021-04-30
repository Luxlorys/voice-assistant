from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QApplication, QMainWindow
from commands import Commands

import sys

class App(Commands):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.window = QMainWindow()

        self.window.setWindowTitle('Голосовий асистент CVA')
        self.window.setGeometry(500, 500, 500, 500)

        self.btn = QtWidgets.QPushButton(self.window)
        self.btn.move(50, 50)
        self.btn.setText('Слухати')
        self.btn.clicked.connect(self.record_and_recognize_audio)
        
        self.window.show()

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())