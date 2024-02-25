from pprint import pprint

from paramiko import SSHClient, AutoAddPolicy
import time


class DhcpServer:
    """Класс для работы с базой и станцией Ubiquiti \n
    методы станции: get_local_link, get_local_mac
    методы базы: get_wifi_info"""

    def __init__(self, ip: str):
        self.ip = ip
        self.channel = None
        self.connected: bool = self._connect()

    # подключается к базе
    def _connect(self) -> bool:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            client.connect(self.ip, username='supp0rt', password='AskMeForIp')
        except:
            return False
        self.channel = client.invoke_shell()
        time.sleep(0.3)
        self.channel.recv(10000)
        return True

    # отправляет запрос на поиск мака в логах
    def start_mac_search(self, mac: str):
        self.channel.send(f'm {mac}\n'.encode())
        self.channel.recv(1000)

    # если записи есть, берёт последнюю
    def get_answer(self) -> str:
        answer = self.channel.recv(100000).decode('ascii')
        answer = answer.split('\r')
        if len(answer) > 3:
            return answer[-2]


class DhcpUnity:
    def __init__(self):
        self.syava = DhcpServer('syava.dec.net.ua')
        self.siplyj = DhcpServer('siplyj.dec.net.ua')
        self.smash = DhcpServer('smash.dec.net.ua')

    def check_wrong_flat(self, mac) -> str:
        for server in (self.syava, self.smash, self.siplyj):
            server.start_mac_search(mac)
        time.sleep(0.1)
        last_signs = []
        for server in (self.syava, self.smash, self.siplyj):
            last_sign = server.get_answer()
            if last_sign:
                last_signs.append(last_sign)

        try:
            last_signs = sorted(last_signs, key=lambda x: self.get_sign_t(x))
            latest_sign = last_signs[-1]
        except:
            return ''

        # ищет паттерны несовпадения свитча/порта в ответе
        for info in ('Not equal port', 'Not equal switch'):
            if info in latest_sign:
                return info
        return ''

    # сжимает время из записи (04:15:13.141 -> 041513141)
    @staticmethod
    def get_sign_t(sign: str) -> int:
        sign = sign.split(' ')[2].strip(',')
        sign = sign.replace(':', '')
        sign = sign.replace('.', '')
        return int(sign)


if __name__ == '__main__':

    dhcp_unity = DhcpUnity()
    while True:
        print('\n', dhcp_unity.check_wrong_flat('9c:a2:f4:37:67:33'))
        input()