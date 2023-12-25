from .app_init import DiagError, logging
from .requests_api import GcdbApi


class GcdbData:

    def __init__(self, request):
        self.username = request.args.get('username')
        self.anumber = request.args.get('anumber')
        self.switch_ip = request.args.get('switch_ip')
        self.switch_port = request.args.get('switch_port')
        self.pon_port = request.args.get('pon_port')

        self.abon_ip = request.args.get('real_ip')
        if not self.abon_ip:
            self.abon_ip = request.args.get('local_ip')

        self.ip_list = [self.abon_ip]
        self.mac_list = []
        self.group_ticket = []

        if not (self.username and self.switch_ip and self.switch_port):
            raise DiagError('Неполный запрос')

        self.update_data()
        logging.info(f'{self.username} opened {self.switch_ip} : {self.switch_port} : {self.pon_port}')

    # отправляет запрос к gcdb_api, сортирует данные
    def update_data(self):
        data = GcdbApi.get_data(self.anumber, self.switch_ip)
        if not data:
            return

        if data['group_tickets']:
            self.group_ticket = sorted(data['group_tickets'])[-1]
        del data['group_tickets']

        # print(self.group_ticket)
        for key, elem in data.items():
            if elem['mac'] and not elem['mac'] in self.mac_list:
                self.mac_list.append(elem['mac'])

            ip = elem['r_ip'] if elem['r_ip'] else elem['l_ip']
            if not (ip in self.ip_list):
                self.ip_list.append(ip)

    # def __del__(self):
    #     print('gcdb_data object deleted')
