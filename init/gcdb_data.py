from pprint import pprint

from .app_init import DiagError, logging
from .requests_out import GcdbApi


class GcdbData:

    def __init__(self, request):
        self.username = request.args.get('username')
        self.anumber = request.args.get('anumber')
        self.ctype = request.args.get('ctype')
        self.abon_login = request.args.get('abon_login')
        self.switch_ip = request.args.get('switch_ip')
        self.switch_port = int(request.args.get('switch_port'))
        self.pon_port = request.args.get('pon_port')
        self.vlan = ''

        self.abon_ip = request.args.get('real_ip')
        if not self.abon_ip:
            self.abon_ip = request.args.get('local_ip')

        self.phone = request.args.get('phone')
        if not self.phone:
            self.phone = ''

        self.ip_list = []
        if self.abon_ip:
            self.ip_list.append(self.abon_ip)
        self.mac_list = []
        self.group_tickets = {}

        if not (self.username and self.switch_ip and self.switch_port):
            raise DiagError('Неполный запрос')

        logging.info(f'{self.username} opened {self.switch_ip} : {self.switch_port} : {self.pon_port}')

    # отправляет запрос к gcdb_api, сортирует данные
    def update_data(self):
        data = GcdbApi.get_data(self.anumber, self.switch_ip)
        if not data:
            return

        if data['group_tickets']:
            for key, elem in data['group_tickets'].items():
                if len(elem) > 25:
                    elem = elem[0:25]
                self.group_tickets[key] = elem[0:25]

        # print(self.group_tickets)
        for elem in data['accounts']:
            if elem['mac'] and not elem['mac'] in self.mac_list:
                self.mac_list.append(elem['mac'])

            ip = elem['r_ip'] if elem['r_ip'] else elem['l_ip']
            if ip and not (ip in self.ip_list):
                self.ip_list.append(ip)
    # def __del__(self):
    #     print('gcdb_data object deleted')


class Air:
    def __init__(self):
        self.base = None
        self.station = None
        self.ip_list = []
