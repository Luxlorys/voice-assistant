from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys
import pyttsx3
import speech_recognition
import re
import webbrowser


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)


def google_search(result):
    return webbrowser.open("https://www.google.com/search?q=" + result)


def say_hello(*args):
    engine.say('Привіт і тобі')
    engine.runAndWait()


commands = {
    ("що таке", "шо таке", "що такє"): google_search,
    ("привіт", "хай", "йо", "привєт"): say_hello,
}


def record_and_recognize_audio():

    result = ''

    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print('Скажіть що небудь')
        audio = r.listen(source, 4, 4)

    result = r.recognize_google(audio, language='uk-UA')

    # seatching in google
    for key in commands.keys():
        for kkey in key:
            if re.match(kkey, result):
                commands[key](result)

    return


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle('Simple program')
    window.setGeometry(300, 300, 300, 300)

    btn = QtWidgets.QPushButton(window)
    btn.move(100, 70)
    btn.setText('Слухати')
    btn.setGeometry(150, 150, 100, 100)
    btn.clicked.connect(record_and_recognize_audio)


    window.show()
    sys.exit(app.exec_())