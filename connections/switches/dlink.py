from connections.switches.utils.mixin import SwitchMixin
from connections.telnet import Telnet


class Dlink(SwitchMixin):
    """Класс для работы со свитчами Dlink \n
    проверки:\n port, bind, mac, errors, cable, bind_state, log
    действия:\n set_port, set_bind, clear"""

    def __init__(self, session: Telnet):
        self.session = session
        self.model = session.switch_model
        self.ip = session.switch_ip
        self.session.push('enable clipaging')
        self.session.read()
        self.test_methods = [  # методы для тестов
            self.port, self.errors,
            self.bind_state, self.mac, self.bind,
            self.cable, self.log, self.util]

    # диагностика порта
    def port(self, port: int) -> dict:
        result = {'enabled': 'Enabled', 'port': '', 'ok': True, 'error': False}
        self.session.read(timeout=0)
        self.session.push(f'\nshow ports {port} ')
        answer = self.session.read(string='Speed', timeout=1)
        self.session.push('q')

        if self._find(r'[0-9][ ]+Disabled[ ]+', answer):
            result['enabled'] = 'Disabled'
            result['ok'] = False

        port_patterns = [  # список для поиска в ответе и статусы
            [r'100M/Full/[A-Za-z]+', True],
            [r'[0-9]+M/\w\w\w\w/[A-Za-z]+', False],
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
        self.session.read(timeout=0)
        self.session.push(f'\nshow address_binding dhcp_snoop binding_entry port {port}')
        answer = self.session.read(timeout=2, string='Entries')
        self.session.push('q')

        des_binding_patterns = [
            ['DES-3028',  # список паттернов для DES-3028
             r'Port[ ]+Status',
             r'[0-9.]+[ ]+[A-Za-z0-9- ]+ive',
             r'Active'],
            ['DES-3200',  # список паттернов для DES-3200
             r'A: Active',
             r'[0-9.]+[ ]+[A-Z0-9-]+ [A-Z]',
             r'\w\w A'],
            ['DES-1028',  # список паттернов для DES-1028
             r'Port[ ]+Lease',
             r'[0-9.]+[ ]+[A-Za-z0-9- ]+ive',
             r'Active']]

        for elem in des_binding_patterns:
            if self._find(elem[1], answer):
                des_bind_all = elem[2]
                des_bind_pattern = elem[3]
                break
        else:  # вообще не найден ответ
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
    def mac(self, port: int, macs: list) -> dict:
        result = {'mac': {}, 'ok': True, 'error': False}
        self.session.read(timeout=0)
        self.session.push(f'\nshow fdb port {port}')
        answer = self.session.read(timeout=2, string='Entries')

        if not ('Entries' in answer):
            return {'error': True}

        mac_list = self._findall(self._mac_pattern, answer)
        if not mac_list:
            return {'ok': False, 'error': False}

        for mac in mac_list:
            mac = self._fix_mac(mac)
            result['mac'][mac] = (mac in macs)
        return result

    # поиск ошибок
    def errors(self, port: int) -> dict:
        result = {'rx': {}, 'tx': {}, 'ok': True, 'ok_tx': True, 'error': False}
        self.session.read()
        self.session.push(f'\nshow error ports {port}')
        answer = self.session.read(string='RX Frames', timeout=1)
        self.session.push('\nq', read=True)

        if not ('RX Frames' in answer):
            return {'error': True}

        err_patterns = {'crc': r'CRC Error[ ]+[0-9-]+',
                        'frg': r'Fragment[ ]+[0-9-]+',
                        'jab': r'Jabber[ ]+[0-9-]+'}

        for key, pattern in err_patterns.items():
            if self._find(pattern, answer):
                res = self._finded.split()[-1]
                result['rx'][key] = res
                if int(res):
                    result['ok'] = False

        err_patterns = {'xdef': r'Excessive Deferral[ ]+[0-9-]+',
                        'lcol': r'Late Collision[ ]+[0-9-]+',
                        'xcol': r'Excessive Collision[ ]+[0-9-]+',
                        'scol': r'Single Collision[ ]+[0-9-]+',
                        'col': r'   Collision[ ]+[0-9-]+'}

        for key, pattern in err_patterns.items():
            if self._find(pattern, answer):
                res = self._finded.split()[-1]
                result['tx'][key] = res
                if int(res):
                    result['ok'] = False
                    result['ok_tx'] = False

        return result

    # диагностика кабеля
    def cable(self, port: int) -> dict:
        result = {'cable': [], 'ok': True, 'error': False}
        self.session.read(timeout=0)
        self.session.push(f'cable_diag ports {port}\n')
        answer = self.session.read(timeout=2, string='Result')
        self.session.push('q\n')

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
    def log(self, port: int = 0, hours: int = 24) -> dict:
        result = {'snmp': [], 'log': [],
                  'ok': True, 'error': False}
        self.session.read(timeout=0)
        self.session.push('\nshow log')
        answer = self.session.read(timeout=2, string='Index')
        answer = answer.replace('\\n\\r     ', '+++')
        answer = ' '.join(answer.split()).replace('+++', '')

        # если лог не отобразился
        if not ('Index' in answer):
            self.session.push('q')  # прервать команду лога
            return {'error': True}

        pattern = (  # паттерн любой записи лога
            r'[0-9]+ +[0-9-]+ +[0-9:]+ +[0-9:A-Za-z()., -"+]+\\')
        log = []
        for elem in self._findall(pattern, answer):
            log.append(elem.strip('\\').replace('  ', ' '))

        # поиск времени последней записи
        self._find(r'[0-9-]+ [0-9]+:', answer)
        log_last_time = self._time_to_hours(self._finded)
        log_time_range = 0
        attempt = 0
        # print(answer)

        # пока охват меньше заданных часов, и проходов меньше 20
        while log_time_range < hours:

            attempt += 1
            if attempt > 20:
                break

            self.session.push('nnn')
            answer = self.session.read()
            answer = answer.replace('\\n\\r     ', '+++')
            answer = ' '.join(answer.split()).replace('+++', '')

            for elem in self._findall(pattern, answer):
                log.append(elem.strip('\\').replace('  ', ' '))

            if log:  # если лог не пустой, определяет охват времени
                log_bottom_time = self._find(r'[0-9-]+ [0-9]+:', log[-1])
                log_time_range = log_last_time - self._time_to_hours(log_bottom_time)

        self.session.push('q')  # прервать выдачу лога

        if port == 0:
            result['log'] = log
            return result

        for elem in log:  # выборка записей о нужном порте
            if ((f'ort {port} ' in elem+' ') or (f'orts {port} ' in elem+' ')) and (len(result['log']) < 20):
                result['log'].append(elem)
                if ('storm' in elem) or ('loop' in elem):
                    result['snmp'].append(elem)

        if attempt > 20:
            result['log'].append('Прочитал лог меньше суток! Вероятно, кто-то ПОСил.')

        # 'ок':True будет, если длина лога < 50, и нет штормов/колец
        result['ok'] = (len(result['log']) < 50) and (not result['snmp'])
        return result

    # утилизация порта
    def util(self, port: int = 0) -> dict:
        result = {'rx': 0, 'tx': 0, 'error': False}

        if port:
            self.session.read(timeout=0)
            self.session.push(f'show packet ports {port}')
            answer = self.session.read(1, 'TX Frames')
            self.session.push('q\n')
            if not ('TX Frames' in answer):
                return {'error': True}

            answer = answer.replace('\\t', '')
            rx = self._find(r'RX Bytes +[0-9]+ +[0-9]+', answer).split()[-1]
            tx = self._find(r'TX Bytes +[0-9]+ +[0-9]+', answer).split()[-1]

            # перевод из байтов в кбиты
            rx = int(rx) / 128
            tx = int(tx) / 128

            # если трафик больше мбита, переводит в них
            value = ' KB/s'
            if tx > 1024 or rx > 1024:
                value = ' MB/s'
                rx, tx = rx/1024, tx/1024

            result['rx'] = f'{int(rx)} {value}'
            result['tx'] = f'{int(tx)} {value}'

        return result

    # обнаружение флуда
    def flood(self) -> dict:
        self.session.read(timeout=0)
        self.session.push('\nshow util ports')
        answer = self.session.read(string='RX')
        self.session.push('q')
        if not ('RX' in answer):
            return {'error': True}

        answer = answer.split('\\n\\r')
        rx_low = []
        rx_high = []
        for elem in answer:
            try:  # пытается взять кол-во пакетов из строки
                elem = int(elem.split()[1])
                if elem > 4_000:
                    rx_high.append(elem)
                elif elem >= 0:
                    rx_low.append(elem)
            except Exception:
                pass

        #  если нет большого трафла, или разница в трафике больше 5к
        if not rx_high or (rx_high[0] - rx_high[-1]) > 5_000:
            return {'flood': False, 'error': False}

        return {'flood': True, 'flood_rx': rx_high[0], 'error': False}

    # проверка, есть ли подписки
    def igmp(self, port: int) -> dict:
        result = {'port': False, 'other': False, 'error': False}
        self.session.read(timeout=0)
        self.session.push('\nshow igmp_snooping host')
        answer = self.session.read(string='Entries')
        if not ('Entries' in answer):
            return {'error': True}

        subscribes = self._findall(r'[0-9]+ +[0-9.]+ +[0-9]+ +[0-9.]+', answer)
        if not subscribes:
            return result

        port_igmp = 0  # поиск подписок нужного порта
        for elem in subscribes:
            if int(elem.split()[2]) == port:
                port_igmp += 1

        if port_igmp:  # если есть подписки порта
            result['port'] = port_igmp
            return result

        #  если нет подписок нужного порта, укажет подписки других
        result['other'] = len(subscribes) - port_igmp
        return result

    # проверка, в лузе ли порт
    def bind_state(self, port: int) -> dict:
        self.session.read()
        self.session.push('\nshow address_binding ports')
        self.session.push('nnnn')
        answer = self.session.read(string='ARP')

        if not ('ARP' in answer):
            return {'error': True}

        answer = answer.replace('\\r', '  ').replace('\\n', '\n')

        if bool(self._find(' ' + str(port) + '[ ]+Disabled', answer)):
            return {'state': 'Disabled', 'error': False}
        else:
            strict = bool(self._find('[ ]' + str(port) + '[ ]+Strict', answer))
            return {'state': 'Strict' if strict else 'Loose', 'error': False}

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

    # def __del__(self):
    #     print('dlink object deleted')


#

class Dlink1210(Dlink):
    """Отдельный класс для работы со свитчами DES-1210 \n
    переопределены: cable, log"""

    # диагностика кабеля
    def cable(self, port: int) -> dict:
        result = {'cable': [], 'ok': True, 'error': False}
        self.session.read(timeout=0)
        self.session.push(f' cable diagnostic port {port}\n')
        answer = self.session.read(timeout=5, string='Success')
        self.session.push('q\n')

        if self._findall(r'Pair[A-Za-z0-9 ]+M', answer):
            pairs = self._finded
            try:
                pair1 = int(pairs[0].replace('M', '').split()[-1])
                pair2 = int(pairs[1].replace('M', '').split()[-1])
                # если разница в парах больше 5ти, или кабель длиннее 90м
                result['ok'] = (abs(pair1 - pair2) < 5) and (pair1 < 90)
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
    def log(self, port: int = 0, hours: int = 24) -> dict:
        result = {'snmp': [], 'log': [],
                  'ok': True, 'error': False}
        self.session.read(timeout=0)
        self.session.push('\nshow log')
        answer = self.session.read(timeout=2, string='Index')
        answer = answer.replace('\\n\\r      ', ' ')
        answer = ' '.join(answer.split())

        # если лог не отобразился
        if not ('Index' in answer):
            self.session.push('q')  # прервать команду лога
            return {'error': True}

        pattern = (  # паттерн любой записи лога
            r'[0-9]+ +[A-Za-z]+ +[0-9]+ +[0-9A-Za-z: "-]+\\')
        log = []
        for elem in self._findall(pattern, answer):
            log.append(elem.strip('\\'))

        # пока проходов меньше 10
        for i in range(10):

            self.session.push('nnn')
            answer = self.session.read()
            answer = answer.replace('\\n\\r     ', ' +++')
            answer = ' '.join(answer.split()).replace('+++', '')

            for elem in self._findall(pattern, answer):
                log.append(elem.strip('\\'))

        self.session.push('q')  # прервать выдачу лога

        if port == 0:
            result['log'] = log
            return result

        for elem in log:  # выборка записей о нужном порте
            if (f'ort {port} ' in elem) or (f'orts {port} ' in elem) or f' {port}"' in elem:
                result['log'].append(elem)
                if ('storm' in elem) or ('loop' in elem):
                    result['snmp'].append(elem)

        result['log'].append(f'Прочитано {len(result["log"])} записей лога.')

        # 'ок':True будет, если длина лога < 50, и нет штормов/колец
        result['ok'] = (len(result['log']) < 50) and (not result['snmp'])
        return result
