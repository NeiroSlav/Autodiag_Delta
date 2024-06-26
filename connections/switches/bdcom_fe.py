import time

from connections.switches.utils.mixin import SwitchMixin
from connections.telnet import Telnet


class BdcomFE(SwitchMixin):
    """Класс для работы с Bdcom на Fast Ethernet \n
    проверки:
    port, mac"""

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
        time.sleep(0.5)
        result = {'port': 'Down', 'errors': '0',
                  'ok': True, 'error': False}

        commands = [f'\n  sh int fastEthernet 0/{port}\n',
                    f'\n  sh int gigaEthernet 0/{port}\n']

        # пробует разные команды для проверки порта
        for command in commands:
            self.session.read()
            self.session.push(command)
            answer = self.session.read(timeout=5, string='Received')
            if 'invalid' not in answer and 'nknown' not in answer:
                break
        else:  # если ни одна команда не сработала
            return {'error': True}

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
        time.sleep(0.5)
        result = {'mac': {}, 'ok': False, 'error': False}
        commands = [f'\n sh mac address-table interface f0/{port}',
                    f'\n sh mac address-table interface gigaEthernet 0/{port}']

        # пробует разные команды для поиска мака
        for command in commands:
            self.session.read()
            self.session.push(command)
            answer = self.session.read(timeout=5, string='#')
            if 'invalid' not in answer and 'nknown' not in answer:
                break
        else:  # если ни одна команда не сработала
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

    # базовая быстрая проверка
    def fast_check(self, port_data: dict) -> dict:
        port = port_data['port']

        return {
            'port': self.port(port),
            'mac': self.mac(port, []),
        }
