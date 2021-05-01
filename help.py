import pyttsx3

class Help:

    help_text = [
        ('Вітаю, зараз я розповім вам, що я вмію'),
        ('Скажіть "знайти або шукати", щоб зробити запит в гугл'),
        ('Скажіть "Бувай", щоб завершити мою роботу'),
        ('Скажіть "Відео або включи", щоб знайти відео в ютьюбі'),
        ('Скажіть "Термін або Слово", щоб знайти слово в вікіпедії'),
    ]

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.setProperty('voice', voices[3].id)

    def help_for_user(self):
        
        for key in self.help_text:
            self.engine.say(key)
            self.engine.runAndWait()

        return

