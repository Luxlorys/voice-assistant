from logging import exception
# import sys
import os
import pyttsx3
from pyttsx3 import engine
import speech_recognition
import re
import webbrowser
import wikipediaapi
import pyowm

from datetime import datetime
from help import Help
from random import choice
from GoogleNews import GoogleNews

class Commands(Help):
    '''
        this class contains functions that a voice assistant can perform
        each function performs a separate functionality
        
    '''

    # speech settings 
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30) 
    engine.setProperty('voice', voices[3].id) # id[3] is ukrainian localization on my computer

    # google new settings
    googlenews = GoogleNews()
    googlenews.set_lang('ua')

    coin = ['орел', 'решка'] # if user say 'flip coin' 

    cube = [
        'одиниця', 'двійка', 'трійка', 
        'читвірка', 'п"ятірка', 'шістка'
        ] # if user say 'flip cube'

    # if user say 'hallo'
    hello = [
        'Вітаю, я Сівія', 'Привіт, я Сівія', 'Привітусики',
        'Рада чути вас', 'Оо, це ви? давно не бачилися', 'Добрий день',
        'Рада вітати вас', 'Доброго здоров"я', 'День добрий',
        'Добридень', 'Ну нарешті ви повернулися', 'знову ви? і чого вам треба цього разу?'
    ]

    # if user leave
    leave = [
        'До зустрічі', 'фух, ось і перерва на попоїсти', 'Побачимося', 'Сподіваюся почути вас знову',
        'Бувайте здорові', 'Всього вам доброго', 'Всього найкращого',
        'На все добре', 'Була рада вам допомогти', 'Прощавайте',
        'щось я запихалася, нарешті зможу відпочити'
    ]

    # if user say 'how are you?'
    mood = [
        'Як завжди все добре, а ти як?', 'Настрій відмінний - як перед вихідними', 'Сплю і бачу страшний сон, в якому ти у мене питаєш, як в мене справи',
        'Все добре, дякую, що цікавитеся. А ви як?', 'Мрію про щасливе майбутнє', 'Як у казці!', 
        'Як завжди - відмінно', 'Дякую. Все гаразд', 'У вашій компанії стало краще'
    ]
    
    actions = [
        'Протираю пил з посуду, що стоїть на моєму столі', 'Мрію про щасливе майбутнє', 'Займаюся метанням слини в стелю',
        'Намагаюся навчити кота говорити «привіт»', 'Вирішила влаштувати дегустацію чаю', 'Відзначаю день міста в Кейптауні', 
        'Переглядаю «Санта-Барбару», останній сезон', 'Ставлю рекорд з поїдання мармеладу', 'Сушу сухарі'
    ]

    music_list = [
        'http://surl.li/wyfs', 'http://surl.li/wyfu', 'http://surl.li/wyfw',
        'http://surl.li/wyfx', 'http://surl.li/wygc', 'http://surl.li/wygd'
    ]

    def open_random_music(self, *args):
        return webbrowser.open(choice(self.music_list))


    def get_news(self, result):
        self.result = result
        self.result = self.result.replace('новини ', '')
        self.result = self.result.replace('які новини в ', '')
        self.result = self.result.replace('які сьогодні новини в ', '')
        self.result = self.result.replace('актуальні новини в ', '')
        self.result = self.result.replace('актуальні новини ', '')
        
        try:
            self.googlenews.search(self.result)
            self.googlenews.get_page(1)
            self.links = self.googlenews.get_links()
            self.titles = self.googlenews.get_texts()
            
            for link in self.links[0:5]:
                webbrowser.open(link)

            for title in self.titles[0:5]:
                self.engine.say(title)
                self.engine.runAndWait()

        except exception:
            self.engine.say()
            self.engine.runAndWait()


    def get_info_about_assistant(self, *args):
        self.engine.say('Добре, що ви спитали, давно хотіла з кимось поговорити')
        self.engine.say(' мене звуть Сівія, дуже просте ім"я, чи не правда')
        self.engine.say('я багато чого вмію, але хочу ще більше, сподіваюся програмісти, які мене розробляли модифікують мене')
        self.engine.say('Якщо ж ви хочете детальніше дізнатися про всі мої можливості то просто натисніть Ф2 або на кнопку Допомога')
        self.engine.runAndWait()


    def get_weather(self, result):
        self.result = result
        self.result = self.result.replace('погода ', '')
        self.result = self.result.replace('яка погода ', '')
        self.result = self.result.replace('яка сьогодні погода в ', '')
        
        self.owm = pyowm.OWM('6f7f209b9973d7cfbdcbf0c6c651eb3f')
        self.mgr = self.owm.weather_manager()

        try:
            self.observation = self.mgr.weather_at_place(self.result)
            self.w = self.observation.weather

            self.valid_temperature = self.w.temperature('celsius')['temp']
            self.max_temperature = self.w.temperature('celsius')['temp_max']
            self.min_temperature = self.w.temperature('celsius')['temp_min']

            self.engine.say(f'Сьогодні в місті {self.result} {int(self.valid_temperature)} градусів')
            self.engine.say(f'Максимальна кількість градусів - {int(self.max_temperature)+2}')
            self.engine.say(f'Мінімальна кількість градусів - {int(self.min_temperature)-4}')
            self.engine.runAndWait()
        # if city not found
        except pyowm.commons.exceptions.NotFoundError:
            self.engine.say('Вибачте, я не почула в якому місті потрібно дізнатися погоду')
            self.engine.runAndWait()


    def speak_with_user(self, result):
        self.result = result
        if self.result == 'як справи' or self.result == 'як ти' or self.result == 'як твої справи':
            self.engine.say(choice(self.mood))
            self.engine.runAndWait()
        elif self.result == 'що робиш' or self.result == 'чим займаєшся' or self.result == 'що нового':
            self.engine.say(choice(self.actions))
            self.engine.runAndWait()


    def shutdown_pc(self, *args):
        try:
            self.engine.say('Вимимкаю комп"ютер')
            self.engine.runAndWait()
            os.system('shutdown /s /t 1')
        except exception:
            self.engine.say('Виникли помилки при вимкненні комп"ютера')
            self.engine.runAndWait()


    def restart_pc(self, *args):
        try:
            self.engine.say('Перезавантажую комп"ютер')
            self.engine.runAndWait()
            os.system('shutdown /r /t 1')
        except exception:
            self.engine.say('Виникли помилки при перезавантаженні комп"ютера')
            self.engine.runAndWait()


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
        self.engine.say(f'Ось що я знайшла по запиту {self.result}')
        self.engine.runAndWait()
        return webbrowser.open(f"https://www.google.com/search?q={self.result}")


    def youtube_search(self, result):
        self.result = result
        self.engine.say(f'Ось що я знайшла по запиту {self.result}')
        self.engine.runAndWait()
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
        self.engine.say('очікую команду')
        self.engine.runAndWait()

        self.r = speech_recognition.Recognizer()
        
        while True:
            self.result = ''

            # self.r = speech_recognition.Recognizer()
            with speech_recognition.Microphone() as source:
                
                try:
                    self.audio = self.r.listen(source, 3, 3)
                    try:
                        self.result = self.r.recognize_google(self.audio, language='uk-UA')
                        self.result = self.result.lower()
                    except speech_recognition.UnknownValueError:
                        pass
                    
                except speech_recognition.WaitTimeoutError:
                    pass

                except speech_recognition.RequestError:
                    self.engine.say('Виникли помилки при розпізнанні мови. Перевірте підключення до мережі')
                    self.engine.runAndWait()
            
            # я из-за регулярок весь день не кушал, извините за такой плохой код, мне самому не нравится
            for key in self.commands.keys(): # loop over all tuples
                for item in key: # loop over all commands inside tuple
                    try:
                        if re.match(item, self.result):
                            self.commands[key](self, self.result) #start function
                    except TypeError:
                        pass
            
        return


    commands = {
    ("привіт", "добрий вечір", "день добрий", "добрий день", "вітаю", "йо", "хай"): say_hello,
    ('пока', "до побачення", "бувай", "виключись", "вимкнись"): exit_app,
    ("знайди", "шукай", "шукати", "гугл", "де знаходиться", "курс", "який курс", "загугли"): google_search,
    ('відео', "включи відео", "ютуб", "відос", 'youtube'): youtube_search,
    ("термін", "слово", "вікіпедія", "вікі", "хто такий", "що таке"): search_tearm_in_wiki,
    ('що ти', "допомога", "допоможи", "як користуватися", 'вміння', "твої вміння"): help_user,
    ('котра година', "скільки годин", "година", "який час", "час", "скільки зараз"): time,
    ('дата', "день", "який день", "який сьогодні день", "сьогодні день", "яка сьогодні дата", "який зараз рік"): date,
    ("монетка", "кинь монетку", "жереб", "підкинь жереб", "підкинь монету", "монета"): flip_coin,
    ("гральний кубик", "кинь кубик", "підкинь кубик"): flip_cube,
    ('порахуй', 'розрахуй', 'калькулятор', 'скільки'): calculate,
    ('вимкни ПК', 'виключи ПК', 'завершити роботу ПК', 'вимкнути ПК', 'виключити комп"ютер', "заверши роботу пк"): shutdown_pc,
    ('рестарт', 'перезавантаж', 'вимкни та включи', 'рестарт ПК', 'перезагрузи ПК'): restart_pc,
    ('як справи', 'як ти', 'як твої справи', 
    'що робиш', 'чим займаєшся', 'що нового'): speak_with_user,
    ('погода', 'яка погода', 'яка сьогодні погода'): get_weather,
    ('хто ти така', 'розкажи про себе', 'як тебе звуть', 'інформація про асистента'): get_info_about_assistant,
    ('новини', 'які сьогодні новини в ', 'актульні новини в ', 'актуальні новини ', 'які новини в '): get_news,
    ('включи музику', 'музика', 'хочу послухати музику', 'відкрий музику', 'слухати музику'): open_random_music
    }
