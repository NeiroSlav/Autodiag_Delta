from pprint import pprint

from paramiko import SSHClient, AutoAddPolicy
import time
import re


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
        time.sleep(1)
        self.channel.recv(10000)
        return True

    # отправляет запрос на поиск мака в логах
    def start_mac_search(self, mac: str):
        self.channel.send(f'm {mac} | tail -1\n'.encode())
        self.channel.recv(1000)

    # если записи есть, берёт последнюю
    def get_answer(self) -> str:
        answer = self.channel.recv(100000).decode('ascii')
        return answer


class DhcpUnity:
    def __init__(self):
        self.syava = DhcpServer('syava.dec.net.ua')
        self.siplyj = DhcpServer('siplyj.dec.net.ua')
        self.smash = DhcpServer('smash.dec.net.ua')

    # проверка самой поздней записи о маке на серверах
    def check_wrong_flat(self, mac: str) -> str | None:
        for server in (self.syava, self.smash, self.siplyj):
            server.start_mac_search(mac)
        time.sleep(0.3)
        last_signs = []
        for server in (self.syava, self.smash, self.siplyj):
            last_server_sign = server.get_answer()
            if last_server_sign:
                last_signs.append(last_server_sign)

        try:  # сортирует записи серверов по времени, выбирает самую позднюю
            last_signs = sorted(last_signs, key=lambda x: self.get_sign_t(x))
            latest_sign = last_signs[-1]
        except IndexError:
            return

        if 'Not equal port' in latest_sign:
            return 'Указан неправильный порт'
        elif 'Not equal switch' in latest_sign:
            return 'Указан неправильный свитч'
        elif 'Not equal PON' in latest_sign:
            return 'Указан неправильный PON'
        elif 'Not equal' in latest_sign:
            return 'Последний флат с ошибкой'

    # сжимает время из записи (04:15:13.141 -> 041513141)
    @staticmethod
    def get_sign_t(sign: str) -> int:
        t = re.search(r'\d\d:\d\d:\d\d\.\d\d\d', sign)
        if not t:  # если в записи не было времени
            return 0

        time_info = t.group().replace(':', '')
        time_info = time_info.replace('.', '')
        return int(time_info)


if __name__ == '__main__':

    dhcp_unity = DhcpUnity()
    while True:
        mac = input()
        wrong_flat = dhcp_unity.check_wrong_flat(mac)
        print(wrong_flat if wrong_flat else 'ok')

