# settings.py
import os

class Config:
    # Основные настройки
    DEBUG = False
    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_ROOT = 'content'
    POST_DIR = 'posts'
    PORT_DIR = 'portfolio'
    
    # Настройки сайта
    SITE_NAME = "Мой Портфолио Блог"
    AUTHOR = "Дуплей Максим Игоревич"
    DESCRIPTION = "Персональный блог и портфолио разработчика"
    THEME = "light"
    
    # Пути
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    FREEZER_DESTINATION = os.path.join(BASE_DIR, 'build')
    
    # Дополнительные параметры
    PYGMENTS_STYLE = 'monokai'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'

# Выбираем конфигурацию
settings = Config()