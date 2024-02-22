import time
import json
from pprint import pprint
from datetime import datetime, timedelta

from paramiko import SSHClient, AutoAddPolicy


class Ubiquiti:
    """Класс для работы с базой Ubiquiti \n
    единственный метод get_station_info """

    def __init__(self, base_ip: str):
        self.base_ip = base_ip
        self.channel = None
        self.connected: bool = self._connect()

    # подключается к базе
    def _connect(self) -> bool:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            client.connect(self.base_ip, username='ubnt', password='HflfH')
        except:
            return False
        self.channel = client.invoke_shell()
        time.sleep(0.1)
        self.channel.recv(1000)
        return True

    # забирает с базы данные о всех станциях, парсит json
    def _get_all_info(self) -> json:
        self.channel.send(b'wstalist\n')
        self.channel.recv(1000)
        time.sleep(0.2)
        answer = self.channel.recv(10000).decode('ascii')

        # находит начало и конец json-строки
        start = answer.find('[')
        finish = answer[::-1].find(']')
        raw_json = answer[start:-finish]
        return json.loads(raw_json)

    # ищет во всей информации данные о станции
    def _find_station_info(self, st_ip: str) -> json:
        all_info = self._get_all_info()
        for st_info in all_info:
            if st_info['lastip'] == station_ip:
                return st_info['remote'] | {'stats': st_info['stats']}

    # структурирует сырые данные в нужный вид
    @staticmethod
    def _map_station_info(st_info):
        result = {
            'error': False,
            'hostname': st_info['hostname'],
            'noise': st_info['noisefloor'],
            'signal': st_info['signal'],
            'uptime': str,
            'ok': bool,
            'pkt_rx': st_info['stats']['rx_pps'],
            'pkt_tx': st_info['stats']['tx_pps'],
        }
        result['ok'] = result['noise'] < result['signal']

        uptime_sec = timedelta(seconds=st_info['uptime'])
        t = datetime(1, 1, 1) + uptime_sec
        uptime = "%d дней %d:%d:%d" % (t.day-1, t.hour, t.minute, t.second)
        result['uptime'] = uptime

        return result

    # возвращает готовые данные о станции
    def get_station_info(self, st_ip) -> dict:
        try:  # пробует получить данные по станции
            station_info = self._find_station_info(st_ip)
        except json.decoder.JSONDecodeError:  # ловит ошибку с _get_all_info
            return {'error': True, 'info': 'не получен ответ от базы'}

        if not station_info:  # если по этой станции нет информации
            return {'error': True, 'info': 'станция не найдена'}
        return self._map_station_info(station_info)


if __name__ == '__main__':
    base_ip = '172.16.3.198'
    station_ip = '172.16.3.205'

    ubq = Ubiquiti(base_ip)
    if ubq.connected:
        pprint(ubq.get_station_info(station_ip))
    else:
        print('ошибка подключения')
