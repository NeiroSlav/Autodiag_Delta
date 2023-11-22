from .app_init import DiagError
from connections import switch_login, switch_password


class GcdbData:

    def __init__(self, request):
        self.username = request.args.get('username')
        self.switch_login = switch_login
        self.switch_password = switch_password

        self.switch_ip = request.args.get('switch_ip')
        self.switch_port = request.args.get('switch_port')
        self.pon_port = request.args.get('pon_port')

        self.abon_ip = request.args.get('real_ip')
        if not self.abon_ip:
            self.abon_ip = request.args.get('local_ip')

        self.mac_list = [
            request.args.get('abon_mac'),
            request.args.get('stb1_mac'),
            request.args.get('stb2_mac'),
            request.args.get('stb3_mac'),
            request.args.get('stb4_mac'),
            request.args.get('stb5_mac'),
            request.args.get('stb6_mac'),
        ]

        if not (self.username and self.switch_ip and self.switch_port):
            raise DiagError('Неполный запрос')
