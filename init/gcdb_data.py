from .app_init import DiagError, logging
from connections import switch_login, switch_password
from connections import tolerance_login, tolerance_password


class GcdbData:
    __slots__ = ("username",
                 "switch_ip",
                 "switch_port",
                 "pon_port",
                 "abon_ip",
                 "mac_list",
                 "anumber")

    def __init__(self, request):

        self.username = request.args.get('username')
        self.anumber = request.args.get('anumber')

        self.switch_ip = request.args.get('switch_ip')
        self.switch_port = request.args.get('switch_port')
        self.pon_port = request.args.get('pon_port')

        self.abon_ip = request.args.get('real_ip')
        if not self.abon_ip:
            self.abon_ip = request.args.get('local_ip')

        self.mac_list = (
            request.args.get('abon_mac'),
            request.args.get('stb1_mac'),
            request.args.get('stb2_mac'),
            request.args.get('stb3_mac'),
            request.args.get('stb4_mac'),
            request.args.get('stb5_mac'),
            request.args.get('stb6_mac')
        )

        logging.info(f'{self.username} on {self.switch_ip} : {self.switch_port} : {self.pon_port}')


        if not (self.username and self.switch_ip and self.switch_port):
            raise DiagError('Неполный запрос')

    def __del__(self):
        print('gcdb_data object deleted')
