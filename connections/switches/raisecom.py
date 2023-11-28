from connections.switches.utils.mixin import SwitchMixin
from connections.telnet import Telnet


class Raisecom(SwitchMixin):
    """Класс для работы со свитчами Raisecom \n
    проверки:\n port, mac, errors
    действия:\n set_port"""

    def __init__(self, session: Telnet):
        self.session = session
        self.session.read(0.3)
        self.test_methods = [  # методы для тестов
            self.port,
            self.mac,
            self.errors]

    # диагностика порта, ошибок и аптайма
    def port(self, port: int) -> dict:
        result = {'port': '', 'uptime': '00 days 00:00:00',
                  'enabled': True, 'ok': True, 'error': False}
        self.session.push(f'\nsh interface port {port}')
        answer = self.session.read(timeout=2, string='Forward')

        if not ('Forward' in answer):
            return {'error': True}

        port_patterns = [  # список для поиска в ответе и статусы
            [r'up\([0-9]+M/[a-z]+\)', True],
            [r'down', False]]

        # is port enable check
        if self._find(f'[0-9] +disable', answer):
            result['port'] = 'down'
            result['enabled'] = 'Disabled'
            result['ok'] = False
            return result
        result['enabled'] = 'Enabled'

        # поиск аптайма
        if self._find(r'[0-9]+d[0-9]+h[0-9]+m[0-9]+', answer):
            uptime = self._finded.replace('h', ':')
            uptime = uptime.replace('m', ':')
            uptime = uptime.replace('d', ' days ')
            result['uptime'] = uptime

        # перебор списка паттернов
        for pattern in port_patterns:
            if self._find(pattern[0], answer):
                result['port'] = self._finded
                result['ok'] = (pattern[1])
                return result

    # поиск мака
    def mac(self, port: int, macs: list = []) -> dict:
        result = {'mac': {}, 'ok': True, 'error': False}
        self.session.push(f'\nsh mac-address-table l2-address port {port}')
        answer = self.session.read(timeout=2, string='-----')
        answer += self.session.read(timeout=0.3, string='#')

        if not ('-----' in answer):
            return {'error': True}

        # если не нашёл маков
        if not self._findall(self._mac_pattern_old, answer):
            result['ok'] = False

        # перебор списка маков
        for mac in self._finded:
            mac = self._fix_mac(mac)
            result['mac'][mac] = (mac in macs)

        return result

    # поиск ошибок
    def errors(self, port: int) -> dict:
        result = {'errors': {}, 'ok': True, 'error': False}
        self.session.push(f'\nshow interface port {port} statistics')
        answer = self.session.read(timeout=2, string='Statistics')
        if not ('Statistics' in answer):
            return {'error': True}

        err_patterns = {'crc': r'CRCAlignErrors\(Pkts\):[ ]+[0-9]+',
                        'fragment': r'Fragments\(Pkts\):[ ]+[0-9]+',
                        'jabber': r'Jabbers\(Pkts\):[ ]+[0-9]+',
                        'drop': r'DropEvents\(Pkts\):[ ]+[0-9]+'}

        for key, pattern in err_patterns.items():
            if self._find(pattern, answer):
                result['errors'][key] = self._finded.split()[-1]
                if int(result['errors'][key]):
                    result['ok'] = False

        return result

    # включение/выключение порта
    def set_port(self, port: int, enable: bool):
        self.session.push('\nconfig')
        self.session.push(f'\ninterface port {port}')

        if enable:
            self.session.push('\nno shu')
        else:
            self.session.push('\nshu')

        self.session.push('\nexit'*2, read=True)

    def __del__(self):
        print('raisecom object deleted')
