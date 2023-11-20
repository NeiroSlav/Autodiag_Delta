from connections.switches.utils.mixin import SwitchMixin
from connections.telnet import Telnet


class Dlink(SwitchMixin):
    """Класс для работы со свитчами Dlink \n
    проверки:\n port, bind, mac, errors, cable, loose, log
    действия:\n set_port, set_bind, clear"""

    def __init__(self, session: Telnet):
        self.session = session
        self.session.read()
        self.test_methods = [  # методы для тестов
            self.port, self.errors,
            self.loose, self.mac, self.bind,
            self.cable, self.log]

    # диагностика порта
    def port(self, port: int) -> dict:
        result = {'enabled': 'Enabled', 'port': '', 'ok': True, 'error': False}
        self.session.read()
        self.session.push(f'\nshow ports {port} ')
        answer = self.session.read(string='Speed', timeout=1)
        self.session.push('q', read=True)

        if self._find(r'[0-9][ ]+Disabled[ ]+', answer):
            result['enabled'] = 'Disabled'
            result['ok'] = False

        port_patterns = [  # список для поиска в ответе и статусы
            [r'100M/Full/None', True],
            [r'[0-9]+M/\w\w\w\w/None', False],
            [r'LinkDown', False],
            [r'Link Down', False],
            [r'Err-Disabled', False]]

        for elem in port_patterns:  # перебор списка с поиском в ответе
            if self._find(elem[0], answer):
                result['port'] = self._finded
                result['ok'] = (result['enabled'] == 'Enabled') and elem[1]
                return result

        # print(answer)
        return {'error': True}

    # диагностика привязки
    def bind(self, port: int) -> dict:
        result = {'binding': {}, 'ok': True, 'error': False}
        self.session.read()
        self.session.push(f'\nshow address_binding dhcp_snoop binding_entry port {port}')
        answer = self.session.read(timeout=2, string='Entries')
        # print(str(answer))
        self.session.push('q', read=True)
        des_binding_patterns = [
            ['DES-3028',  # список паттернов для DES-3028
             r'Port[ ]+Status',
             r'[0-9.]+[ ]+[A-Za-z0-9- ]+ive',
             r'Active'],
            ['DES-3200',  # список паттернов для DES-3200
             r'A: Active',
             r'[0-9.]+[ ]+[A-Z0-9-]+ [A-Z]',
             r'\w\w A']]

        for elem in des_binding_patterns:
            if self._find(elem[1], answer):
                des_bind_all = elem[2]
                des_bind_pattern = elem[3]
                break
        else:  # вообще не найден ответ
            # print(answer)
            return {'error': True}

        raw_bindings = self._findall(des_bind_all, answer)
        if not raw_bindings:
            return {'ok': False, 'error': False}

        for elem in raw_bindings:  # перебор строк привязок
            mac = self._find(self._mac_pattern, elem)
            mac = self._fix_mac(mac)
            ip = self._find(self._ip_pattern, elem)
            status = bool(self._find(des_bind_pattern, elem))
            result['binding'][mac] = [ip, status]
            # print(elem, mac, result[mac], sep='\n')

        return result

    # поиск мака на порту
    def mac(self, port: int) -> dict:
        result = {'mac': {}, 'ok': True, 'error': False}
        self.session.read()
        self.session.push(f'\nshow fdb port {port}')
        answer = self.session.read(timeout=2, string='Entries')
        # print(answer)
        if not ('Entries' in answer):
            return {'error': True}

        mac_list = self._findall(self._mac_pattern, answer)
        if not mac_list:
            return {'ok': False, 'error': False}

        for mac in mac_list:
            mac = self._fix_mac(mac)
            result['mac'][mac] = (mac == 'ТУТ БУДЕТ АБОНЕНТСКИЙ МАК')
        return result

    # поиск ошибок
    def errors(self, port: int) -> dict:
        result = {'errors': {}, 'ok': True, 'error': False}
        self.session.read()
        self.session.push(f'\nshow error ports {port}')
        answer = self.session.read(string='RX Frames', timeout=1)
        self.session.push('\nq', read=True)

        if not ('RX Frames' in answer):
            return {'error': True}

        err_patterns = {'crc': r'CRC Error[ ]+[0-9-]+',
                        'fragment': r'Fragment[ ]+[0-9-]+',
                        'jabber': r'Jabber[ ]+[0-9-]+',
                        'drop': r'Drop Pkts[ ]+[0-9-]+'}

        for key, pattern in err_patterns.items():
            if self._find(pattern, answer):
                result['errors'][key] = self._finded.split()[-1]
                result['errors'][key] = result['errors'][key].replace('-', '0')
                if int(result['errors'][key]):
                    result['ok'] = False

        return result

    # диагностика кабеля
    def cable(self, port: int) -> dict:
        result = {'cable': [], 'ok': True, 'error': False}
        self.session.read()
        self.session.push(f'cable_diag ports {port}\n')
        answer = self.session.read(timeout=2, string='Result')
        self.session.push('q\n', read=True)

        if self._findall(r'Pair[A-Za-z0-9 ]+M', answer):
            pairs = self._finded
            try:
                pair1 = int(pairs[0].replace('M', '').split()[-1])
                pair2 = int(pairs[1].replace('M', '').split()[-1])
                # если разница в парах больше 5ти, или кабель длиннее 90м
                result['ok'] = (abs(pair1-pair2) < 5) and (pair1 < 90)
            except IndexError:
                result['ok'] = False
            result['cable'] = pairs
            return result

        other_cable_patterns = [
            [r'No Cable', False],
            [r'Shutdown', False],
            [r'Link Down', False],
            [r'Link Up', True]]

        if not result['cable']:
            for pattern in other_cable_patterns:
                if self._find(pattern[0], answer):
                    result['cable'] = [pattern[0]]
                    result['ok'] = pattern[1]
                    return result

        return {'error': True}

    # парсинг лога
    def log(self, port: int, hours: int = 24) -> dict:
        result = {'snmp': [], 'log': [],
                  'ok': True, 'error': False}
        self.session.read()
        self.session.push('\nenable clip', read=True)
        self.session.push('\nshow log')
        answer = self.session.read(timeout=2, string='Index')
        answer = answer.replace('\\n\\r      ', ' ')
        answer = ' '.join(answer.split())

        # если лог не отобразился
        if not ('Index' in answer):
            self.session.push('q', read=True)  # прервать команду лога
            return {'error': True}

        pattern = (  # паттерн любой записи лога
            r'[0-9]+ +[0-9-]+ +[0-9:]+ +[0-9:A-Za-z()., -"+]+\\')
        log = self._findall(pattern, answer)

        # поиск времени последней записи
        self._find(r'[0-9-]+ [0-9]+:', answer)
        log_last_time = self._time_to_hours(self._finded)
        log_time_range = 0
        # print(answer)

        # пока охват меньше заданных часов, и количество записей меньше 100
        while (log_time_range < hours) and (len(log) < 1000):
            self.session.push('nnn')
            answer = self.session.read()
            answer = answer.replace('\\n\\r     ', ' ')
            answer = ' '.join(answer.split())

            log += self._findall(pattern, answer)
            if log:  # если лог не пустой, определяет охват времени
                log_bottom_time = self._find(r'[0-9-]+ [0-9]+:', log[-1])
                log_time_range = log_last_time - self._time_to_hours(log_bottom_time)

        self.session.push('q', read=True)  # прервать выдачу лога

        for elem in log:  # выборка записей о нужном порте
            elem = elem.replace('\\', ' ')
            if ((f'ort {port} ' in elem) or (f'orts {port} ' in elem)) and (len(result['log']) < 20):
                result['log'].append(elem)
                if ('storm' in elem) or ('loop' in elem):
                    result['snmp'].append(elem)

        # 'ок':True будет, если длина лога < 50, и нет штормов/колец
        result['ok'] = (len(result['log']) < 50) and (not result['snmp'])
        return result

    # проверка, в лузе ли порт
    def loose(self, port: int) -> dict:
        self.session.read()
        self.session.push('\nshow address_binding ports')
        self.session.push('nnnn')
        answer = self.session.read(string='ARP')

        if not ('ARP' in answer):
            return {'error': True}

        loose = bool(self._find('r' + str(port) + '[ ]+Loose', answer))
        return {'ok': loose, 'error': False}

    # включение/выключение порта
    def set_port(self, port: int, enable: bool):
        if enable:
            self.session.push(f'config ports {port} state enable', read=True)
        else:
            self.session.push(f'config ports {port} state disable', read=True)
        return {'ok': True}

    # порт в loose/strict
    def set_bind(self, port: int, loose: bool) -> dict:
        command = 'config address_binding ip_mac ports ' + str(port)

        if loose:  # если просят луз
            self.session.push(command + ' arp_inspection loose \n', read=True)
            self.session.push(command + ' state enable loose \n', read=True)
            return {'ok': True, 'error': False}

        else:  # если просят в стрикт
            self.session.push(command + ' arp_inspection strict \n', read=True)
            self.session.push(command + ' state enable strict \n', read=True)

    # очистить ошибки
    def clear(self, port: int):
        self.session.push(f'clear counter ports {port}', read=True)
        return {'ok': True}
