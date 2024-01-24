import time

from connections.switches.utils.mixin import SwitchMixin
from connections.telnet import Telnet


class BdcomFE(SwitchMixin):
    """Класс для работы с Bdcom на Fast Ethernet \n
    проверки:
    port, mac, signal, active"""

    def __init__(self, session: Telnet):
        self.session = session
        self.model = session.switch_model
        self.ip = session.switch_ip
        self.session.read()
        self.session.push('\nena')
        self.session.read(2, '#')
        self.test_methods = [  # методы для тестов
            self.port, self.mac]

    # диагностика порта, ошибок, и аптайма
    def port(self, port: int) -> dict:
        result = {'port': 'Down', 'errors': '0',
                  'ok': True, 'error': False}

        command = f'\nsh int fastEthernet 0/{port}'
        self.session.read()
        self.session.push(command)
        self.session.push('\nn')

        answer = self.session.read(timeout=2, string='Received')
        if not ('Received' in answer):
            return {'error': True}

        port_patterns = [  # список для поиска в ответе и статусы
            [r'is up,', True],
            [r'is down,', False]]

        for elem in port_patterns:  # перебор списка с поиском в ответе
            if self._find(elem[0], answer):
                result['port'] = self._finded.replace(',', '').replace('is', 'Link')
                result['ok'] = elem[1]

        # поиск ошибок
        if self._find(r'[0-9]+ error', answer):
            port_errors = self._finded.split(' ')[0]
            if int(port_errors):
                result['ok'] = False
            result['errors'] = port_errors

        return result

    # поиск мака
    def mac(self, port: int, macs: list) -> dict:
        result = {'mac': {}, 'ok': False, 'error': False}
        command = f'\nsh mac address-table interface f0/{port}'

        self.session.read()
        self.session.push(command)
        answer = self.session.read(timeout=0.5, string='#')

        # если ошибка при вводе команды
        if 'invalid' in answer:
            return {'error': True}

        # если таблица маков пустая
        if not self._findall(self._mac_pattern_old, answer):
            return {'ok': False, 'error': False}

        # перебор списка маков
        for mac in self._finded:
            mac = self._fix_mac(mac)
            result['mac'][mac] = (mac in macs)
            result['ok'] = True

        return result

    # def __del__(self):
    #     print('bdcom_fe object deleted')
