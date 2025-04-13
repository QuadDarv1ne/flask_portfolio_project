"""
Flask-приложение для генерации статического блога и портфолио.

Использует:
- Flask-FlatPages для обработки markdown-страниц
- Frozen-Flask для генерации статических файлов
- Pygments для подсветки синтаксиса

Структура контента:
- Посты блога: /content/posts/*.md
- Проекты портфолио: /content/portfolio/*.md
- Общие настройки: settings.txt
"""

import sys
import json
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from settings import settings  # Импортируем настройки

# Конфигурация приложения
DEBUG = False  # Режим отладки
FLATPAGES_EXTENSION = '.md'  # Расширение файлов контента
FLATPAGES_ROOT = 'content'  # Корневая директория контента
POST_DIR = 'posts'  # Директория постов блога
PORT_DIR = 'portfolio'  # Директория проектов портфолио

app = Flask(__name__)
flatpages = FlatPages(app)  # Инициализация FlatPages
freezer = Freezer(app)  # Инициализация Frozen-Flask
app.config.from_object(__name__)  # Загрузка конфигурации


@app.route("/")
def index():
    """
    Главная страница сайта.
    
    Собирает данные для отображения:
    - Последние посты блога, отсортированные по дате
    - Проекты портфолио, отсортированные по названию
    - Настройки из файла settings.txt
    - Уникальные теги из метаданных страниц
    
    Возвращает:
        Отрендеренный шаблон index.html с контекстом:
        - posts: список постов блога
        - cards: список проектов портфолио
        - bigheader: флаг для отображения большого заголовка
        - settings: словарь с настройками
        - tags: множество уникальных тегов
    """
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=True)
    cards = [p for p in flatpages if p.path.startswith(PORT_DIR)]
    cards.sort(key=lambda item: item['title'])
    
    # Загрузка настроек из файла (ИСПРАВЛЕННЫЙ БЛОК)
    with open('settings.txt', encoding='utf8') as config:
        settings = json.load(config)  # Правильное чтение файла
    
    # Сбор уникальных тегов
    tags = {p.meta.get('tag').lower() for p in flatpages if p.meta.get('tag')}

    return render_template(
        'index.html',
        posts=posts,
        cards=cards,
        bigheader=True,
        **settings,
        tags=tags
    )

@app.route('/posts/<name>/')
def post(name):
    """
    Страница поста блога.
    
    Параметры:
        name (str): Имя файла markdown-поста без расширения
    
    Возвращает:
        Отрендеренный шаблон post.html с контекстом:
        - post: объект страницы FlatPage
        
    Исключения:
        404: Если страница не найдена
    """
    path = f'{POST_DIR}/{name}'
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


@app.route('/portfolio/<name>/')
def card(name):
    """
    Страница проекта портфолио.
    
    Параметры:
        name (str): Имя файла markdown-проекта без расширения
    
    Возвращает:
        Отрендеренный шаблон card.html с контекстом:
        - card: объект страницы FlatPage
        
    Исключения:
        404: Если страница не найдена
    """
    path = f'{PORT_DIR}/{name}'
    card = flatpages.get_or_404(path)
    return render_template('card.html', card=card)


@app.route('/pygments.css')
def pygments_css():
    """
    Генерирует CSS для подсветки синтаксиса Pygments.
    
    Возвращает:
        Стили CSS для выбранной темы (monokai) с правильным Content-Type
    """
    return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}


@app.errorhandler(404)
def page_not_found(e):
    """
    Обработчик ошибки 404.
    
    Возвращает:
        Отрендеренный шаблон 404.html с кодом 404
    """
    return render_template('404.html'), 404


if __name__ == "__main__":
    # Запуск приложения в режиме разработки или сборки
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()  # Генерация статического сайта
    else:
        app.run(
            host='127.0.0.1',  # Локальный хост
            port=5001,         # Порт по умолчанию
            debug=DEBUG        # Режим отладки согласно конфигурации
        )