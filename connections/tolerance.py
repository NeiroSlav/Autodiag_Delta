import re
import paramiko
from .personal_data import tolerance_login, tolerance_password


class Tolerance:
    """Отвечает за SSH-сессию и связанную сессию Telnet;
       Хранит информацию о типе свитча"""

    hostname = 'tolerance.dec.net.ua'
    telnet_error = None

    def __init__(self):
        self.username = tolerance_login
        self.password = tolerance_password
        self._ssh_connect()

    # создание соединения ssh, объявление локальных атрибутов _client и _channel
    def _ssh_connect(self):
        self._client = paramiko.SSHClient()  # инициализация клиента
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # не спрашивать про ключ
        try:
            self._client.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                look_for_keys=False,  # не искать ключи,
                allow_agent=False)  # не ssh-агент windows
            self._channel = self._client.invoke_shell()  # запустить ssh в реальном режиме
            self.read()  # очистить кэш
            # print('Подключился к tolerance')

        except TimeoutError:
            print('ошибка подключения по ssh')

    # отправка команды через канал
    def push(self, command: str, read: bool = False, timeout: float = 0.1) -> str:
        self._channel.send(f'{command}\n')
        if read:
            return self.read(timeout)

    # @timing  # чтение данных из канала
    def read(self, timeout: float = 0.1) -> str:
        answer = ''
        self._channel.settimeout(timeout)
        try:
            while True:
                answer += str(self._channel.recv(1000))
        except TimeoutError:
            answer = answer.replace('\\r', '')
            answer = answer.replace('\\n', '\n')
            return answer.replace("'b'", '')

    # чтение, пока не появится запись, если не появилась - ''
    def wait(self, string: str, timeout: float = 1) -> str:
        result = ''
        for i in range(int(timeout*10)):
            result += self.read()
            if string in result:
                return result.replace('\\t', ' ')

        return ''  # если не дождался - вернёт пустую строку

    # поиск порта удалёнки, возвращает словарь с ип и портом
    def find_open_port(self, router_ip: str) -> dir:
        answer = ''
        self.push(f'ch {router_ip} \n')
        while not re.search('scanned', answer):
            answer += self.read()

        port = re.search(r'[0-9]+/tcp +open', answer)  # ищет открытый порт
        if not port:  # если порт не найден
            return {'ip': router_ip, 'port': None}

        port = port.group(0).split('/')[0]
        return {'ip': router_ip, 'port': port}

    #
    def ping(self, ip_address: str, num: int = 3) -> dict:
        command = f'ping -i .2 -s 1000 -c {num} {ip_address}'
        answer = self.push(command, read=True, timeout=0.3)
        if 'statistics' in answer:
            return {'ok': True}

    def close(self):
        self._client.close()

    def __del__(self):
        print('tolerance object deleted')
