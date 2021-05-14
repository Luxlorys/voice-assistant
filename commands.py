import sys
import os
import pyttsx3
import speech_recognition
import re
import webbrowser
import wikipediaapi

from datetime import datetime
from help import Help
from random import choice

"""
    This file contain all commands
"""
class Commands(Help):

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.setProperty('voice', voices[3].id)

    coin = ['орел', 'решка']
    cube = [
        'одиниця', 'двійка', 'трійка', 
        'читвірка', 'п"ятірка', 'шістка'
        ]

    hello = [
        'Вітаю, я Сівія', 'Привіт, я Сівія', 'Привітусики',
        'Рада чути вас', 'Добридень', 'Добрий день',
        'Рада вітати вас', 'Доброго здоров"я', 'День добрий',
    ]

    leave = [
        'До зустрічі', 'Побачимося', 'Бувайте',
        'Бувайте здорові', 'Всього вам доброго', 'Всього найкращого',
        'На все добре', 'Була рада вам допомогти', 'Прощавайте',
    ]

    # погода "Город"
    # Переверсти "Слово" на "Язык"
    # курс "Валюта"
    # как дела
    # чем занимаешься

    def shutdown_pc(self, *args):
        self.engine.say('Вимимкаю комп"ютер')
        self.engine.runAndWait()
        os.system('shutdown /s /t 1')


    def restart_pc(self, *args):
        self.engine.say('Перезавантажую комп"ютер')
        self.engine.runAndWait()
        os.system('shutdown /r /t 1')


    def calculate(self, result):
        self.result = result
        self.result = result.split(' ')
        self.result.pop(0)
        self.result = ' '.join(self.result)

        if '+' in self.result:
            self.result = self.result.split(' + ')
            self.result = int(self.result[0]) + int(self.result[1])
            self.engine.say(f'Результат {self.result}')
            self.engine.runAndWait()
        elif '-' in self.result:
            self.result = self.result.split(' - ')
            self.result = int(self.result[0]) - int(self.result[1])
            self.engine.say(f'Результат {self.result}')
            self.engine.runAndWait()
        elif '*' in self.result:
            self.result = self.result.split(' * ')
            self.result = int(self.result[0]) * int(self.result[1])
            self.engine.say(f'Результат {self.result}')
            self.engine.runAndWait()
        elif '/' in self.result:
            self.result = self.result.split(' / ')
            self.result = int(self.result[0]) / int(self.result[1])
            self.result = int(self.result)
            self.engine.say(f'Результат {self.result}')
            self.engine.runAndWait()


    def flip_cube(self, *args):
        self.engine.say(f'Випала {choice(self.cube)}')
        self.engine.runAndWait()


    def flip_coin(self, *args):
        if choice(self.coin) == 'орел':
            self.engine.say('Випав орел')
            self.engine.runAndWait()
        else:
            self.engine.say('Випала решка')
            self.engine.runAndWait()


    def time(self, *args):
        self.now = datetime.now()
        self.hour = self.now.hour
        self.minutes = self.now.minute
        self.engine.say(f'Зараз {self.hour}, {self.minutes}')
        self.engine.runAndWait()

    
    def date(self, *args):
        self.date = datetime.now()
        self.month = self.date.strftime('%m')
        self.day = self.date.strftime('%d')
        self.year = self.date.strftime('%Y')
        self.week_day = self.date.strftime('%A')

        self.years = {
            '2021': 'Дві тисячи двадцять першого',
            '2022': 'Дві тисячи двадцять другого',
            '2023': 'Дві тисячи двадцять третього',
            '2024': 'Дві тисячи двадцять четвертого',
        } # lmao, it sounds better

        self.week = {
            'Monday': 'Понеділок',
            'Tuesday': 'Вівторок',
            'Wednesday': 'Середа',
            'Thursday': 'Четвер',
            'Friday': 'П"ятниця',
            'Saturday': 'Субота',
            'Sunday': 'Неділя'
        }

        self.year_months = {
            '01': 'Січня', '02': 'Лютого', '03': 'Березня',
            '04': 'Квітня', '05': 'Травня', '06': 'Червня',
            '07': 'Липня', '08': 'Серпня', '09': 'Вересня',
            '10': 'Жовтня', '11': 'Листопада', '12': 'Грудня',
        }

        for day in self.week.keys():
            if self.week_day == day:
                self.week_day = self.week[day]

        for day in self.year_months.keys():
            if self.month == day:
                self.month = self.year_months[day]

        for key in self.years.keys():
            if self.year == key:
                self.year = self.years[key]


        self.engine.say(f'Сьогодні {self.week_day}, {self.day}, {self.month}, {self.year} року')
        self.engine.runAndWait()


    def help_user(self, *args):
        self.help_for_user()


    def google_search(self, result):
        self.result = result
        return webbrowser.open(f"https://www.google.com/search?q={self.result}")


    def youtube_search(self, result):
        self.result = result
        self.result = self.result.replace('відео ', "")
        self.result = self.result.replace('включи ', "")
        self.result = self.result.replace('YouTube ', "")
        self.result = self.result.replace('відос ', "")
        
        return webbrowser.open(f'https://www.youtube.com/results?search_query={self.result}')


    def say_hello(self, *args):
        self.engine.say(choice(self.hello))
        self.engine.runAndWait()

    
    def exit_app(self, *args):
        self.engine.say(choice(self.leave))
        self.engine.runAndWait()
        exit()

    
    def search_tearm_in_wiki(self, result):
        self.result = result
        self.result = self.result.replace('що таке ', '')
        self.result = self.result.replace('хто такий ', '')
        self.result = self.result.replace('термін ', '')
        self.result = self.result.replace('слово ', '')
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
            
    
    # the next code causes vomiting
    def record_and_recognize_audio(self):
        """
        1 constant listening to the microphone
        2 loop over all commands (key is command, values is function)
        """
        self.engine.say('очікую команди')
        self.engine.runAndWait()


        while True:

            self.result = ''

            self.r = speech_recognition.Recognizer()
            with speech_recognition.Microphone() as source:
                print('Скажіть що небудь')
                try:
                    self.audio = self.r.listen(source, 3, 3)
                    try:
                        self.result = self.r.recognize_google(self.audio, language='uk-UA')
                    except speech_recognition.UnknownValueError:
                        pass
                    
                except speech_recognition.WaitTimeoutError:
                    pass

                except speech_recognition.RequestError:
                    self.engine.say('Виникли помилки при розпізнанні мови. Перевірте підключення до мережі')
                    self.engine.runAndWait()

            # loop over all tuples
            # я из-за регулярок весь день не кушал, извините за такой плохой код, мне самому не нравится
            for key in self.commands.keys():
                for kkey in key: # loop over all commands inside tuple
                    try:
                        if re.match(kkey, self.result):
                            self.commands[key](self, self.result) #start function
                    except TypeError:
                        pass

        return


    commands = {
    ("привіт", "добрий вечір", "день добрий", "добрий день", "вітаю", "йо", "хай"): say_hello,
    ('пока', "до побачення", "бувай", "виключись", "вимкнись"): exit_app,
    ("знайди", "шукай", "шукати", "гугл", "де знаходиться", "як"): google_search,
    ('відео', "включи відео", "ютуб", "відос", "включи", 'YouTube'): youtube_search,
    ("термін", "слово", "вікіпедія", "вікі", "хто такий", "що таке"): search_tearm_in_wiki,
    ('що ти', "допомога", "допоможи", "як користуватися", 'вміння', "твої вміння"): help_user,
    ('котра година', "скільки годин", "година", "який час", "час", "скільки зараз"): time,
    ('дата', "день", "який день", "який сьогодні день", "сьогодні день"): date,
    ("монетка", "кинь монетку", "жереб", "підкинь жереб", "підкинь монету", "монета"): flip_coin,
    ("гральний кубик", "кинь кубик", "підкинь кубик"): flip_cube,
    ('порахуй', 'розрахуй', 'калькулятор', 'скільки'): calculate,
    ('вимкни ПК', 'виключи ПК', 'завершити роботу ПК', 'вимкнути ПК', 'виключити комп"ютер'): shutdown_pc,
    ('рестарт', 'перезавантаж', 'вимкни та включи', 'рестарт ПК', 'перезагрузи ПК'): restart_pc,
    }
