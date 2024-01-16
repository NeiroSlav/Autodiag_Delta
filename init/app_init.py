import datetime
import logging
import os
from flask import Flask, render_template, session
from .user_settings import UserSettings

# инициализация лога
date_time = str(datetime.datetime.now()).split('.')[0]
date_time = date_time.replace(' ', '-').replace(':', '-')
log_file_path = os.path.join('log', f'LOG-{date_time}.log')
logging.basicConfig(level=logging.INFO, filename=log_file_path, filemode="w",
                    format="%(asctime)s %(levelname)s | %(message)s")


# инициализация приложения flask
static_dir = os.path.abspath('static/')
template_dir = os.path.abspath('templates/')
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
app.secret_key = os.urandom(12)  # назначение секретного ключа (чтобы работали сессии)

flask_log = logging.getLogger('werkzeug')  # перенаправление лога flask
flask_log.disabled = True  # и выключение его, чтобы не видеть get-запросы

user_sets = UserSettings()


# собственный класс исключений
class DiagError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# функция отрисовки ошибки
def render_error(err_text):
    return render_template(
        'error.html',
        title='Ошибка', topinfo=err_text,
        theme=session['theme'])
