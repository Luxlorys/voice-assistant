import sys
import pyttsx3
import speech_recognition
import re
import webbrowser
import wikipediaapi

from datetime import datetime
from help import Help

"""
    This file contain all commands
"""
class Commands(Help):

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.setProperty('voice', voices[3].id)


    def time(self, *args):
        self.now = datetime.now()
        self.hour = self.now.hour
        self.minutes = self.now.minute
        self.engine.say(f'Зараз {self.hour} годин, {self.minutes} хвилин')
        self.engine.runAndWait()

    
    def date(self, *args):
        self.now = datetime.now()
        self.week_day = self.now.strftime('%A')

        if self.week_day == 'Monday':
            self.week_day = 'Понеділок'
        elif self.week_day == 'Tuesday':
            self.week_day = 'Вівторок'
        elif self.week_day == 'Wedesday':
            self.week_day = 'Середа'
        elif self.week_day == 'Thursday':
            self.week_day = 'Четвер'
        elif self.week_day == 'Friday':
            self.week_day = 'П"ятнися'
        elif self.week_day == 'Saturday':
            self.week_day = 'Субота'
        else:
            self.week_day == 'Неділя'

        self.engine.say(f'Сьогодні {self.week_day}')
        self.engine.runAndWait()


    def help_user(self, *args):
        self.help_for_user()

    # seach for tearm on google
    def google_search(self, result):
        self.result = result
        return webbrowser.open(f"https://www.google.com/search?q={self.result}")


    def youtube_search(self, result):
        self.result = result.split(' ')
        self.command = self.result[0]
        self.result.remove(self.command)
        self.result = ' '.join(self.result)
        
        return webbrowser.open(f'https://www.youtube.com/results?search_query={self.result}')

    def say_hello(self, *args):
        self.engine.say('Вітаю, я Сівія')
        self.engine.runAndWait()

    
    def exit_app(self, *args):
        self.engine.say('Була рада допомогти вам')
        self.engine.runAndWait()
        exit()

    
    def search_tearm_in_wiki(self, result):
        self.result = result.split(' ')
        self.result.pop(0)
        self.result = ' '.join(self.result)
        self.wiki = wikipediaapi.Wikipedia('uk')
        self.wiki_page = self.wiki.page(self.result)
        
        try:
            if self.wiki_page.exists():
                webbrowser.open(self.wiki_page.fullurl)
                self.engine.say(str(self.wiki_page.summary.split(".")[:3]))
                self.engine.runAndWait()
            else:
                webbrowser.open(f'https://google.com/search?q={self.result}')
        except Exception:
            pass

        return
            
    
    def record_and_recognize_audio(self):
        """
        1 constant listening to the microphone
        2 loop over all commands (key is command, values is function)
        """
        self.engine.say('Вітаю вас, очікую команди')
        self.engine.runAndWait()


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

            # loop over all tuples
            for key in self.commands.keys():
                for kkey in key: # loop over all commands inside tuple
                    if re.match(kkey, self.result):
                        self.commands[key](self, self.result) #start function

        return

    commands = {
    ("знайди", "шукай", "шукати", "гугл", "де знаходиться"): google_search,
    ("привіт", "хай", "йо", "привєт", "вітаю"): say_hello,
    ('пока', "до побачення", "бувай", "виключись", "вимкнись"): exit_app,
    ('відео', "включи відео", "ютуб", "відос"): youtube_search,
    ("термін", "слово", "вікіпедія", "вікі", "хто такий", "що таке"): search_tearm_in_wiki,
    ('що ти', "допомога", "допоможи", "як користуватися", 'вміння', "твої вміння"): help_user,
    ('яка година', "скільки годин", "година", "який час", "час", "скільки зараз"): time,
    ('дата', "день", "який день", "який сьогодні день", "сьогодні день"): date
    }
