import sys
import pyttsx3
import speech_recognition
import re
import webbrowser
import wikipediaapi

"""
    This file contain all commands
"""
class Commands:

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.setProperty('voice', voices[3].id)

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
        
        if self.wiki_page.exists():
            webbrowser.open(self.wiki_page.fullurl)
            self.engine.say(str(self.wiki_page.summary.split(".")[:3]))
            self.engine.runAndWait()
        else:
            webbrowser.open(f'https://google.com/search?q={self.result}')
        
        return
            


    
    def record_and_recognize_audio(self):
        """
        1 constant listening to the microphone
        2 loop over all commands (key is command, values is function)
        """
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
                        # self.commands[key] = list(self.commands[key])

                        self.commands[key](self, self.result) #start function

        return

    commands = {
    ("знайди", "шукай", "шукати", "гугл", "де знаходиться"): google_search,
    ("привіт", "хай", "йо", "привєт", "вітаю"): say_hello,
    ('пока', "до побачення", "бувай", "виключись", "вимкнись"): exit_app,
    ('відео', "включи відео", "ютуб", "відос"): youtube_search,
    ("термін", "слово", "вікіпедія", "вікі", "хто такий", "що таке"): search_tearm_in_wiki
    }
