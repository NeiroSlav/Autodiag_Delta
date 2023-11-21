import gc
import os
import threading
import time
from functools import wraps
from random import randint
from flask import Flask, jsonify, render_template, redirect, request

static_dir = os.path.abspath('static/')
template_dir = os.path.abspath('templates/')
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
app.secret_key = os.urandom(12)
_token_dict = {}


# собственный класс исключений
class DiagError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# функция отрисовки ошибки
def render_error(err_text):
    return render_template(
        'index.html',
        title='Ошибка', topinfo=err_text)


#


# функция создания токена
def token_init():
    while True:  # пока токен не будет уникальным
        token = str(randint(a=10000, b=99999))
        if not token_exists(token):
            break

    _token_dict[token] = {  # начальные значения:
        '_busy_query': [],  # очередь занятости токена,
        '_last_active': int(time.time()),  # время последней активности
        '_changes': [],
        'first_time_flag': True,
    }
    print(int(time.time()), token)
    return token


# проверка наличия токена
def token_exists(token):
    return token in _token_dict


# запись объекта в токен
def token_set(token: str, name: str, obj):
    _token_dict[token][name] = obj


# получение объекта из токена
def token_get(token: str, name: str):
    return _token_dict[token][name]


# изменение в списке токена
def token_changes(token: str, change: str, remove: bool = False):
    if remove and (change in _token_dict[token]['_changes']):
        _token_dict[token]['_changes'].remove(change)
    elif not remove:
        _token_dict[token]['_changes'].append(change)


# удаление токена
def token_del(token: str):
    if token_exists(token):

        _changes = _token_dict[token]['_changes']
        gcdb_data = _token_dict[token]['gcdb_data']
        if _changes:
            switch = _token_dict[token]['switch']
            if 'set_port_down' in _changes:
                switch.set_port(gcdb_data.switch_port, True)
                print('PORT RAISED')
            if 'set_bind_loose' in _changes:
                switch.set_bind(gcdb_data.switch_port, loose=False)
                print('return strict')

        try:
            tolerance = _token_dict[token]['tolerance']
            tolerance.close()
            telnet = _token_dict[token]['telnet']
            telnet.close()
        except Exception as ex:
            print(f'ошибка закрытия сессии {token}: \n{ex}')

        del _token_dict[token]


# копирование данных словаря токенов
def token_dict_image_get() -> dict:
    return _token_dict


#


# функция ожидания очереди токена, и её занятия
def token_wait_busy(token: str, func_name: str):
    _token_dict[token]['_busy_query'].append(func_name)
    while _token_dict[token]['_busy_query'][0] != func_name:
        time.sleep(0.1)


# освобождение очереди токена
def token_set_free(token):
    _token_dict[token]['_busy_query'].pop(0)


# декоратор для синхронной работы с токеном
def use_token(func):
    @wraps(func)
    def wrapper(token):
        if not token_exists(token):  # если токена не существует
            return jsonify({'error': True, 'type': 'TokenNotFound'})

        token_wait_busy(token, func.__name__)  # ждёт очередь, и занимает
        print(token, func.__name__)
        try:
            func_answer = func(
                token,  # извлекает данные по токену, передаёт в функцию
                gcdb_data=token_get(token, 'gcdb_data'),
                tolerance=token_get(token, 'tolerance'),
                telnet=token_get(token, 'telnet'),
                switch=token_get(token, 'switch'))
            token_set_free(token)  # освобождает очередь
        except Exception as e:
            func_answer = {'error': True, 'type': f'PythonError: {e}'}
        return jsonify(func_answer)  # возвращает ответ функции в формате json

    return wrapper


#


# обновление времени последней активности токена
@app.route("/still_active/<token>")
def token_still_active(token):
    if token_exists(token):
        print(token, 'activity')
        token_set(token, '_last_active', int(time.time()))
    return {'ok': token_exists(token)}


# раз в минуту проверяет активность токенов, удерживает telnet
def token_watch_activity():
    print(' # Token watcher started\n')

    while True:
        current_time = int(time.time())
        tokens_to_del = []
        print('- '*30)
        try:
            for token, t_data in _token_dict.items():
                time_range = current_time - t_data['_last_active']
                print('', f'token: {token}', f'time range: {time_range}',
                      f'user: {t_data["gcdb_data"].username}', sep='   ', end='   ')

                # если активность старше 5ти минут
                if time_range > 100:
                    tokens_to_del.append(token)
                    print('удаляю')

                # если токен занят
                elif t_data['_busy_query']:
                    print('занят')

                else:  # если активность не устарела
                    # не даёт закрыться сессию telnet
                    token_wait_busy(token, 'watcher')
                    t_data['telnet'].push('\n', read=True)
                    token_set_free(token)
                    print('держу')

            # удаление просроченных токенов
            for token in tokens_to_del:
                token_del(token)

            print('- ' * 30)
            gc.collect()
            time.sleep(60)

        except Exception as ex:
            print(f'\n   ! Ошибка потока слежки за токенами \n   ! {ex}')


token_thread = threading.Thread(target=token_watch_activity)
