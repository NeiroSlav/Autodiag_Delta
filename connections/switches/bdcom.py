import time

from connections.switches.utils.mixin import SwitchMixin
from connections.telnet import Telnet


class Bdcom(SwitchMixin):
    """Класс для работы с Bdcom ePON \n
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
            self.port, self.mac,
            self.signal, self.active]

    # диагностика порта, ошибок, и аптайма
    def port(self, port: int, pon: int) -> dict:
        result = {'port': 'Down',
                  'ok': True, 'error': False}

        command = f'\nsh interface epon 0/{port}:{pon}'
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

        return result

    # поиск мака
    def mac(self, port: int, pon: int, macs: list) -> dict:
        result = {'mac': {}, 'ok': False, 'error': False}
        command = f'show mac address-table interface ePON 0/{port}:{pon}\n'

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

    # проверка сигнала
    def signal(self, port: int, pon: int) -> dict:
        result = {'signal': '', 'ok': False, 'error': False}
        command = (f'show epon interface epon 0/{port}:{pon} ' +
                   'onu ctc optical-transceive\n\n')

        self.session.read()
        self.session.push(command)
        answer = self.session.read(timeout=1, string='DBm')

        # если не нашёл ответ
        if not ('#' in answer):
            return {'error': True}

        # проверка качества сигнала
        if not self._find(r'received power\(DBm\): -[0-9.]+', answer):
            return {'error': False, 'ok': False, 'signal': '0'}

        signal = self._finded.split('-')
        result['signal'] = f'-{signal[-1]}'
        signal = float(signal[-1])
        result['ok'] = signal < 30
        return result

    # проверка неактивных ONU
    def active(self, port: int, pon: int) -> dict:
        result = {'ok': True, 'error': False}
        command = f'sh epon inactive-onu interface ePON 0/{port}\n'

        self.session.read()
        self.session.push(command)
        self.session.push('       ')
        answer = self.session.read(timeout=5, string='#')

        if not ('----' in answer):
            return {'error': True}

        if self._find(r'EPON0/' + f'{port}:{pon} ', answer):
            result['ok'] = False

        return result

    # базовая быстрая проверка
    def fast_check(self, port_data: dict) -> dict:
        port = port_data['port']
        pon = port_data['pon']

        return {
            'port': self.port(port, pon),
            'mac': self.mac(port, pon, []),
            'signal': self.signal(port, pon),
            'active': self.active(port, pon)
        }
