from connections.switches.utils.mixin import SwitchMixin
from connections.telnet import Telnet


class Zyxel(SwitchMixin):
    """Класс для работы со свитчами Zyxel \n
    проверки:\n port, mac, cable, log
    действия:\n set_port"""

    def __init__(self, session: Telnet):
        self.session = session
        self.session.read()
        self.test_methods = [  # методы для тестов
            self.port, self.mac,
            self.cable, self.log]

    # диагностика порта, ошибок, и аптайма
    def port(self, port: int) -> dict:
        result = {'enabled': 'Enabled', 'port': 'Down', 'uptime': '0:00:00', 'errors': '0',
                  'ok': True, 'error': False}
        self.session.push(f'\nsh int {port}')
        self.session.push('q\n\n\n')

        answer = self.session.read(timeout=2, string='Port NO')
        answer = answer.replace('\\t', ' ')
        if not ('Port NO' in answer):
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

        # включен ли порт
        if not (':FORWARDING' in answer):
            result['enabled'] = 'Disabled'

        for elem in port_patterns:  # перебор списка с поиском в ответе
            if self._find(elem[0], answer):
                result['port'] = self._finded
                result['ok'] = bool(result['ok'] and elem[1])
                return result

    # поиск мака
    def mac(self, port: int) -> dict:
        result = {'mac': {}, 'ok': False, 'error': False}
        self.session.read()
        self.session.push(f'\nsh mac address-table port {port}')

        # ждёт ответ свитча
        answer = self.session.read(timeout=2, string='Type')
        if not ('Type' in answer):
            return {'error': True}

        # перебор списка маков
        mac_list = self._findall(self._mac_pattern, answer)
        for mac in mac_list:
            mac = self._fix_mac(mac)
            result['mac'][mac] = (mac == 'ТУТ БУДЕТ АБОНЕНТСКИЙ МАК')
            result['ok'] = True

        return result

    # диагностика кабеля
    def cable(self, port: int) -> dict:
        result = {'cable': [], 'ok': True, 'error': False}
        self.session.read()
        self.session.push(f'\ncable-diagnostics {port}')
        answer = self.session.read(timeout=2, string='pair')
        answer = answer.replace('\\r', ' ').replace("'b'", '')

        if 'unknown' in answer:
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
    def log(self, port: int) -> dict:
        result = {'log': [], 'ok': True, 'error': False}
        self.session.read()
        self.session.push('\nsh logging')
        self.session.push('\n'*3)

        # ждёт ответ свитча
        answer = self.session.read(timeout=2, string='Clear')
        answer += self.session.read()
        if not ('INFO' in answer):
            return {'error': True}

        log_pattern = (  # паттерн записи лога с участием портов
            r'[0-9]+ [A-Za-z ]+ [0-9]+ +[0-9:]+ [A-Za-z0-9():, -=>]+ort ' +
            str(port) +
            ' [A-Za-z0-9():, -=>]+')

        result['log'] = self._findall(log_pattern, answer)
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
