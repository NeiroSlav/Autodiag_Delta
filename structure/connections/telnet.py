import telnetlib
import re
import time

from .switches.utils.timing import timing


class Telnet:
    """Отвечает за сессию Telnet;
       Хранит информацию о типе свитча"""

    _channel = None
    switch_type = None

    def __init__(self, gcdb_data):
        self.switch_ip = gcdb_data.switch_ip
        self.username = gcdb_data.switch_login
        self.password = gcdb_data.switch_password
        self._connect(self.switch_ip)
        if not self.switch_type:
            print(f'{self.switch_ip} лежит')
            return

        print(f'Зашёл на {self.switch_type} {self.switch_ip}')

        if not timing(self._login_funk)():
            self.switch_type = None
            self.close()
            print(f'{self.switch_ip} завис')
            return

        print(f'Логин на {self.switch_type} {self.switch_ip}')

    # отправка команды через канал
    def push(self, command: str, read: bool = False, timeout: float = 0) -> str:
        command = f'{command}\n'.encode('ascii')
        self._channel.write(command)
        if read:
            return self.read(timeout)

    # чтение данных из канала
    def read(self, timeout: float = 0.1, string: str = '$#@&$') -> str | None:
        answer_full = ''
        answer = ' '
        # читает, пока не перестанут появляться новые ответы
        while str(answer):
            answer = self._channel.read_until(string.encode('ascii'), timeout)
            answer = str(answer).replace("b''", '').replace("'b'", '')
            answer_full += answer
            # если попалась искомая строка
            if string in answer_full:
                time.sleep(0.1)
                answer_full += str(self._channel.read_very_eager())
                return answer_full

        return answer_full

    # вход на свитч, и определения свитча
    @timing
    def _connect(self, switch_ip: str):
        try:
            self._channel = telnetlib.Telnet(switch_ip, timeout=5)
        except TimeoutError:
            return

        answer = ''
        # словарь фраз для определения свитча
        phrases = {
            'D-Link': ['dlink', self._dlink_login],
            'User name:': ['zyxel', self._zyxel_login],
            'Login:': ['raisecom', self._raisecom_login],
            'User Access Verification': ['bdcom', self._bdcom_login],
            'Username': ['foxgate', self._foxgate_login],
        }

        for i in range(100):  # 100 попыток с маленьким таймаутом
            answer += self.read(0.1, 'D-Link')
            for key, var in phrases.items():
                if re.search(key, str(answer)):  # поиск совпадения в словаре свитчей
                    self.switch_type = var[0]
                    self._login_funk = var[1]
                    return True

    def close(self):
        try:
            self._channel.close()
            print(f'Сессия telnet {self.switch_ip} закрыта')
        except Exception as ex:
            print(f'{ex} : ошибка закрытия telnet сессии с {self.switch_ip}')

    # методы логинов для свитчей

    def _dlink_login(self):
        self.push(self.username)
        self.push(self.password)
        self.push('admin')
        self.push('GfhfljrC')
        if not ('#' in self.read(2, '#')):
            return False
        return True

    def _zyxel_login(self):
        self.push('admin')
        self.push('Xf,fXjR9,8')
        self.push('GfhfljrC')
        if not ('#' in self.read(2, '#')):
            return False
        return True

    def _raisecom_login(self):
        self.push(self.username)
        self.push(self.password)
        if not ('#' in self.read(2, '#')):
            return False
        return True

    def _foxgate_login(self):
        self.push('admin')
        self.push('Xf,fXjR9,8')
        try:
            answer = self._channel.expect(
                ['#'.encode('ascii'),
                 '>'.encode('ascii')])
            if answer[0] == 1:
                self.push('ena')
                self.read(1, '#')
            return True
        except TimeoutError:
            return False

    def _bdcom_login(self):
        self.push('admin')
        self.push('GfhfljrC')
        self.push(self.username)
        self.push(self.password)
        if not ('-' in self.read(2, '-')):
            return False
        self.push('ena')
        return True
