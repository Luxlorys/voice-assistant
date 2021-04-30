import sys
import pyttsx3
import speech_recognition
import re
import webbrowser


class Commands:

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.setProperty('voice', voices[3].id)

    def google_search(self, result):
        self.result = result
        return webbrowser.open("https://www.google.com/search?q=" + self.result)


    def say_hello(self, *args):
        self.engine.say('Вітаю, я Сівія')
        self.engine.runAndWait()

    
    def exit_app(self, *args):
        self.engine.say('Була рада допомогти вам')
        self.engine.runAndWait()
        exit()

    
    def record_and_recognize_audio(self):
        while True:
            self.result = ''

            r = speech_recognition.Recognizer()
            with speech_recognition.Microphone() as source:
                print('Скажіть що небудь')
                try:
                    self.audio = r.listen(source, 4, 4)
                    try:
                        self.result = r.recognize_google(self.audio, language='uk-UA')
                    except speech_recognition.UnknownValueError:
                        pass

                except speech_recognition.WaitTimeoutError:
                    pass

            # seatching in google
            for key in self.commands.keys():
                for kkey in key:
                    if re.match(kkey, self.result):
                        self.commands[key](self, self.result)

        return

    commands = {
    ("що таке", "шо таке", "що такє"): google_search,
    ("привіт", "хай", "йо", "привєт"): say_hello,
    ('пока', "до побачення", "бувай", "виключись", "вимкнись"): exit_app,
    }
