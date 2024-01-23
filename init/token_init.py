from __future__ import annotations
import gc
import threading
import time
from functools import wraps
from random import randint
from flask import jsonify
from .app_init import app, logging


class Token:
    """Класс для работы с токенами, хранит в себе словарь токенов
    в словаре токенов ключ - номер токена, значение - объект токена"""

    _dict = {}  # инициализация словаря токенов
    changes_list = []  # лог-список выключения/включения портов

    # создание объекта токена, добавление его в словарь
    def __init__(self):
        while True:  # пока токен не будет уникальным
            token = str(randint(a=10000, b=99999))
            if token not in Token._dict:
                break

        self.number = token
        self._busy_query = []
        self._last_active = int(time.time())
        self.changes = []
        self.first_time_flag = True
        self.default_bind_state = 'loose'
        self.abon_ping_dict = {}

        self.gcdb_data = None
        self.telnet = None
        self.switch = None

        Token._dict[token] = self
        logging.info(f'{token} token created')

    def __str__(self):
        return self.number

    # по номеру токена вернёт объект
    @staticmethod
    def pull(token: str) -> Token:
        return Token._dict.get(token)

    # работа со списком изменений
    def change(self, name: str, add: bool):
        if add:
            return self.changes.append(name)
        self.changes.remove(name)

    # ожидание очереди токена, и её занятия
    def wait_busy(self, func_name: str):
        func_name += '_' + str(time.time())
        self._busy_query.append(func_name)
        while self._busy_query[0] != func_name:
            time.sleep(0.1)

    # освобождение очереди токена
    def set_free(self):
        self._busy_query.pop(0)

    # удаление токена
    def delete(self):
        if self.changes:
            if 'set_port_down' in self.changes:
                self.switch.set_port(self.gcdb_data.switch_port, True)
                logging.warning(f'token {self.number} enabled port {self.switch.ip}')
            if 'set_bind_loose' in self.changes:
                self.switch.set_bind(self.gcdb_data.switch_port, loose=False)
                logging.warning(f'token {self.number} set strict on {self.switch.ip}')
        try:
            self.telnet.close()
        except Exception as ex:
            logging.error(f'can\'t close telnet connection {self.number}: \n{ex}')

        del Token._dict[self.number]


# декоратор для синхронной работы с токеном
def use_token(func):
    @wraps(func)
    def wrapper(token):
        _token = Token.pull(token)
        if not _token:  # если токена не существует
            return jsonify({'error': True, 'type': 'Token Not Found'})

        _token.wait_busy(func.__name__)  # ждёт очередь, и занимает
        try:
            func_answer = func(_token)
        except Exception as e:
            print(e)
            func_answer = {'error': True, 'type': f'PythonError: {e}'}

        _token.set_free()  # освобождает очередь
        # print(func_answer)
        return jsonify(func_answer)  # возвращает ответ функции в формате json

    return wrapper


# обновление времени последней активности токена
@app.route("/still_active/<token>")
def token_still_active(token):
    token = Token.pull(token)
    if not token:
        return {'ok': False}

    # logging.info(f'{token} activity')
    token._last_active = int(time.time())
    return {'ok': True}


# раз в минуту проверяет активность токенов, удерживает telnet
def token_watch_activity():
    logging.critical('Token watcher started')

    while True:
        time.sleep(60)
        current_time = int(time.time())
        tokens_to_del = []
        log_string = ''

        try:
            for token_number, token in Token._dict.items():
                time_range = current_time - token._last_active

                log_string += (
                    f'\ntoken: {token}  '
                    f'user: {token.gcdb_data.username:<12}'
                    f'time: {"%02d:%02d" % ((time_range // 60), (time_range % 60))}  ')

                # если активность старше 3ёх минут
                if time_range > 180:
                    tokens_to_del.append(token)
                    log_string += ' del'

                # если токен занят
                elif token._busy_query:
                    log_string += 'busy'

                else:  # не даёт закрыться сессии telnet
                    token.wait_busy('watcher')
                    token.telnet.push('\n', read=True)
                    token.set_free()
                    log_string += 'hold'

            if log_string:
                logging.info(log_string)

            # удаление просроченных токенов
            for token in tokens_to_del:
                token.delete()

            # сборка мусора
            gc.collect()

        except Exception as ex:
            logging.critical(f'error while token dict checking:\n{ex}')


token_thread = threading.Thread(target=token_watch_activity)