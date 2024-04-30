from connections.switches.utils.mixin import SwitchMixin
from connections.telnet import Telnet


class Zyxel(SwitchMixin):
    """Класс для работы со свитчами Zyxel \n
    проверки:\n port, enabled, mac, cable, log
    действия:\n set_port"""

    def __init__(self, session: Telnet):
        self.session = session
        self.model = session.switch_model
        self.ip = session.switch_ip
        self.session.read()
        self.test_methods = [  # методы для тестов
            self.port, self.mac,
            self.cable, self.log]

    # диагностика порта, ошибок, и аптайма
    def port(self, port: int) -> dict:
        result = {'port': 'Down', 'uptime': '0:00:00', 'errors': '0',
                  'ok': True, 'error': False}
        self.session.read(timeout=0)
        self.session.push('q\n\n\n', read=True)
        self.session.push(f'\nsh int {port}')
        self.session.push('q\n\n\n')

        answer = self.session.read(timeout=2, string=':0')
        answer = answer.replace('\\t', ' ')

        if not (':0' in answer):
            return {'error': True}

        port_patterns = [  # список для поиска в ответе и статусы
            [r'100+M/F', True],
            [r'[0-9]+M/[a-zA-Z]', False],
            [r'Down', False]]

        # поиск аптайма
        if self._find(r'Up Time[ ]+[:0-9]+', answer):
            uptime = self._finded.split()[-1].strip(':')
            result['uptime'] = uptime

        # поиск ошибок
        if self._find(r'Errors[ ]+:[0-9]+', answer):
            port_errors = self._finded.split(':')[-1]
            if int(port_errors):
                result['ok'] = False
            result['errors'] = port_errors

        for elem in port_patterns:  # перебор списка с поиском в ответе
            if self._find(elem[0], answer):
                result['port'] = self._finded
                result['ok'] = bool(result['ok'] and elem[1])
                return result

    # включен ли порт
    def enabled(self, port: int) -> dict:
        result = {'enabled': 'Disabled', 'ok': False, 'error': False}
        self.session.read(timeout=0)
        self.session.push(f'\nsh int config {port}')

        # ждёт ответ свитча
        answer = self.session.read(timeout=2, string='Active')
        answer = answer.replace("'b'", '').replace('\\t', '')

        if not ('Active' in answer):
            return {'error': True}

        if self._find('Active +:Yes', answer):
            result['enabled'] = 'Enabled'
            result['ok'] = True

        return result

    # поиск мака
    def mac(self, port: int, macs: list) -> dict:
        result = {'mac': {}, 'ok': False, 'error': False}
        self.session.read(timeout=0)
        self.session.push(f'\nsh mac address-table port {port}')

        # ждёт ответ свитча
        answer = self.session.read(timeout=2, string='ype')

        if not ('ype' in answer):
            return {'error': True}

        # перебор списка маков
        mac_list = self._findall(self._mac_pattern, answer)
        for mac in mac_list:
            mac = self._fix_mac(mac)
            result['mac'][mac] = (mac in macs)
            result['ok'] = True

        return result

    # диагностика кабеля
    def cable(self, port: int) -> dict:
        result = {'cable': [], 'ok': True, 'error': False}
        self.session.read(timeout=0)
        self.session.push(f'\ncable-diagnostics {port}')
        answer = self.session.read(timeout=2, string='pairB')
        answer = answer.replace('\\r', ' ').replace("'b'", '')

        if not ('pair' in answer):
            return {'ok': False, 'error': False}

        # поиск пар А, B, C, D
        for pair in [r'pairA:', r'pairB:', r'pairC', r'pairD']:
            if self._find(pair+' [A-Za-z]+', answer):
                result['cable'].append(self._finded)
        try:  # попытка сравнить пары A и B
            a_stat = result['cable'][0].split(':')[-1]
            b_stat = result['cable'][1].split(':')[-1]
            result['ok'] = (a_stat == b_stat)
            return result

        except IndexError:
            return {'error': True}

    # парсинг лога
    def log(self, port: int = 0) -> dict:
        result = {'log': [], 'ok': True, 'error': False}
        self.session.read(timeout=0)
        self.session.push('\nsh logging')
        self.session.push('\n'*2)

        # ждёт ответ свитча
        answer = self.session.read(timeout=2, string='Clear')
        self.session.push('qq\n')

        # если просмотр лога не закрылся, ещё раз закрывает
        if '#' not in self.session.read(timeout=1, string='#'):
            self.session.push('qq\n')

        if not (':' in answer):
            return {'error': True}

        log_pattern = (  # паттерн записи лога с участием портов
            r'[0-9]+ [A-Za-z ]+ [0-9]+ +[0-9:]+ [A-Za-z0-9():, -=>]+ort [0-9] [A-Za-z0-9():, -=>]+')

        log = self._findall(log_pattern, answer)

        if port == 0:
            result['log'] = log
            return result

        for elem in log:
            if f'ort {port} ' in elem:
                result['log'].append(elem)

        result['ok'] = (len(result['log']) > 20)
        return result

    # вкл/выкл порт
    def set_port(self, port: int, enable: bool):
        self.session.push('\nconfig', read=True)
        self.session.push(f'\ninterface port-channel {port}', read=True)

        if enable:
            self.session.push('\nno inactive', read=True)
        else:
            self.session.push('\ninactive', read=True)

        self.session.push('\nexit', read=True)
        self.session.push('\nexit', read=True, timeout=0.3)

    # базовая быстрая проверка
    def fast_check(self, port_data: dict) -> dict:
        port = port_data['port']

        return {
            'port': self.port(port),
            'mac': self.mac(port, []),
            'cable': self.cable(port)
        }
