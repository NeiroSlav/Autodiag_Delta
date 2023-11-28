from connections.switches.utils.mixin import SwitchMixin
from connections.telnet import Telnet


class Foxgate(SwitchMixin):
    """Класс для работы со свитчами Foxgate \n
    проверки: port, mac
    действия: set_port"""

    def __init__(self, session: Telnet):
        self.session = session
        self.session.read()
        self.test_methods = [  # методы для тестов
            self.port, self.mac]

    # диагностика порта и аптайма
    def port(self, port: int) -> dict:
        result = {'port': '', 'uptime': '00:00',
                  'ok': True, 'error': False}
        self.session.push(f'sh int eth 0/0/{port}\n')
        answer = self.session.read(string='Output', timeout=2)

        port_patterns = [  # список для поиска в ответе и статусы
            [r'[0-9]+M, Duplex mode is [a-z]+', True],
            [r'link is down', False]]

        for elem in port_patterns:  # перебор списка с поиском в ответе
            if self._find(elem[0], answer):
                port = self._finded.split()
                result['port'] = f'{port[0]} {port[-1]}'
                result['ok'] = bool(result['ok'] and elem[1])
                break
        else:
            return {'error': True}

        # проверка, включен ли порт
        if self._find(f'state: disabled', answer):
            result['port'] = 'down'
            result['enabled'] = 'Disabled'
            result['ok'] = False
            return result
        result['enabled'] = 'Enabled'

        if result['ok']:  # поиск аптайма, перевод из 22 minute 12 second в 22:12
            if self._find(r'linkup is [0-9a-z ]+second', answer):
                uptime = self._finded.split('is ')[-1].replace(' second', '')
                uptime = uptime.replace(' hour ', ':').replace(' minute ', ':')
                if len(uptime) == 2:
                    uptime = '00:' + uptime
                result['uptime'] = uptime.strip()

        return result

    # поиск мака
    def mac(self, port: int, macs: list = []) -> dict:
        result = {'mac': {}, 'ok': True, 'error': False}
        self.session.read()
        self.session.push(f'sh mac-address-table interface ethernet 0/0/{port}\n')
        answer = self.session.read(timeout=1, string='#')

        if self._findall(self._mac_pattern, answer):
            mac_list = self._finded  # перебор списка маков
            for i, mac in enumerate(mac_list):
                mac_list[i] = self._fix_mac(mac)
                result['mac'][mac] = (mac in macs)
            return result

        # если таблица маков пустая
        elif 'does not exist' in answer:
            result['ok'] = False
            return result

        return {'error': True}

    # вкл/выкл порт
    def set_port(self, port: int, enable: bool):
        self.session.push('conf\n')
        self.session.push(f'int ethernet 0/0/{port}\n')

        if enable:
            self.session.push('no shutdown\n')
        else:
            self.session.push('shutdown\n')

        self.session.push('exit\nexit\n', read=True)

    def __del__(self):
        print('foxgate object deleted')
