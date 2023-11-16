from connections.switches.utils.timing import timing
import re


class SwitchMixin:
    test_methods = []
    _mac_pattern = r'\w\w[:-]\w\w[:-]\w\w[:-]\w\w[:-]\w\w[:-]\w\w'
    _mac_pattern_old = r'\w\w\w\w[.]\w\w\w\w[.]\w\w\w\w'
    _ip_pattern = r'[0-9.]+'

    # диагностика всего
    @timing
    def test_all(self, port: int, pon: int = 0, vertical=False, speed=False):
        print()
        error_list = []
        for method in self.test_methods:

            if speed: method = timing(method)
            else: print(method.__name__.upper(), '  ', end='')

            if pon: res = (method(port, pon))
            else: res = (method(port))

            if res['error']:
                error_list.append(method.__name__)

            if vertical and ('log' in res):
                print(res)
                for elem in res['log']:
                    print(elem)
            else:
                print(res)

        return error_list

    # перевод мака из AB-CD-EF-01-02-03 в ab:cd:ef:01:02:03
    @staticmethod
    def _fix_mac(mac: str) -> str:
        mac = mac.lower()
        mac = mac.replace('-', ':')
        if not ('.' in mac):
            return mac
        mac = mac.replace('.', '')
        return ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])

    # перевод строки 2023-10-20 23:02:04 в количество часов
    @staticmethod
    def _time_to_hours(date: str) -> int:
        t = date.replace('-', ' ')
        t = t.replace(':', ' ')
        t = t.split()
        # print(time)
        for i in range(4):
            t[i] = int(t[i])
        hours = t[0]*8760 + t[1]*744 + t[2]*24 + t[3]
        return int(hours)

    # вынесенный поиск регулярны выражений
    # @timing
    def _find(self, pattern, text) -> str:
        self._finded = re.search(pattern, text)
        if self._finded:
            self._finded = self._finded.group(0)
            return self._finded

    # вынесенный поиск списков регулярных выражений
    def _findall(self, pattern, text) -> list:
        self._finded = re.findall(pattern, text)
        return self._finded


if __name__ == '__main__':
    print(SwitchMixin._fix_mac('1234.5678.abcd'))
    SwitchMixin._time_to_hours('2023-10-12 00:02:04')
