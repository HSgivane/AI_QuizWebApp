test_shablon = '''
1. Какой из пакетов Python является основным для backend-разработки веб-приложений?

Варианты ответов:
a) Django
b) PyQt
c) Tkinter
d) Flask

Ответ: a) Django

2. Какой тип данных в Python используется для хранения нескольких одновременно доступных значений с идентичными именами?

Варианты ответов:
a) dict
b) list
c) tuple
d) set

Ответ: b) list

3. Что возвращает функция len() в Python?

Варианты ответов:
a) Имя введённого пользователем
b) Длину надстрочных отступов в блоке кода
c) Длину данного именименного объекта на языке программирования
d) Длину строки, которая передаётся внутри функции len()

Ответ: d) Длину строки, которая передаётся внутри функции len()

4. Какое значение для переменной, объявленной как bool, будет получено по умолчанию?

Варианты ответов:
a) True
b) False
c) 0
d) 1

Ответ: b) False

5. Какую из стандартных библиотек Python используют для сетевых запросов?

Варианты ответов:
a) requests
b) socket
c) Tkinter
d) PyQt

Ответ: a) requests
'''

def get_prompt_test(topic):
    prompt_test = f"""
    Составь тест из 10 вопросов по теме "{topic}".

    Формат должен быть строго следующим:

    1. Вопрос с формулировкой

    Варианты ответов:
    a) ...
    b) ...
    c) ...
    d) ...

    Ответ: <правильный вариант полностью>

    Не пиши пояснений, не добавляй вводных или заключений. Просто блоки вопросов и вариантов, как в примере ниже.

    Пример формата:

    1. Какой из пакетов Python является основным для backend-разработки веб-приложений?

    Варианты ответов:
    a) Django  
    b) PyQt  
    c) Tkinter  
    d) Flask  

    Ответ: a) Django

    Соблюдай точно такой же стиль, пробелы, отступы, без markdown, без HTML, только текст.
    """
    return prompt_test

def get_prompt_score(correct_questions, incorrect_questions):
    prompt_score = f"""
    Ты — преподаватель по программированию.

    Правильно отвеченные вопросы:
    {chr(10).join(correct_questions)}

    Ошибки пользователя:
    {chr(10).join(incorrect_questions)}

    На основе этого:

    1. Определи уровень знаний пользователя: начальный / ниже среднего / средний / выше среднего / продвинутый;
    2. Выдели, какие темы он понимает, а где есть пробелы;
    3. Дай краткие рекомендации: что повторить, какие темы изучить;
    4. Не упоминай тест, не используй ссылки, не предлагай конкретные ресурсы.

    Формат ответа — 3–6 предложений, в дружелюбном тоне, как если бы ты давал советы лично.
    """
    return prompt_score