class Message:

    """
    A class for generating messages that will be used to inform the user .
    """

    @staticmethod
    def start(first_name: str, last_name: str) -> str:
        return f'Привіт 👋 {first_name} {last_name}. ' \
               f'Для додавання музики 🎧 у цей чат просто надішли мені посилання на YouTube відео ' \
               f'яке ти хочеш перетворити в аудіо.'

    @staticmethod
    def help() -> str:
        return 'Цей 🤖 розроблений для додавання аудіозаписів, які ти зможеш прослуховувати безкоштовно. ' \
               'Їх даний бот завантажує з YouTube посилань.'

    @staticmethod
    def inappropriate_text() -> str:
        return 'Будь ласка передайте посилання на YouTube відео запис, аудіо якого ви хочете зберегти. 🤔'

    @staticmethod
    def success_downloaded() -> str:
        return '<strong>Процес завантаження аудіо файлу:</strong> \n ' \
               '✅ Завантаження файлу завершено. \n Гарного прослуховування 😁'

    @staticmethod
    def downloading_file() -> str:
        return '<strong>Процес завантаження аудіо файлу:</strong> \n ' \
               '⏳ Завантажую файл із YouTube. \n Це може зайняти якийсь час 😅'

    @staticmethod
    def unavailable_link(availability: str) -> str:
        return f'😔 Вибачте але завантажити дане відео не вдалось. Повний опис причини: \n {availability}'

    @staticmethod
    def unworked_link() -> str:
        return '🥴 Вибачте але дане посилання не можливо відкрити. ' \
               '🤔 Переконайтесь у правильності посиланні та відправте нове.'
