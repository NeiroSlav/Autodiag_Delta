import time
import json
from pprint import pprint
from datetime import datetime, timedelta
import re
from .switches.utils.timing import plural_days

from paramiko import SSHClient, AutoAddPolicy


class Ubiquiti:
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
            client.connect(self.ip, username='ubnt', password='HflfH')
        except:
            return False
        self.channel = client.invoke_shell()
        time.sleep(0.5)
        self.channel.recv(1000)
        return True

    def close(self):
        self.channel.close()

    # выполняет команду на ubiquiti, возвращает ответ
    def _exec_command(self, command: str) -> str:
        self.channel.send(command.encode())
        self.channel.recv(1000)
        time.sleep(0.2)
        return self.channel.recv(10000).decode('ascii')

    # возвращает готовые данные о wi-fi линке со стороны базы
    def get_wifi_info(self, st_ip: str) -> dict:
        try:  # пробует получить данные по станции
            station_info = self._find_base_wifi_info(st_ip)
        except json.decoder.JSONDecodeError:  # ловит ошибку с _find_base_wifi_info
            return {'error': True, 'info': 'ошибка обработки ответа базы'}

        if not station_info:  # если по этой станции нет информации
            return {'error': True, 'info': 'станция не подключена'}
        return self._map_base_wifi_info(station_info)

    # возвращает данные об fe линке со стороны базы
    def get_local_link(self) -> dict:
        result = {
            'lan_speed': self._get_lan_speed(),
            'interfaces': {
                'eth0': self._get_eth_link('eth0'),
                'eth1': self._get_eth_link('eth1'),
                'wifi': self._get_eth_link('wifi0'),
            }
        }
        return result

    # возвращает данные о маках устройств за станцией
    def get_local_mac(self, macs) -> dict:
        if not macs:
            macs = []

        answer = self._exec_command('brctl showmacs br0\n')
        answer = answer.replace('\t', ' ')
        mac_list = re.findall(r'1 [a-z0-9:]+ +no +[0-9]', answer)
        mac_list = list(map(lambda x: x.split()[1], mac_list))

        result = {}
        for mac in mac_list:
            result[mac] = (mac in macs)

        return result

    # ищет во всей информации данные из wstalist
    def _find_base_wifi_info(self, st_ip: str) -> json:
        answer = self._exec_command('wstalist\n')
        # находит начало и конец json-строки
        start = answer.find('[')
        finish = answer[::-1].find(']')
        raw_json = answer[start:-finish]
        all_info = json.loads(raw_json)

        for st_info in all_info:
            if st_info['lastip'] == st_ip:
                remote = st_info.get('remote')
                if not remote:
                    remote = {'hostname': 'нет данных', 'noisefloor': 0, 'signal': 0, 'uptime': 0}
                return remote | {'stats': st_info['stats']}

    # структурирует сырые данные в нужный вид
    @staticmethod
    def _map_base_wifi_info(st_info: json) -> dict:
        result = {
            'error': False,
            'pkt_rx': st_info['stats']['rx_pps'],
            'pkt_tx': st_info['stats']['tx_pps'],
            'hostname': st_info['hostname'],
            'noise': st_info['noisefloor'],
            'signal': st_info['signal'],
            'uptime': str,
            'ok': bool,
        }
        # если сигнал выше -80, и выше уровня шума минимум на 10 единиц, то всё ок
        result['ok'] = result['signal'] > -80 and result['signal']-result['noise'] > 10

        # приведение uptime к читаемому виду
        uptime_sec = timedelta(seconds=st_info['uptime'])
        t = datetime(1, 1, 1) + uptime_sec
        day_word = plural_days(t.day-1)
        result['uptime'] = "%d %s %02d:%02d:%02d" % (t.day-1, day_word, t.hour, t.minute, t.second)

        return result

    # ищет на станции данные о скорости лан-сети
    def _get_lan_speed(self) -> str:
        answer = self._exec_command('mca-status\n')
        answer = re.findall(r'lanSpeed=[0-9A-Za-z-]+', answer)
        try:
            return answer[0].split('=')[-1].replace('bps', '')
        except IndexError:
            return ''

    # ищет на станции данные о линке ethernet
    def _get_eth_link(self, interface: str) -> dict:
        answer = self._exec_command(f'ip addr show {interface}\nifconfig {interface}\n')
        # print(answer)
        try:
            _link = 'up' if re.search('state UP', answer) else 'down'
            _bytes = re.findall(r'X bytes:[0-9]+ [(][0-9A-Za-z. ]+[)]', answer)
            _rx, _tx = map(lambda x: x.split('(')[-1].strip(')'), _bytes)
        except ValueError:
            return {}
        result = {
            'link': _link,
            'rx_all': _rx,
            'tx_all': _tx,
        }
        return result


if __name__ == '__main__':
    base_ip = '172.16.3.198'
    station_ip = '172.16.3.205'

    # base_ip = '172.16.2.218'
    # station_ip = '172.16.2.217'

    ubqBase = Ubiquiti(base_ip)
    ubqStation = Ubiquiti(station_ip)
    print('Инициализировано\n\n')

    if ubqBase.connected:
        print('\nИНФОРМАЦИЯ О ПОДКЛЮЧЕНИИ С БАЗЫ')
        pprint(ubqBase.get_wifi_info(station_ip))
    else:
        print('ошибка подключения к базе')

    if ubqStation.connected:
        print('\nИНФОРМАЦИЯ О СЕТИ НА СТАНЦИИ')
        pprint(ubqStation.get_local_link())
        pprint(ubqStation.get_local_mac([]))
    else:
        print('ошибка подключения к станции')
