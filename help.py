import pyttsx3

class Help:

    help_text = [
        ('Вітаю, зараз я розповім вам, що я вмію'),
        ('Скажіть "знайти або шукати", щоб зробити запит в гугл'),
        ('"Бувай", щоб завершити мою роботу'),
        ('"Відео або включи", щоб знайти відео в ютьюбі'),
        ('"Термін або Слово", щоб знайти слово в вікіпедії'),
        ('Дата, щоб дізнатися дату'),
        ('Яка година, щоб дізнатися час'),
        ('Підкинь жереб, щоб кинути монетку'),
        ('Кубик, щоб підкинути гральний кубик'),
        ('Порахуй, а потім виріз, щоб провести простий розрахунок'),
        ('Вимкни ПК, щоб завершити роботу комп"ютер'),
        ('Рестар ПК, щоб перезавантажити комп"ютер'),
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

